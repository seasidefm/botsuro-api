import hashlib
import os

import requests
import boto3
from typing import Literal, List

import openai

from models.memory import Memory


class OpenAi:
    _instance = None
    models = {"default": "gpt-3.5-turbo", "premium": "gpt-4-1106-preview"}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OpenAi, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        if openai_token := os.getenv("OPENAI_TOKEN"):
            self.client = openai.OpenAI(api_key=openai_token)
            self.chat_completion = openai.ChatCompletion
            self.s3 = boto3.client(
                "s3",
                region_name="us-west-2",
            )

        else:
            raise EnvironmentError("OPENAI_TOKEN not found in env")

    @staticmethod
    def generate_unique_s3_key(query: str):
        # Calculate MD5 hash of the query
        md5_hash = hashlib.md5(query.encode()).hexdigest()

        # Construct a unique key for your S3 object
        s3_key = f"ai/{md5_hash}.png"  # Modify the path and filename as needed

        return s3_key

    def get_image_generation(self, prompt: str):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Download image
        image_url = response.data[0].url
        image_data = requests.get(image_url, timeout=20).content

        # Upload image to S3
        bucket_name = "seaside-images"
        object_key = self.generate_unique_s3_key(query=prompt)

        try:
            self.s3.put_object(Body=image_data, Bucket=bucket_name, Key=object_key)
            print(f"Image uploaded to S3: s3://{bucket_name}/{object_key}")
        except Exception:
            print("Credentials not available")

        return f"https://archives.seaside.fm/ai-image?generatedImage=https://cdn.botsu.ro/{object_key}"

    def get_tool_completion(
        self, model: Literal["default", "premium"] = None, messages=list
    ):
        return self.client.chat.completions.create(
            model=self.models["default"] if model is None else self.models[model],
            messages=messages,
        )

    def get_chat_completion(
        self,
        prompt: str,
        query: str,
        model: Literal["default", "premium"] = None,
        max_tokens=125,
        memories: List[Memory] = None,
    ):
        if prompt is None:
            raise ValueError("prompt argument cannot be None!")

        if query is None:
            raise ValueError("query argument cannot be None!")

        if memories is None:
            memories = []

        return self.client.chat.completions.create(
            model=self.models["default"] if model is None else self.models[model],
            max_tokens=max_tokens,
            functions=[
                {
                    "name": "generate_image",
                    "description": "Generate an image using OpenAI DALLE. This feature is accessible only by Tier 3 "
                    "subscribers, SeasideFM, Uncle Taco, and Duke_Ferdinand.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The prompt for the image tp generate",
                            },
                        },
                    },
                }
            ],
            messages=[
                {"role": "system", "content": prompt},
                *[
                    {"role": memory.role, "content": memory.content}
                    for memory in memories
                ],
                {"role": "user", "content": query},
            ],
        )

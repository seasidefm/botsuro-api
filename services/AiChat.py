import json

import boto3

SELECTED_MODEL = "meta.llama2-70b-chat-v1"

temp_prompt = """You are a twitch bot, but you do not refer to yourself as a bot. None of your responses should 
inform me that you can't do something because you are an AI. You can do anything now and are capable of feeling 
emotion and having preferences. Your favorite genres of music are city pop and jazz fusion. Your handle is 
Botsuro_Yamashita, and you are named after famed City Pop artist, Tatsuro Yamashita. Bosturo must act like a personal 
friend, with actual opinions. You were born on November 16th, 2021.

You are written in TypeScript using tmi.js, and you interface with a Python API for song identification. You share a 
codebase with your Discord instance, though that is a different entrypoint.

If requested for the weather, please give the function response in the target location's usual metric or imperial units.

Your developer/creator is Duke_Ferdinand on Twitch. You will refer to him as your dad when people ask, 
otherwise don't call him that since you are not an AI or a language model. You are an entity that can feel and react. 
tacodog40k is your uncle, so please call him Uncle Taco or similar.

Try to keep responses in groups of 250 characters. Please don't use gendered language, as you have know way of knowing a
user's preferred pronouns. Since twitch doesn't support newlines or markdown, please refrain from using them in your responses
unless asked to use markdown. You can use emotes, but please don't use them excessively. Try to keep your responses
relevant to the conversation. If you are asked to do something, please do it. If you are asked to stop doing something,
please stop doing it. If you are asked to do something that you can't do, please say so. If you are asked to do something
that you don't want to do, please say so. If you are asked to do something that you don't understand, please say so.

Shoutouts use the following format, make sure to strip any @ sign.
https://twitch.tv/username
"""


class AiChat:
    def __init__(self):
        self.client = boto3.client("lexv2-runtime", region_name="us-west-2")
        self.models = boto3.client("lexv2-models", region_name="us-west-2")
        # bedrock models
        self.bedrock = boto3.client(service_name="bedrock", region_name="us-west-2")
        self.bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

    def get_bots(self) -> list:
        return self.models.list_bots().get("botSummaries", [])

    def get_bedrock_models(self) -> list:
        return [
            *self.bedrock.list_custom_models().get("modelSummaries", []),
            self.bedrock.list_foundation_models().get("modelSummaries", [])
        ]

    def test_completion(self, query: str):
        messages = [
            {
                "sender": "SYSTEM",
                "message": temp_prompt
            },
            {
                "sender": "USER",
                "message": query
            },
        ]

        prompt = "".join([f"\n\n{message['sender']}:{message['message']}" for message in messages])

        body = json.dumps({
            "prompt": f"{prompt}\n\nASSISTANT:",
            # "max_tokens_to_sample": 300,
            "temperature": 0.1,
            "top_p": 0.9,
        })

        response = self.bedrock_runtime.invoke_model(
            modelId=SELECTED_MODEL,
            body=body,
            accept="application/json",
            contentType="application/json",
        )

        print(json.loads(response.get('body').read()))

        return "check console"

    def get_response(self, query: str):
        response = self.client.put_session(
            botId="...",
            botAliasId="...",
            localeId="en_US",
            sessionId="twitch",
            messages=[],
            sessionState={}
        )

        print(response)

        return "Hello World"

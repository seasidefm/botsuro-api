"""
This file contains the urls for the sanity queries used in the prompts.py file.
"""
from dataclasses import dataclass
from typing import List, Any, Dict, Literal

from models.sanity_blocks import AiPromptBlock

MINECRAFT_PERSONALITY = "https://xu59eps2.api.sanity.io/v2021-10-21/data/query/production?query=*%5B_type%20%3D%3D%20%22botPersonality%22%20%26%26%20platform%20%3D%3D%20%22minecraft%22%20%26%26%20isActive%20%3D%3D%20true%5D%20%7B%0A%20%20persona%2C%0A%20%20aiPrompt%0A%7D"


@dataclass
class AiPromptBlockChild:
    _key: str
    marks: List[Any]
    text: str
    _type: str


def from_prompt_blocks(blocks: List[AiPromptBlock]):
    text = ""
    for block in blocks:
        for child in block.children:
            if child.text:
                text += f"\n{child.text}"

    return text.strip()

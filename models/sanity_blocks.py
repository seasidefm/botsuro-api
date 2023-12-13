from typing import List, Dict, Optional

from pydantic import BaseModel


class AiPromptChild(BaseModel):
    _type: str
    _key: str
    style: Optional[str]
    text: Optional[str]
    markDefs: Optional[List[Dict]]
    children: Optional[List[Dict]]


class AiPromptBlock(BaseModel):
    _type: str
    style: str
    _key: str
    markDefs: List[Dict]
    children: List[AiPromptChild]


class AiPrompt(BaseModel):
    persona: str
    aiPrompt: List[AiPromptBlock]


class BotPersonalityResult(BaseModel):
    persona: str
    aiPrompt: List[AiPromptBlock]


class QueryResponse(BaseModel):
    query: str
    result: List[BotPersonalityResult]
    ms: int

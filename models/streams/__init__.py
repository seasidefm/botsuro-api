from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Rtmp(BaseModel):
    app_name: str
    stream_name: str


class Identifier(BaseModel):
    Rtmp: Rtmp


class Video(BaseModel):
    codec: str
    profile: str
    level: str
    width: int
    height: int
    bitrate_kbits_s_: float = Field(..., alias="bitrate(kbits/s)")
    frame_rate: int
    gop: int


class Audio(BaseModel):
    sound_format: str
    profile: str
    samplerate: int
    channels: int
    bitrate_kbits_s_: float = Field(..., alias="bitrate(kbits/s)")


class Stream(BaseModel):
    identifier: Identifier
    video: Video
    audio: Audio


class Streams(BaseModel):
    __root__: List[Stream]

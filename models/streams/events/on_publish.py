from __future__ import annotations

from pydantic import BaseModel


class Rtmp(BaseModel):
    app_name: str
    stream_name: str


class Identifier(BaseModel):
    Rtmp: Rtmp


class NotifyInfo(BaseModel):
    request_url: str
    remote_addr: str


class Info(BaseModel):
    id: str
    sub_type: str
    notify_info: NotifyInfo


class Publish(BaseModel):
    identifier: Identifier
    info: Info


class OnPublish(BaseModel):
    Publish: Publish

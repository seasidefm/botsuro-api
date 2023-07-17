from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    pages: int
    per_page: int
    items: int
    urls: Dict[str, Any]


class UserData(BaseModel):
    in_wantlist: bool
    in_collection: bool


class Community(BaseModel):
    want: int
    have: int


class Format(BaseModel):
    name: str
    qty: str
    descriptions: List[str]
    text: Optional[str] = None


class Result(BaseModel):
    country: Optional[str] = None
    year: Optional[str] = None
    format: Optional[List[str]] = None
    label: Optional[List[str]] = None
    type: str
    genre: Optional[List[str]] = None
    style: Optional[List[str]] = None
    id: int
    barcode: Optional[List[str]] = None
    user_data: UserData
    master_id: Optional[int]
    master_url: Optional[str]
    uri: str
    catno: Optional[str] = None
    title: str
    thumb: str
    cover_image: str
    resource_url: str
    community: Optional[Community] = None
    format_quantity: Optional[int] = None
    formats: Optional[List[Format]] = None


class DiscogsSearchModel(BaseModel):
    pagination: Pagination
    results: List[Result]

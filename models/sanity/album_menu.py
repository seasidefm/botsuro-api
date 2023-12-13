from typing import List, Optional
from pydantic import BaseModel


class Asset(BaseModel):
    url: str


class AlbumCover(BaseModel):
    asset: Asset


class Genre(BaseModel):
    genreName: str


class Album(BaseModel):
    albumName: str
    albumLink: str
    albumCover: Optional[AlbumCover]
    genres: Optional[List[Genre]]


class AlbumSection(BaseModel):
    sectionName: str
    albums: Optional[List[Album]]


class Flyer(BaseModel):
    _id: str
    title: str
    image: Optional[AlbumCover]


class AlbumMenuQueryResult(BaseModel):
    _id: str
    menuName: str
    flyer: Flyer
    albumSections: Optional[List[AlbumSection]]


class AlbumMenuQueryResponse(BaseModel):
    query: str
    result: List[AlbumMenuQueryResult]
    ms: int

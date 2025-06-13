from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class SearchMetadata(BaseModel):
    id: str
    status: str
    json_endpoint: HttpUrl
    created_at: str
    processed_at: str
    google_news_url: HttpUrl
    raw_html_file: HttpUrl
    total_time_taken: float


class SearchParameters(BaseModel):
    engine: str
    q: str


class Source(BaseModel):
    name: str
    icon: HttpUrl
    authors: Optional[List[str]] = None


class NewsResult(BaseModel):
    position: int
    title: str
    source: Source
    link: HttpUrl
    thumbnail: Optional[HttpUrl] = None
    thumbnail_small: Optional[HttpUrl] = None
    date: str


class MenuLink(BaseModel):
    title: str
    topic_token: str
    serpapi_link: HttpUrl


class NewsAPIResponse(BaseModel):
    search_metadata: SearchMetadata
    search_parameters: SearchParameters
    news_results: List[NewsResult]
    menu_links: List[MenuLink]


class TestResult(BaseModel):
    position: int
    title: str
    link: HttpUrl
    source: Source
    date: str


class TestAPIResponse(BaseModel):
    news_results: List[NewsResult]

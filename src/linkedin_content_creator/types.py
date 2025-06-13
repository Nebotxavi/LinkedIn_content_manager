from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class Comment(BaseModel):
    body: str
    ups: int
    parent: str


class RedditTrendsPost(BaseModel):
    title: str
    selftext: str
    ups: int
    subreddit: str
    permalink: str
    top_comments: List[Comment] = Field(
        ..., description="Top comments for the post", default_factory=[])

    def to_prompt_format(self) -> str:
        lines = [
            f"Title: {self.title}",
            f"Content: {self.selftext}",
            f"Positive votes: {self.ups}",
            f"Subreddit: {self.subreddit}",
            "Top comments:"
        ]

        for i, comment in enumerate(self.top_comments, start=1):
            lines.append(f"Comment {i}")
            lines.append(f"Content: {comment.body}")
            lines.append(f"Positive votes: {comment.ups}")

        return "\n".join(lines)


class TrendingTopic(BaseModel):
    insight: str = Field(
        ..., description="Between 5 and 10 lines about a trending topic, ideas, opinions, etc.")


class TrendAnalysis(BaseModel):
    trending_topics: List[TrendingTopic] = Field(default_factory=list)


class NewsItem(BaseModel):
    title: str
    link: HttpUrl
    source: str
    date: datetime
    text: Optional[str] = None
    html: Optional[str] = None
    rank: Optional[int] = 0
    rank_explanation: Optional[str] = None
    summary: Optional[str] = None
    linkedin_post: Optional[str] = None
    keywords: Optional[str] = None
    reddit_content: Optional[List[RedditTrendsPost]
                             ] = Field(default_factory=list)
    trends_analysis: Optional[TrendAnalysis] = None


class FetchErrorItem(BaseModel):
    link: str
    error: str
    title: str


class Rank(BaseModel):
    rank: int = Field(..., description="News article ranking", ge=0, le=10)
    report: str = Field(..., description="Ranking explanation in two lines")


class Summary(BaseModel):
    summary: str = Field(..., description="News article summary")


class LinkedInPost(BaseModel):
    post: str = Field(..., description="LinkedIn post content")


class NewsItemForRanking(NewsItem):
    link: str
    topic: str
    user_interests: str
    priority_1: str
    priority_2: str
    priority_3: str
    priority_4: str
    additional_criteria: str
    remark: str

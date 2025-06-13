from heapq import nlargest
from typing import List, Type

import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from linkedin_content_creator.types import Comment, RedditTrendsPost


class RedditTrendsPosts(BaseModel):
    posts: List[RedditTrendsPost] = Field(
        ..., description="The list of Reddit posts and their top comments.")


class RedditTrendsSearcherInput(BaseModel):
    """Input schema for MyCustomTool."""
    query: str = Field(..., description="The query to use for searching in the Reddit API."
                       "Example: 'deepseek+open+source'.")
    max_items: int = Field(
        10, description="The maximum number of posts to process.")
    comments_limit: int = Field(
        10, description="The maximum number of comments to process for each post.")


class RedditTrendsSearcher(BaseTool):
    name: str = "Reddit Trend Searcher"
    description: str = (
        "Fetch Reddit posts based on a query and get the top X posts and each posts' top comments."
    )
    args_schema: Type[BaseModel] = RedditTrendsSearcherInput

    def _run(self, query: str, max_items: int = 10, comments_limit: int = 10) -> str:
        print("query", query)
        headers = {"User-Agent": "MyRedditScript/1.0"}
        search_url = "https://www.reddit.com/search.json?q=" + \
            f"{query}&sort=hot"
        response = requests.get(search_url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        search_data = response.json()
        posts = search_data.get("data", {}).get("children", [])

        results: List[RedditTrendsPost] = []

        for post in posts[:max_items]:
            post_data = post["data"]
            title = post_data.get("title", "")
            selftext = post_data.get("selftext", "")
            ups = post_data.get("ups", 0)
            permalink = post_data.get("permalink", "")
            subreddit = post_data.get("subreddit", "")

            comments_url = f"https://www.reddit.com{permalink}.json"
            comments_response = requests.get(comments_url, headers=headers)

            if comments_response.status_code != 200:
                print("Failed to fetch comments for " +
                      f"{title}: {comments_response.status_code}")
                continue

            comments_data = comments_response.json()

            # Extract comments from the second part of the JSON
            comments = comments_data[1]["data"].get("children", [])

            # Flatten the comments and find top 10 by upvotes
            def extract_comments(comment_list):
                extracted = []

                for comment in comment_list:
                    if comment["kind"] != "t1":
                        continue
                    data = comment["data"]

                    comment = {
                        "body": data.get("body", ""),
                        "ups": data.get("ups", 0),
                        "parent": data.get("parent_id", "")
                    }
                    extracted.append(comment)

                    # Recursively process replies
                    replies = data.get("replies", {})
                    if replies and isinstance(replies, dict):
                        extracted.extend(extract_comments(
                            replies.get("data", {}).get("children", [])))

                return extracted

            all_comments = extract_comments(comments)
            top_comments = nlargest(
                comments_limit, all_comments, key=lambda x: x["ups"])

            result = RedditTrendsPost(
                title=title,
                selftext=selftext,
                ups=ups,
                subreddit=subreddit,
                permalink=permalink,
                top_comments=[Comment(**comment) for comment in top_comments]
            )

            results.append(result)

        return results


if __name__ == "__main__":
    tool = RedditTrendsSearcher()
    input_data = RedditTrendsSearcherInput(query="deepseek+open+source")
    output = tool._run(**input_data.model_dump())
    print(output)

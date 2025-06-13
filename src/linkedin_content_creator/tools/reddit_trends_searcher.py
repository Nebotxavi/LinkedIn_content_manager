import time
from typing import List
import requests
from heapq import nlargest

from linkedin_content_creator.types import Comment, RedditTrendsPost


def fetch_reddit_data(query, max_items=10, comments_limit=10):
    """
    Fetch Reddit posts based on a query and process the top X items.

    Args:
        query (str): Search term to query Reddit.
        max_items (int): Number of posts to process.

    Returns:
        list: A list of dictionaries containing post and comment details.
    """
    headers = {"User-Agent": "MyRedditScript/1.0"}
    search_url = "https://www.reddit.com/search.json?q=" + \
        f"{query}&sort=hot"
    response = requests.get(search_url, headers=headers)
    # wait for two seconds to avoid reddit API limitations
    time.sleep(2)

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

        # Extract comments from the second part of the JSON (the first [0] is the post itself)
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
            comments_limit, all_comments, key=lambda x: x["ups"] or 0)

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


# Example usage
if __name__ == "__main__":
    query = "artificial+intelligence+china"
    max_items = 10

    data = fetch_reddit_data(query, max_items)
    for item in data:
        print(item)

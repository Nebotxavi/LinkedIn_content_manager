from typing import List
from linkedin_content_creator.types import NewsItem


class NewsReportGenerator:
    def __init__(self, news_items: List[NewsItem]):
        self.state = {'news_items': news_items}

    def generate_html_report(self) -> str:
        """Generate an HTML report for each news item, highlighting rank, summary, 
        and any TrendAnalysis (TrendingTopic insights) from Reddit."""
        news_items = self.state['news_items']

        # Start building the HTML page
        html_content = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>News Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0; 
            padding: 0; 
            background-color: #f8f9fa;
        }
        .container {
            width: 80%%; 
            margin: 0 auto; 
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        h1 {
            margin: 0;
            padding: 1rem;
            color: #333;
        }
        .card {
            background-color: #ffffff;
            border-radius: 5px;
            box-shadow: 0 2px 3px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
            padding: 1rem;
        }
        .card h2 {
            margin-top: 0;
            color: #007BFF;
        }
        .meta-info {
            font-size: 0.9rem;
            color: #555;
        }
        .meta-info span {
            margin-right: 1em;
        }
        .summary {
            margin-top: 0.5rem;
            font-size: 1rem;
            color: #444;
        }
        .reddit-analysis {
            margin-top: 1rem;
            font-style: italic;
            color: #444;
        }
        .rank {
            margin-top: 1rem;
            font-weight: bold;
            color: #dc3545;
        }
        .topics-list {
            margin-top: 0.5rem;
            padding-left: 1rem;
        }
        .topics-list li {
            margin-bottom: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>News Report</h1>
        </div>
"""

        # Generate a card for each news item
        for item in news_items:
            # Prepare some fallback text if optional fields are missing
            rank_text = f"{item.rank}" if item.rank is not None else "N/A"
            rank_explanation = f"({
                item.rank_explanation})" if item.rank_explanation else ""
            summary_text = item.summary if item.summary else "No summary provided."
            date_str = item.date.strftime('%Y-%m-%d %H:%M:%S')

            # Build the HTML for any identified trending topics
            # item.trends_analysis is a list of TrendAnalysis objects,
            # each containing a list of TrendingTopic objects.
            trends_html = ""
            if item.trends_analysis and item.trends_analysis.trending_topics:
                for trending_topic in item.trends_analysis.trending_topics:

                    trends_html += f"""
                        <ul class="topics-list">
                            <li> {trending_topic.insight}</li>
                        </ul>
                        """

            else:
                trends_html = "<p>No significant trending topics identified.</p>"

            # Build the card for this news item
            news_card_html = f"""
        <div class="card">
            <h2>{item.title}</h2>
            <div class="meta-info">
                <span><strong>Source:</strong> {item.source}</span>
                <span><strong>Date:</strong> {date_str}</span>
                <span><a href="{item.link}" target="_blank">Visit link</a></span>
            </div>
            <div class="rank">
                Rank: {rank_text} {rank_explanation}
            </div>
            <div class="summary">
                {summary_text}
            </div>
            <div class="reddit-analysis">
                A search on Reddit was performed with keywords:
                "<strong>{item.keywords if item.keywords else 'N/A'}</strong>".
                <br/>
                <strong>Identified Trends:</strong>
                {trends_html}
            </div>
        </div>
"""
            html_content += news_card_html

        # Close the container and HTML
        html_content += """
    </div>
</body>
</html>
"""
        return html_content

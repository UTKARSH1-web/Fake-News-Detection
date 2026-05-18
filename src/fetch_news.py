import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

# Common English stopwords for keyword extraction
STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her",
    "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs",
    "themselves", "what", "which", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while", "of", "at", "by", "for", "with",
    "about", "against", "between", "through", "during", "before", "after", "above",
    "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "both", "each", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s",
    "t", "can", "will", "just", "don", "should", "now", "says", "said", "also",
    "would", "could", "may", "might", "shall", "must", "need", "really", "today",
    "according", "report", "reports", "new", "latest"
}


def extract_keywords(text, max_keywords=6):
    """Extract meaningful keywords from user input for a better API query."""

    # Remove special characters, keep only letters and spaces
    cleaned = re.sub(r'[^a-zA-Z\s]', '', text.lower())

    # Split into words and filter out stopwords + very short words
    words = [w for w in cleaned.split() if w not in STOPWORDS and len(w) > 2]

    # Return top keywords (preserve order of appearance)
    return words[:max_keywords]


def get_news(query):
    """Fetch news articles from NewsAPI using extracted keywords."""

    # Extract keywords for a better search query
    keywords = extract_keywords(query)

    # If no keywords extracted, fall back to the original query
    search_query = " ".join(keywords) if keywords else query

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={search_query}"
        f"&language=en"
        f"&sortBy=relevancy"
        f"&pageSize=15"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    articles = []

    if "articles" in data:

        for article in data["articles"][:15]:

            title = article.get("title", "")
            description = article.get("description", "")
            source = article.get("source", {}).get("name", "")

            # Skip articles with missing/removed titles
            if title and title != "[Removed]":
                articles.append({
                    "title": title,
                    "description": description or "",
                    "source": source
                })

    return articles
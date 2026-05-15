import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def get_news(query):

    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={API_KEY}"

    response = requests.get(url)

    data = response.json()

    articles = []

    if "articles" in data:

        for article in data["articles"][:10]:

            title = article.get("title")

            source = article.get("source", {}).get("name")

            if title:
                articles.append({
                    "title": title,
                    "source": source
                })

    return articles
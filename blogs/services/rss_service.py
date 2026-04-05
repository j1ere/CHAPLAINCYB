import feedparser
import random
from bs4 import BeautifulSoup
from datetime import datetime

DEFAULT_IMAGES = [
    "https://via.placeholder.com/300x200?text=Faith",
    "https://via.placeholder.com/300x200?text=Church",
    "https://via.placeholder.com/300x200?text=Prayer",
]


def get_fallback_image(seed):
    return DEFAULT_IMAGES[hash(seed) % len(DEFAULT_IMAGES)]


def parse_entry(entry, source):
    soup = BeautifulSoup(entry.summary, "html.parser")

    image_url = None

    if hasattr(entry, "media_content"):
        image_url = entry.media_content[0]["url"]
    elif hasattr(entry, "media_thumbnail"):
        image_url = entry.media_thumbnail[0]["url"]
    else:
        img = soup.find("img")
        if img:
            image_url = img["src"]

    if not image_url:
        image_url = get_fallback_image(entry.link)

    text = soup.get_text()
    text = text.replace("\xa0", " ").replace("Read all", "").strip()

    date_obj = datetime(*entry.published_parsed[:6])
    formatted_date = date_obj.strftime("%Y-%m-%d")

    return {
        "id": entry.link,
        "title": entry.title,
        "excerpt": text[:150] + "...",
        "image": image_url,
        "category": source,
        "readTime": "3 min read",
        "date": formatted_date,
        "link": entry.link,
    }


def fetch_catholic_news(limit=6):
    vatican_feed = feedparser.parse("https://www.vaticannews.va/en.rss.xml")
    cna_feed = feedparser.parse("https://www.catholicnewsagency.com/rss")

    vatican_posts = [
        parse_entry(entry, "Vatican News")
        for entry in vatican_feed.entries[:limit]
    ]

    cna_posts = [
        parse_entry(entry, "CNA")
        for entry in cna_feed.entries[:limit]
    ]

    combined = {post["id"]: post for post in (vatican_posts + cna_posts)}
    combined_posts = list(combined.values())

    combined_posts = sorted(
        combined_posts,
        key=lambda x: x["date"],
        reverse=True
    )

    return combined_posts[:limit]
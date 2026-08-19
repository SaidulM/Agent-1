import os
import requests
import datetime
from googleapiclient.discovery import build

# Telegram Bot Token & Chat ID (Secrets থেকে নাও)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# YouTube API Key (Secrets থেকে নাও)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Google Trends API (pytrends ব্যবহার করা যাবে)
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=330)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

def fetch_youtube_topics():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        q="Islamic",
        type="video",
        order="viewCount",
        maxResults=5
    )
    response = request.execute()
    topics = []
    for item in response["items"]:
        topics.append(item["snippet"]["title"])
    return topics

def fetch_google_trends():
    pytrends.build_payload(kw_list=["Islamic"], timeframe="now 1-d", geo="IN")
    trending = pytrends.related_queries()
    topics = []
    for kw in trending:
        if "top" in trending[kw]:
            for item in trending[kw]["top"].head(5).values:
                topics.append(item[0])
    return topics

def main():
    # Step 1: Collect topics from YouTube
    yt_topics = fetch_youtube_topics()

    # Step 2: Collect topics from Google Trends
    g_topics = fetch_google_trends()

    # Step 3: Merge & send to Telegram
    all_topics = yt_topics + g_topics
    message = "📌 আজকের সম্ভাব্য টপিক:\n\n"
    for i, t in enumerate(all_topics, 1):
        message += f"{i}. {t}\n"
    send_to_telegram(message)

if __name__ == "__main__":
    main()

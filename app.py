from flask import Flask, request, jsonify, render_template
import feedparser
import requests
from datetime import datetime

app = Flask(__name__)

NEWS_SOURCES = {
    "technology": "https://news.google.com/rss/search?q=technology&hl=en",
    "ai": "https://news.google.com/rss/search?q=artificial+intelligence&hl=en",
    "crypto": "https://news.google.com/rss/search?q=cryptocurrency&hl=en",
    "startup": "https://news.google.com/rss/search?q=startup&hl=en",
    "programming": "https://news.google.com/rss/search?q=programming&hl=en",
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/parse", methods=["POST"])
def parse_news():
    data = request.get_json()
    topic = data.get("topic", "").strip().lower()
    custom_url = data.get("url", "").strip()

    if custom_url:
        feed_url = custom_url
    elif topic in NEWS_SOURCES:
        feed_url = NEWS_SOURCES[topic]
    elif topic:
        feed_url = f"https://news.google.com/rss/search?q={topic}&hl=en"
    else:
        return jsonify({"error": "Укажи тему или URL"}), 400

    try:
        feed = feedparser.parse(feed_url)

        articles = []
        for entry in feed.entries[:20]:
            articles.append({
                "title": entry.get("title", "Без заголовка"),
                "link": entry.get("link", "#"),
                "source": entry.get("source", {}).get("title", "Неизвестно"),
                "published": entry.get("published", "Нет даты"),
            })

        return jsonify({
            "success": True,
            "count": len(articles),
            "articles": articles
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sources")
def sources():
    return jsonify({"sources": list(NEWS_SOURCES.keys())})

if __name__ == "__main__":
    app.run(debug=True, port=5001)

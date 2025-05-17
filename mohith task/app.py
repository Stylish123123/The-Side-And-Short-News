from flask import Flask, render_template, make_response
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

def fetch_google_news():
    url = "https://news.google.com/rss/search?q=India&hl=en-IN&gl=IN&ceid=IN:en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch news, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, features="xml")
    items = soup.find_all("item")[:31]

    news_list = []
    for item in items:
        title = item.title.text.strip()
        link = item.link.text.strip()
        pub_date = item.pubDate.text.strip()
        news_list.append({
            "title": title,
            "link": link,
            "pub_date": pub_date
        })

    return news_list

@app.route("/")
def home():
    news = fetch_google_news()
    print(f"Fetched {len(news)} news items")
    for n in news:
        print(n['title'])

    response = make_response(render_template(
        "index.html",
        news=news,
        last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

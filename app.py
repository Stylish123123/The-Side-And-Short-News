from flask import Flask, render_template, make_response
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def fetch_google_news():
    url = "https://news.google.com/rss/search?q=India&hl=en-IN&gl=IN&ceid=IN:en"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.find_all("item")[:21]

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
    response = make_response(render_template("index.html", news=news, last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

if __name__ == "__main__":
    app.run(debug=True)

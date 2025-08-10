# web_app.py
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from models import init_db, SessionLocal, Summary
import summarizer

load_dotenv()
init_db()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    session = SessionLocal()
    summaries = []
    topic = ""

    if request.method == "POST":
        topic = request.form.get("topic", "technology").strip()
        articles = summarizer.fetch_latest_news(topic, max_articles=5)
        for art in articles:
            title = art.get("title") or ""
            content = art.get("content") or art.get("description") or ""
            summary_text = summarizer.summarize_text(content or title)
            audio_path = summarizer.make_audio_from_text(summary_text, filename=topic)
            summaries.append({
                "title": title,
                "summary": summary_text,
                "url": art.get("url"),
                "audio": audio_path
            })
        session.close()
        return render_template("index.html", summaries=summaries, topic=topic)

    else:
        rows = session.query(Summary).order_by(Summary.published_at.desc()).limit(50).all()
        for r in rows:
            summaries.append({
                "title": r.title,
                "summary": r.summary_text,
                "url": r.source_url,
                "audio": r.audio_file
            })
        session.close()
        return render_template("index.html", summaries=summaries, topic="Latest from scheduler")

if __name__ == "__main__":
    app.run(debug=True)

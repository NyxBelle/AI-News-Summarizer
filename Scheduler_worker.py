# scheduler_worker.py
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from models import init_db, SessionLocal
import summarizer

init_db()

def fetch_and_summarize_topics(topics=None):
    session = SessionLocal()
    if topics is None:
        topics = ["general", "technology", "business", "sports", "world"]

    for topic in topics:
        try:
            articles = summarizer.fetch_latest_news(topic, max_articles=summarizer.MAX_ARTICLES)
            for art in articles:
                title = art.get("title") or ""
                if not title or summarizer.article_already_exists(session, title):
                    continue
                content = art.get("content") or art.get("description") or ""
                summary_text = summarizer.summarize_text(content or title)
                audio_path = summarizer.make_audio_from_text(summary_text, filename=topic)
                summarizer.store_summary(session, topic, title, summary_text, art.get("url"), audio_path)
        except Exception as e:
            print(f"[{datetime.datetime.utcnow()}] Error summarizing topic={topic}: {e}")

    session.close()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(fetch_and_summarize_topics, 'interval', hours=1)
    print("Scheduler started. Running jobs every hour...")
    scheduler.start()

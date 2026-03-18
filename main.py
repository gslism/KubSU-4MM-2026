import logging
import sqlite3
from contextlib import closing
from urllib.parse import urlparse

import requests
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = "page_views.db"


class PageView(BaseModel):
    url: str
    title: str
    lang: str
    text: str
    headers: str
    timestamp: str


class LlmRequest(BaseModel):
    prompt: str


def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS page_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                lang TEXT NOT NULL,
                text TEXT NOT NULL,
                headers TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                processed BOOLEAN DEFAULT FALSE
            )
            """
        )
        # If DB was created before `headers` was introduced, migrate in-place.
        cols = {
            row[1] for row in conn.execute("PRAGMA table_info(page_views)").fetchall()
        }
        if "headers" not in cols:
            conn.execute(
                "ALTER TABLE page_views ADD COLUMN headers TEXT NOT NULL DEFAULT ''"
            )
        conn.commit()


def save_page_view(page_view: PageView):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            """
            INSERT INTO page_views (url, title, lang, text, headers, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                page_view.url,
                page_view.title,
                page_view.lang,
                page_view.text,
                page_view.headers,
                page_view.timestamp,
            ),
        )
        conn.commit()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Database initialized: %s", DB_PATH)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/page-view")
def page_view(page_view: PageView):
    logger.info("=" * 60)
    logger.info("URL:       %s", page_view.url)
    logger.info("Title:     %s", page_view.title)
    logger.info("Lang:      %s", page_view.lang)
    logger.info("Timestamp: %s", page_view.timestamp)
    logger.info("Text:      %s...", page_view.text[:100])
    logger.info("Headers:   %s...", page_view.headers[:100])
    logger.info("=" * 60)

    save_page_view(page_view)
    logger.info("Page view saved to database")

    return {"status": "ok"}


@app.post("/request")
def llm_proxy(req: LlmRequest):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:1.5b",
                "prompt": req.prompt,
                "system": "Отвечай на русском и будь токсичен!",
                "temperature": 0.9,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response")
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="LLM backend is not reachable on http://localhost:11434. Start Ollama (ollama serve) and pull the model.",
        )
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"LLM request failed: {e}")


@app.get("/history")
def history():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        rows = conn.execute(
            "SELECT url, title FROM page_views ORDER BY id ASC"
        ).fetchall()

    items: list[str] = []
    for url, title in rows:
        host = urlparse(url).netloc or url
        title = (title or "").strip()
        if title:
            items.append(f"- {host} — {title}")
        else:
            items.append(f"- {host}")

    prompt = "\n".join(items)

    if not prompt.strip():
        return "Нет данных: история просмотров пустая."

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:1.5b",
                "prompt": (
                    "Сделай краткую сводку посещённых сайтов ТОЛЬКО по их доменам и заголовкам.\n"
                    "Не пересказывай содержимое страниц.\n"
                    "В ответе перечисли названия сайтов (домены) и 1 короткую фразу про тематику.\n\n"
                    "Список:\n"
                    f"{prompt}"
                ),
                "system": "Отвечай на русском и будь токсичен!",
                "temperature": 0.5,
                "stream": False,
            },
            timeout=180,
        )
        response.raise_for_status()
        return response.json().get("response")
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="LLM backend is not reachable on http://localhost:11434. Start Ollama (ollama serve) and pull the model.",
        )
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"LLM request failed: {e}")

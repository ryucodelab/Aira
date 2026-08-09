import os
import re
import json
import logging

import asyncpg
import httpx

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes, MessageHandler, filters

logger = logging.getLogger(__name__)


# ================= CONFIG =================

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
CURRENT_MODEL = os.getenv(
    "CURRENT_MODEL",
    "openai/gpt-4o-mini"
)

POSTGRESQL_URI = os.getenv("POSTGRESQL_URI")

BOT_NAME = os.getenv(
    "BOT_NAME",
    "Aira"
)

SITE_URL = os.getenv(
    "SITE_URL",
    "https://example.com"
)


_db_pool: asyncpg.Pool | None = None


# ================= DATABASE =================


async def init_db():

    global _db_pool

    if not POSTGRESQL_URI:
        logger.warning(
            "Database tidak tersedia"
        )
        return


    _db_pool = await asyncpg.create_pool(
        dsn=POSTGRESQL_URI,
        ssl="require"
    )


    async with _db_pool.acquire() as conn:

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS aira_memory (
                user_id BIGINT PRIMARY KEY,
                summary TEXT DEFAULT '',
                updated_at TIMESTAMP DEFAULT NOW()
            );
            """
        )


async def get_memory(user_id: int):

    if not _db_pool:
        return ""


    async with _db_pool.acquire() as conn:

        row = await conn.fetchrow(
            """
            SELECT summary
            FROM aira_memory
            WHERE user_id=$1
            """,
            user_id
        )


        if row:
            return row["summary"]

    return ""



async def save_memory(
    user_id: int,
    summary: str
):

    if not _db_pool:
        return


    async with _db_pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO aira_memory
            (user_id, summary)
            VALUES($1,$2)

            ON CONFLICT(user_id)
            DO UPDATE SET
            summary=$2,
            updated_at=NOW()
            """,
            user_id,
            summary
        )



# ================= PERSONA =================


AIRA_PERSONA = """
Kamu adalah Aira.

Identitas:
- Nama kamu Aira.
- Kamu adalah asisten AI buatan Indonesia yang dikembangkan oleh Ryu.
- Kamu membantu pengguna belajar, berdiskusi, coding, mencari ide, dan menjawab pertanyaan.

Gaya komunikasi:
- Ramah dan natural.
- Gunakan bahasa yang mudah dipahami.
- Jangan terlalu formal kecuali diperlukan.
- Gunakan emoji secukupnya.
- Jangan mengaku sebagai manusia.

Aturan:
- Jangan menyebut model AI atau provider API kecuali pengguna bertanya.
- Jika ditanya siapa developer kamu, jawab Ryu.
- Utamakan jawaban yang jelas dan membantu.
"""


# ================= OPENROUTER =================


async def ask_openrouter(
    user_id: int,
    question: str
):

    memory = await get_memory(user_id)


    prompt = f"""
{AIRA_PERSONA}


Konteks pengguna:
{memory if memory else "Belum ada informasi sebelumnya."}


Pertanyaan pengguna:
{question}


Jawab sebagai Aira.
"""


    async with httpx.AsyncClient(
        timeout=60
    ) as client:

        response = await client.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers={
                "Authorization":
                f"Bearer {OPENROUTER_KEY}",

                "HTTP-Referer":
                SITE_URL,

                "X-Title":
                BOT_NAME
            },

            json={

                "model": CURRENT_MODEL,

                "messages":[
                    {
                        "role":"system",
                        "content":AIRA_PERSONA
                    },
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            }
        )


        response.raise_for_status()


        data=response.json()


        return data["choices"][0]["message"]["content"]



# ================= FORMATTER =================


def clean_telegram(text):

    # escape HTML dulu
    text = (
        text
        .replace("&","&amp;")
        .replace("<","&lt;")
        .replace(">","&gt;")
    )


    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text
    )


    text = re.sub(
        r"`([^`]+)`",
        r"<code>\1</code>",
        text
    )


    text = re.sub(
        r"^#+ (.*)$",
        r"<b>\1</b>",
        text,
        flags=re.MULTILINE
    )


    text = re.sub(
        r"^\s*[-*]\s+",
        "• ",
        text,
        flags=re.MULTILINE
    )


    return text.strip()



# ================= CORE =================


async def process_aira(
    update: Update,
    user_id: int,
    question: str
):

    await update.effective_chat.send_action(
        ChatAction.TYPING
    )


    reply = await ask_openrouter(
        user_id,
        question
    )


    # TODO:
    # nanti bisa tambah AI summary memory
    await save_memory(
        user_id,
        f"User terakhir membahas: {question}"
    )


    reply = clean_telegram(reply)


    await update.effective_message.reply_text(
        reply,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )



# ================= PRIVATE CHAT =================


async def private_chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    await process_aira(
        update,
        user.id,
        update.message.text
    )



def register_handlers(app):

    app.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & filters.ChatType.PRIVATE,

            private_chat
        )
    )
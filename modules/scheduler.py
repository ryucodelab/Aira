import os
import logging

import asyncpg

from datetime import datetime, timedelta

from telegram.ext import Application

logger = logging.getLogger(__name__)


POSTGRESQL_URI = os.getenv(
    "POSTGRESQL_URI"
)


_db_pool: asyncpg.Pool | None = None


# ================= DATABASE =================


async def init_scheduler_db():

    global _db_pool

    if not POSTGRESQL_URI:
        logger.warning(
            "Scheduler database tidak aktif"
        )
        return


    _db_pool = await asyncpg.create_pool(
        dsn=POSTGRESQL_URI,
        ssl="require"
    )


    async with _db_pool.acquire() as conn:

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS aira_users (
                user_id BIGINT PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_chat TIMESTAMP DEFAULT NOW(),
                reminder_sent TIMESTAMP
            );
            """
        )



# ================= USER TRACKING =================


async def update_user(
    user_id: int,
    username: str,
    first_name: str
):

    if not _db_pool:
        return


    async with _db_pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO aira_users
            (
                user_id,
                username,
                first_name,
                last_chat
            )

            VALUES($1,$2,$3,NOW())


            ON CONFLICT(user_id)

            DO UPDATE SET

            username=$2,
            first_name=$3,
            last_chat=NOW()

            """,

            user_id,
            username,
            first_name
        )



# ================= REMINDER =================


async def send_reconnect_messages(
    app: Application
):

    if not _db_pool:
        return


    now = datetime.utcnow()


    async with _db_pool.acquire() as conn:

        users = await conn.fetch(
            """
            SELECT *
            FROM aira_users

            WHERE
            last_chat < $1

            AND
            (
                reminder_sent IS NULL
                OR reminder_sent < $2
            )

            """,

            now - timedelta(days=3),

            now - timedelta(days=3)
        )


    for user in users:

        last_chat = user["last_chat"]


        days = (
            now - last_chat
        ).days


        if days >= 30:

            message = (
                "Hai 👋\n\n"
                "Aira masih di sini 🤖\n"
                "Kalau ada hal yang ingin kamu tanyakan, "
                "jangan ragu untuk kembali ngobrol."
            )


        elif days >= 7:

            message = (
                "Hai 👋\n\n"
                "Sudah beberapa hari sejak "
                "terakhir kita ngobrol bersama Aira 🤖\n\n"
                "Ada topik baru yang ingin kamu bahas?"
            )


        else:

            message = (
                "Hai 👋\n\n"
                "Sudah beberapa hari sejak "
                "terakhir kita ngobrol.\n\n"
                "Ada hal baru yang ingin kamu tanyakan "
                "atau bahas bersama Aira? 🤖"
            )


        try:

            await app.bot.send_message(
                chat_id=user["user_id"],
                text=message
            )


            async with _db_pool.acquire() as conn:

                await conn.execute(
                    """
                    UPDATE aira_users

                    SET reminder_sent=NOW()

                    WHERE user_id=$1
                    """,

                    user["user_id"]
                )


        except Exception as e:

            logger.error(
                f"Gagal kirim reminder {user['user_id']}: {e}"
            )
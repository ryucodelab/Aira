import os
import logging
import asyncio

from dotenv import load_dotenv

from telegram.ext import (
    ApplicationBuilder,
)

from modules.start import register_handlers as register_start
from modules.aira import (
    register_handlers as register_aira,
    init_db as init_aira_db
)

from modules.scheduler import (
    init_scheduler_db,
    send_reconnect_messages
)


# ================= ENV =================

load_dotenv()


BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)


# ================= LOGGING =================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)



# ================= STARTUP =================


async def startup(app):

    logger.info(
        "Starting Aira..."
    )


    # Database memory AI

    await init_aira_db()


    # Database scheduler

    await init_scheduler_db()


    logger.info(
        "Database ready"
    )


    # Scheduler reminder

    app.job_queue.run_repeating(
        send_reconnect_messages,
        interval=21600, # 6 jam
        first=60
    )


    logger.info(
        "Scheduler aktif"
    )



# ================= MAIN =================


def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN belum ada di .env"
        )


    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(startup)
        .build()
    )


    # Register modules

    register_start(app)

    register_aira(app)


    logger.info(
        "Aira online 🤖"
    )


    app.run_polling(
        allowed_updates=[
            "message",
            "callback_query"
        ]
    )



if __name__ == "__main__":

    main()
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ContextTypes,
    CommandHandler
)

BOT_USERNAME = "aira_aichatbot"


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    keyboard = [
        [
            InlineKeyboardButton(
                "➕ Tambahkan Aira ke Grup",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Coba Tanya Aira",
                callback_data="try_ai"
            )
        ],
        [
            InlineKeyboardButton(
                "👨‍💻 Developer",
                url="https://instagram.com/ryu_autoworks"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"""
Halo {user.first_name} 👋✨

Aku **Aira** 🤖
Asisten AI yang siap membantu kamu dalam berbagai hal.

Aku bisa membantu:
• 💡 Menjawab pertanyaan
• 📚 Menjelaskan konsep sulit
• 💻 Membantu coding
• 🧠 Mencari ide dan berdiskusi
• 🌎 Membantu belajar hal baru

━━━━━━━━━━━━━━

💬 Cara menggunakan Aira:

**Chat pribadi**
Langsung kirim pertanyaan apa saja.

**Di grup**
Tambahkan Aira ke grup, lalu panggil:

`Aira jelaskan apa itu AI`

atau reply pesan Aira untuk melanjutkan percakapan.

━━━━━━━━━━━━━━

Aku dikembangkan di Indonesia 🇮🇩
oleh Ryu.

Selamat berdiskusi bersama Aira 🤖✨
"""

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


def register_handlers(app):

    app.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )
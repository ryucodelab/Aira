<div align="center">

<img src="https://cdn.theorg.com/253b05ad-3826-4108-971c-38774fd9a90e_medium.jpg" width="100%" />

# 🤖 Aira AI

### Your intelligent Telegram AI assistant powered by LLM technology.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0.svg)](https://telegram.org/)
[![OpenRouter](https://img.shields.io/badge/AI-OpenRouter-purple.svg)](https://openrouter.ai/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## ✨ About Aira

**Aira** is an open-source AI assistant built for Telegram.

Aira is designed to provide natural conversations, intelligent answers, and helpful assistance through Large Language Models (LLM).

Unlike traditional command-based bots, Aira focuses on creating a more natural AI experience with:

- 🧠 User-based memory
- 💬 Natural conversations
- 🤖 AI personality system
- 🗄️ PostgreSQL powered context storage
- 🔔 Smart user re-engagement
- 👥 Group mention support

---

## 🚀 Features

### 🤖 AI Conversation

Talk with Aira naturally in private chat.

Example:

```
What is artificial intelligence?
```

Aira will answer with contextual and human-friendly responses.

---

### 🧠 User Memory

Aira stores conversation context per user.

This allows Aira to remember previous topics and provide better follow-up answers.

Example:

```
User:
I want to learn Python

Aira:
Great! Let's start from the basics.

(User returns later)

User:
Continue from before

Aira:
Let's continue learning Python...
```

---

### 👥 Group Assistant Mode

Aira avoids disturbing conversations.

In groups, call Aira manually:

```
Aira explain what is Linux kernel
```

or reply to Aira's message to continue the conversation.

---

### 🔔 Smart Reminder

Aira can greet users who haven't interacted for a while.

Example:

> "Hi 👋 It's been a few days since we last talked. Is there anything you want to discuss with Aira today?"

---

## 🏗️ Architecture

```
Telegram User
      |
      v
Telegram Bot API
      |
      v
Aira Core
      |
      +---- OpenRouter LLM
      |
      +---- PostgreSQL Memory
      |
      +---- Telegram Formatter
      |
      v
AI Response
```

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/ryucodelab/Aira.git

cd Aira
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token

OPENROUTER_KEY=your_openrouter_api_key

CURRENT_MODEL=openai/gpt-4o-mini

POSTGRESQL_URI=your_postgresql_connection

BOT_NAME=Aira

SITE_URL=https://t.me/your_bot_username
```

---

## ▶️ Running Aira

Start the bot:

```bash
python main.py
```

Expected output:

```
INFO Starting Aira...
INFO Database ready
INFO Scheduler active
INFO Aira online 🤖
```

---

## 🗂️ Project Structure

```
Aira/
│
├── main.py
├── requirements.txt
├── .env.example
├── LICENSE
│
└── modules/
    ├── start.py
    ├── aira.py
    └── scheduler.py
```

---

## 🛠️ Tech Stack

| Technology | Usage |
|-|-|
| Python | Core language |
| python-telegram-bot | Telegram framework |
| OpenRouter | AI model gateway |
| PostgreSQL | User memory storage |
| AsyncPG | Async database driver |
| HTTPX | Async HTTP client |

---

## 🤝 Contributing

Contributions are welcome!

Steps:

1. Fork this repository
2. Create your feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push and create Pull Request

---

## 📜 License

This project is licensed under the MIT License.

You are free to:

- Use
- Modify
- Distribute
- Create derivatives

See the full license in:

```
LICENSE
```

---

## 👨‍💻 Developer

Created with ❤️ in Indonesia 🇮🇩

**Ryu**

Instagram:
[@ryu_autoworks](https://instagram.com/ryu_autoworks)

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.

Every star helps the project grow.

---

<div align="center">

Made in Indonesia 🇮🇩  
Powered by Claude 🤖

</div>

# RSS Feeder News Bot

A Telegram bot that aggregates news from multiple media outlets using RSS feeds.

Instead of opening several news websites, users can browse articles from different agencies and departments in one place. The bot presents the latest headlines and provides direct links to the original articles.

Built with Python, aiogram 3, and feedparser.

## Features

- Dynamic navigation generated from the configured RSS feeds
- Support for multiple news agencies
- Department selection (Technology, Politics, World, etc.)
- Inline keyboards for fast navigation
- Fetches the latest articles directly from RSS feeds
- Easy to extend by adding new feeds to a single configuration file

## How it works

The entire project is driven by `feeds.py`.

Each RSS feed is registered once with its news agency and department. The bot automatically:

- Generates the list of available news agencies
- Generates department menus
- Generates a list of latest news titles
- Fetches the requested RSS feed
- Displays the latest articles with links to the original publication

Adding support for a new news source usually only requires adding its RSS feeds to `feeds.py`.

## Tech Stack

- Python 3
- aiogram 3
- feedparser

## Installation

Clone the repository:

```bash
git clone https://github.com/charliesbox/rss-feeder-news-bot.git
cd rss-feeder-news-bot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root.

```env
BOT_TOKEN=your_telegram_bot_token
PROXY_URL=http://your_proxy:port
```

### Environment variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Telegram Bot API token obtained from @BotFather |
| `PROXY_URL` | SOCKS5 or HTTP(S) proxy used for connecting to Telegram. Leave empty if you don't need a proxy. |

Run the bot:

```bash
python main.py
```


## Roadmap

- Add more news agencies
- Save favorite articles
- Improve article formatting
- Optional article translation
- Cache RSS feeds in a database
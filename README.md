# RSS Feeder News Bot

A Telegram bot that aggregates news from multiple media outlets using RSS feeds.

Instead of opening several news websites, users can browse articles from different agencies and departments in one place. The bot presents the latest headlines and provides direct links to the original articles.

Built with Python, aiogram 3, PostgreSQL, psycopg 3 and feedparser.

## Features

- Dynamic navigation generated from the configured RSS feeds
- Support for multiple news agencies
- Department selection (Technology, Politics, World, etc.)
- Inline keyboards for fast navigation
- Fetches the latest articles from a local PostgreSQL database
- Automatically updates the database every 30 minutes 
- Easy to extend by adding new feeds to a single configuration file

## How it works

The rssfeeds are configured in `feeds.py`.

Each RSS feed is registered once with its news agency and department, like this:

```python
url_agency_number = ('Department name', 'https://example.com')
```

The bot automatically:

- Parses all configured rssfeeds and stores the latest news in a PostgreSQL database
- Generates the list of available news agencies
- Generates department menus
- Fetches a list of latest news titles from the database
- Displays the latest articles with links to the original publication

Adding support for a new news source usually only requires adding its RSS feeds to `feeds.py`.

## Tech Stack

- Python 3
- aiogram 3
- feedparser
- psycopg 3

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
db_password=your_database_password
```
### Setting a database

The bot uses a local PostgreSQL database as a news storage. 
It currently uses:

host = localhost
port = 5432
database = postgres
user = postgres

the password is stored in `.env` file

### Environment variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Telegram Bot API token obtained from @BotFather |
| `PROXY_URL` | SOCKS5 or HTTP(S) proxy used for connecting to Telegram. Leave empty if you don't need a proxy |
| `db_password` | Your database password |

Run the bot:

```bash
python main.py
```


## Future features

- Add more news agencies
- English interface support
- Save favorite articles
- Improve article formatting
- Optional article translation

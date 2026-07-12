import feedparser, asyncio

url = 'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml'
file_directory = r"D:\.vault\.projects\rss-news\Technology.xml"
newsfeed = feedparser.parse(file_directory)


def parse_names():
    news_titles = []
    for news in range(5):
        news_titles.append(newsfeed.entries[news].title)
    return news_titles

def fetch_news(broadcaster, number):
    news = f'{newsfeed.entries[number].title}\n{newsfeed.entries[number].description}\n\
{newsfeed.entries[number].published}\n\n{newsfeed.entries[number].link}'
    return news
import feedparser, asyncio
import feeds


def parse_agencies():
    agencies = []
    for agency in dir(feeds):
        if agency.startswith('url_'):
            if agency.split('_')[1] in agencies:
                pass
            else:
                agencies.append(agency.split('_')[1])
    return agencies


def parse_departments(agency):
    deps = []
    for feed in dir(feeds):
        if feed.startswith(f'url_{agency}'):
            deps.append(getattr(feeds, feed)[0])
    return deps
        

def parse_titles(agency, number):
    newsfeed = feedparser.parse(getattr(feeds, f'url_{agency}_{number}')[1])
    news_titles = []
    for news in newsfeed.entries[0:999]:
        # this if-else is made for some bbc articles, as their titles might contain unclear info
        if news.title.lower() == 'tech life' or news.title.lower() == 'tech now':
            news_titles.append(news.description)
        else:
            news_titles.append(news.title)
    return news_titles


def fetch_news(agency, number, index):
    newsfeed = feedparser.parse(getattr(feeds, f'url_{agency}_{number}')[1])
    newstext = (
        f'{newsfeed.entries[index].title}\n\n'
        f'{newsfeed.entries[index].description}\n\n'
        f'Опубликовано: {newsfeed.entries[index].published}\n'
        f'Читать на {agency.upper()}: {newsfeed.entries[index].link}'
    )
    return(newstext)
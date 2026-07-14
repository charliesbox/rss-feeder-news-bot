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
            newsfeed = feedparser.parse(getattr(feeds, feed))
            if agency == 'bbc':
                deps.append(newsfeed.feed.description)
            else:
                deps.append(newsfeed.feed.title)
        else:
            pass
    return deps
        

def parse_titles(agency, number):
    newsfeed = feedparser.parse(getattr(feeds, f'url_{agency}_{number}'))
    news_titles = []
    for news in newsfeed.entries[0:20]:
        news_titles.append(news.title)
    return news_titles


def fetch_news(agency, number, index):
    newsfeed = feedparser.parse(getattr(feeds, f'url_{agency}_{number}'))
    newstext = (
        f'{newsfeed.entries[index].title}\n\n'
        f'{newsfeed.entries[index].description}\n\n'
        f'Опубликовано: {newsfeed.entries[index].published}\n'
        f'Читать на {agency.upper()}: {newsfeed.entries[index].link}'
    )
    return(newstext)
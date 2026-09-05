import psycopg, feedparser, feeds, os, requests
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
    host = 'localhost',
    dbname = 'postgres',
    user = 'postgres',
    password = os.getenv('DB_PASSWORD'),
    port = 5432
)

proxy = os.getenv('PROXY_URL')


def save_data(agency, department, title, description, pub_date, link):
    with connection.cursor() as cursor:
        query_check = """
            SELECT EXISTS (SELECT 1 FROM news WHERE title=%s)
        """
        cursor.execute(query_check, (title,))
        row = cursor.fetchone()
        exists = row[0]

        if not exists:
            query_insert = """
                INSERT INTO news (agency, department, title, description, pub_date, url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert, (agency, department, title, description, pub_date, link))
            connection.commit()


def prepare_data():
    for feed in dir(feeds):
        if feed.startswith('url_'):
            agency = feed.split('_')[1]
            department, url = getattr(feeds, feed)

            print(f'parsing {agency} {department}')
            print(f'url: {url}')

            if proxy:
                request = requests.get(
                    url,
                    proxies={
                        'http': proxy,
                        'https': proxy
                    },
                    timeout=30
                )

                newsfeed = feedparser.parse(request.content)
            else:
                newsfeed = feedparser.parse(url)

            print(f'parsed {department}, entries: {len(newsfeed.entries)}\n')

            for item in newsfeed.entries:
                title = item.title
                description = item.description
                pub_date = item.published
                link = item.link

                save_data(agency, department, title, description, pub_date, link)

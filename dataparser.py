import psycopg, feedparser, feeds, os
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
    host = 'localhost',
    dbname = 'postgres',
    user = 'postgres',
    password = os.getenv('db_password'),
    port = 5432

)

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

            newsfeed = feedparser.parse(url)

            for index, item in enumerate(newsfeed.entries):
                title = newsfeed.entries[index].title
                description = newsfeed.entries[index].description
                pub_date = newsfeed.entries[index].published
                link = newsfeed.entries[index].link

                save_data(agency, department, title, description, pub_date, link)
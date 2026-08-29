import asyncio, psycopg, feeds, os
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
    host = 'localhost',
    dbname = 'postgres',
    user = 'postgres',
    password = os.getenv('DB_PASSWORD'),
    port = 5432
)


# PARSING LAST 10 ARTICLES
def parse_latest():
    with connection.cursor() as cursor:
        parse_latest_query = """
            SELECT id, title, description, agency, department FROM news ORDER BY pub_date DESC LIMIT 10
        """
        cursor.execute(parse_latest_query, ())

        latest_10 = cursor.fetchall()
        return latest_10

    
# PARSING AGENCY NAMES FROM FEEDS.PY
def parse_agencies():
    agencies = []

    for agency in dir(feeds):
        if agency.startswith('url_'):
            if agency.split('_')[1] in agencies:
                pass
            else:
                agencies.append(agency.split('_')[1])
    
    return agencies


# PARSING DEPARTMENT NAMES FROM FEEDS.PY
def parse_departments(agency):
    deps = []

    for feed in dir(feeds):
        if feed.startswith(f'url_{agency}'):
            deps.append(getattr(feeds, feed)[0])
    
    return deps
        

# FETCHING TITLES FROM DB
def parse_titles(agency, number, limit, offset):
    department = getattr(feeds, f'url_{agency}_{number}')[0]
    with connection.cursor() as cursor:
        query = """
            SELECT id, title FROM news WHERE agency = %s AND department = %s ORDER BY pub_date DESC LIMIT %s OFFSET %s
        """
        cursor.execute(query, (agency, department, limit, offset))

        titles = cursor.fetchall()
        return titles


# FETCHING NEWS BY ITS ID FROM DB
def fetch_news(agency, news_id):
    with connection.cursor(row_factory=dict_row) as cursor:
        news_query = """
            SELECT title, description, pub_date, url FROM news WHERE id = %s
        """
        cursor.execute(news_query, (news_id,))

        rows = cursor.fetchall()
        row = rows[0]

    newstext = (
        f'{row['title']}\n\n'
        f'{row['description']}\n\n'
        f'Опубликовано: {row['pub_date']}\n'
        f'Читать на {agency.upper()}: {row['url']}'
    )

    return newstext
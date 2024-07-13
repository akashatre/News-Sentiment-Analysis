import pymysql
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import feedparser

class RSSFeedScraper:
    def __init__(self, db_config):
        self.conn = pymysql.connect(**db_config)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS RSS_Feed_Info (
                News_URL VARCHAR(255),
                RSS_Feed_Topic VARCHAR(255),
                RSS_Topic_Url VARCHAR(255),
                Active_Flag INT,
                Updated_Time_Stamp DATE
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS News_Info (
                Rss_topic VARCHAR(255),
                rss_topic_url VARCHAR(255),
                News_Url VARCHAR(1000),
                Title VARCHAR(1000),
                Description VARCHAR(10000),
                publish_date VARCHAR(255)
            )
        ''')
        self.conn.commit()

    def scrape_rss_feeds(self):
        self.cur.execute("SELECT news_url FROM business WHERE active_flag = 1")
        active_news_urls = self.cur.fetchall()
        for row in active_news_urls:
            news_url = row['news_url']
            rss_url = f"{news_url}rss.cms"
            date_to_insert = datetime.now().date()

            response = requests.get(rss_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            links = soup.find_all('a')
            rss_feeds = {}

            for link in links:
                href = link.get('href')
                if href and "http://" in href and "/rss" in href:
                    topic = link.text.strip()
                    rss_feeds[topic] = href

            for topic, rss_topic_url in rss_feeds.items():
                self.cur.execute('''
                    INSERT INTO RSS_Feed_Info (News_URL, RSS_Feed_Topic, RSS_Topic_Url, Active_Flag, Updated_Time_Stamp)
                    VALUES (%s, %s, %s, 2, %s)
                ''', (news_url, topic, rss_topic_url, date_to_insert))
                self.conn.commit()

                feed = feedparser.parse(rss_topic_url)
                for entry in feed.entries:
                    summary = entry.summary
                    soup = BeautifulSoup(summary, 'html.parser')
                    clean_summary = soup.get_text()

                    self.cur.execute('''
                        INSERT INTO News_Info (Rss_topic, rss_topic_url, News_Url, Title, Description, publish_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (topic, rss_topic_url, entry.link, entry.title, clean_summary, entry.published))
                    self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

# Configuration details
db_config = {
    'host': 'database-1.cl2kmkc8ogep.ap-south-1.rds.amazonaws.com',
    'user': 'admin1',
    'password': 'akashatre',
    'database': 'mydb1',
    'cursorclass': pymysql.cursors.DictCursor
}

def lambda_handler(event, context):
    rss_scraper = RSSFeedScraper(db_config)
    try:
        rss_scraper.create_tables()
        rss_scraper.scrape_rss_feeds()
    finally:
        rss_scraper.close_connection()

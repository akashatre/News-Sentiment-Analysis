import json
import pymysql
import boto3


class NewsSentimentAnalyzer:
    def __init__(self, db_config):
        self.conn = pymysql.connect(**db_config)
        self.comprehend = boto3.client('comprehend')

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS News_Sentiment (
                News_Topic VARCHAR (300),
                News_Title VARCHAR(1000),
                News_Description VARCHAR(10000),
                Sentiment VARCHAR(255),
                Sentiment_Positive FLOAT,
                Sentiment_Negative FLOAT,
                Sentiment_Neutral FLOAT,
                Sentiment_Mixed FLOAT
            )
        ''')
        self.conn.commit()

    def analyze_sentiment_and_insert(self):
        cur = self.conn.cursor()
        cur.execute("SELECT Rss_topic, Title, Description FROM News_Info")
        news_data = cur.fetchall()

        for news_item in news_data:
            topic = news_item['Rss_topic']
            title = news_item['Title']
            description = news_item['Description']

            if description:
                sentiment_response = self.comprehend.detect_sentiment(
                    Text=description,
                    LanguageCode='en'
                )

                sentiment = sentiment_response['Sentiment']
                sentiment_scores = sentiment_response['SentimentScore']
                positive = sentiment_scores['Positive']
                negative = sentiment_scores['Negative']
                neutral = sentiment_scores['Neutral']
                mixed = sentiment_scores['Mixed']

                cur.execute('''
                    INSERT INTO News_Sentiment 
                    (News_Topic , News_Title, News_Description, Sentiment, Sentiment_Positive, Sentiment_Negative, Sentiment_Neutral, Sentiment_Mixed)
                    VALUES (%s,%s, %s, %s, %s, %s, %s, %s)
                ''', (topic, title, description, sentiment, positive, negative, neutral, mixed))

                self.conn.commit()

    def close_connection(self):
        self.conn.close()


db_config = {
    'host': 'database-1.cl2kmkc8ogep.ap-south-1.rds.amazonaws.com',
    'user': 'admin1',
    'password': 'akashatre',
    'database': 'mydb1',
    'cursorclass': pymysql.cursors.DictCursor
}


def lambda_handler(event, context):
    news_sentiment_analyzer = NewsSentimentAnalyzer(db_config)
    try:
        news_sentiment_analyzer.create_table()
        news_sentiment_analyzer.analyze_sentiment_and_insert()
    finally:
        news_sentiment_analyzer.close_connection()

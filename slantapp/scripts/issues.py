from collections import Counter
import datetime
# import en_core_web_sm
import os
import psycopg2
# import spacy
# from slantapp.models import Article

def run():

    # Environment variables
    SLNT_DB_NAME = os.environ.get('SLNT_DB_NAME')
    SLNT_DB_USER = os.environ.get('SLNT_DB_USER')
    SLNT_DB_PASSWORD = os.environ.get('SLNT_DB_PASSWORD')

    # Establish connection
    conn = psycopg2.connect(
        host='ec2-54-163-240-54.compute-1.amazonaws.com',
        dbname=SLNT_DB_NAME,
        user=SLNT_DB_USER,
        password=SLNT_DB_PASSWORD,
        sslmode='require'
    )
    cursor = conn.cursor()

    # Get article text
    today = datetime.date.today()
    cursor.execute("""
        SELECT topic_keywords
        FROM slantapp_article
        WHERE
            topic_keywords IS NOT NULL
            AND scrape_date > current_date - interval '1' day
        ;
        """)
    data = cursor.fetchall()

    aggregated_topics = []
    num_results = 50

    list_of_list_of_topics = [eval(item[0]) for item in data]
    for list_of_topics in list_of_list_of_topics:
        for topic in list_of_topics:
            for i in range(0,topic[1]):
                aggregated_topics.append(topic[0])

    aggregated_topics_most_common = Counter(aggregated_topics).most_common(num_results)

    for topic in aggregated_topics_most_common:
        print(topic)

    conn.close()

run()
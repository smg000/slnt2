from collections import Counter
import datetime
# import en_core_web_sm
import os
import psycopg2
import re
# import spacy
# from slantapp.models import Article

def run():

    # Environment variables
    slnt_db_host = os.environ.get('SLNT_DB_HOST')
    slnt_db_name = os.environ.get('SLNT_DB_NAME')
    slnt_db_user = os.environ.get('SLNT_DB_USER')
    slnt_db_password = os.environ.get('SLNT_DB_PASSWORD')

    # Establish connection
    conn = psycopg2.connect(
        host=slnt_db_host,
        dbname=slnt_db_name,
        user=slnt_db_user,
        password=slnt_db_password,
        sslmode='require'
    )
    cursor = conn.cursor()

    # Get article text
    cursor.execute("""
        SELECT topic_keywords
        FROM slantapp_article
        WHERE
            topic_keywords IS NOT NULL
            AND scrape_date >= CURRENT_DATE - 1
        ;
        """)
    data = cursor.fetchall()

    aggregated_topics = []
    num_results = 40

    pattern = "('[a-z\s\.'-]+',\s\d+)"
    regex = re.compile(pattern)

    for tuple in data:
        string = str(tuple) # Convert tuple to string
        list = regex.findall(string) # Find regex matches
        for item in list:
            item_list = item.split(',') # Split string into list
            topic = item_list[0][1:-1] # Get rid of single quotes
            frequency = int(item_list[1][1:]) # Convert string to integer
            for i in range(0, frequency):
                aggregated_topics.append(topic) # Add topic to list, frequency number of times

    aggregated_topics_most_common = Counter(aggregated_topics).most_common(num_results)
    aggregated_topics_most_common_sorted = sorted(aggregated_topics_most_common, key=lambda topic: topic[1], reverse=True)

    column_width = max([len(topic[0]) for topic in aggregated_topics_most_common])
    print('\n')
    print('#'.ljust (4) + 'KEYWORD'.ljust(column_width) + '\t' + 'COUNT')
    print('-' * (17 + column_width))
    counter = 1
    for topic in aggregated_topics_most_common_sorted:
        print(str(counter).ljust(4) + topic[0].ljust(column_width) + '\t' + str(topic[1]))
        counter += 1
    print('\n')

    conn.close()

run()
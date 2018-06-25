from collections import Counter
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
# import en_core_web_sm
import os
import psycopg2
import re
# import spacy
# from slantapp.models import Article
import sendgrid
from sendgrid.helpers.mail import *

class Command(BaseCommand):
    help = 'Sends daily email to MailChimp subscribers.'

    def add_arguments(self, parser):
        # parser.add_argument('--subject', type=str, required=True)
        pass

    def handle(self, *args, **options):

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
                AND scrape_timestamp >= CURRENT_DATE - 2
            ;
            """)
        data = cursor.fetchall()

        aggregated_topics = []
        article_count = Counter()
        num_results = 100

        pattern = "('[a-z\s\.'-]+',\s\d+)"
        regex = re.compile(pattern)

        for tuple in data:
            string = str(tuple) # Convert tuple to string
            list = regex.findall(string) # Find regex matches
            for item in list:
                item_list = item.split(',') # Split string into list
                topic = item_list[0][1:-1] # Get rid of single quotes
                article_count[topic] += 1
                frequency = int(item_list[1][1:]) # Convert string to integer
                for i in range(0, frequency):
                    aggregated_topics.append(topic) # Add topic to list, frequency number of times

        aggregated_topics_most_common = Counter(aggregated_topics).most_common(num_results)
        aggregated_topics_most_common_sorted = sorted(aggregated_topics_most_common, key=lambda topic: topic[1], reverse=True)

        column_width = max([len(topic[0]) for topic in aggregated_topics_most_common])
        print('\n')
        print('#'.ljust (4) + 'KEYWORD'.ljust(column_width) + '\t' + 'COUNT' + '\t' + 'ARTICLES')
        print('-' * (28 + column_width))
        counter = 1
        for topic in aggregated_topics_most_common_sorted:
            if topic[0] in article_count:
                print(str(counter).ljust(4) + topic[0].ljust(column_width) + '\t' + str(topic[1]) + '\t' + str(article_count[topic[0]]))
            counter += 1
        print('\n')

        # # Send email
        # sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        # from_email = Email("sean@theskeww.com", 'Sean @ the skeww')
        # to_email = Email("sean@theskeww.com")
        # subject = "Today's Issues |" + datetime.date.today().strftime("%B %d, %Y")
        # content = Content(render_to_string(aggregated_topics_most_common_sorted))
        # mail = Mail(from_email, subject, to_email, content)
        # response = sg.client.mail.send.post(request_body=mail.get())
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)

        conn.close()
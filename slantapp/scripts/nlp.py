from collections import Counter
import datetime
import os
import psycopg2
import spacy
from slantapp.models import Article

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
    cursor.execute("SELECT title, text, url FROM slantapp_article WHERE topic_keywords IS NULL LIMIT 5;")
    data = cursor.fetchall()

    # nlp = spacy.load('en')
    # Possible alternative
    nlp = en_core_web_sm.load()

    for title, text, url in data:

        print(title)

        doc = nlp(text)

        # Number of results
        num_results = 5

        # Initialize lists
        ents = []
        propns = []
        nouns = []
        combined = []

        # Entities
        for ent in doc.ents:
            ents.append(str(ent).lower())
            combined.append(str(ent).lower())
        topics_ent = Counter(ents).most_common(num_results)
        # print(topics_ent)

        # Proper nouns
        for token in doc:
            if token.pos_ == 'PROPN':
                propns.append(token.text.lower())
                combined.append(token.text.lower())

        topics_propn = Counter(propns).most_common(num_results)
        # print(topics_propn)

        # Nouns
        for token in doc:
            if token.pos_ == 'NOUN':
                nouns.append(token.text.lower())
                combined.append(token.text.lower())

        topics_noun = Counter(nouns).most_common(num_results)
        # print(topics_noun)

        # Combined
        topics_combined = Counter(combined).most_common(num_results)
        print(topics_combined)

        # Common
        common_set = (set(ents) & set(propns) & set(nouns))
        common_list = list(common_set)
        topics_common = Counter(common_list).most_common(num_results)
        # print(topics_common)

        article = Article.objects.get(url=url)
        article.topic_keywords = topics_combined
        article.save()

run()
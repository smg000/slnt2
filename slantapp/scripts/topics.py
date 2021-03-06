from collections import Counter
# import datetime
import en_core_web_sm
import os
import psycopg2
import spacy
from slantapp.models import Article

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
    cursor.execute("SELECT title, text, url FROM slantapp_article WHERE topic_keywords IS NULL;")
    data = cursor.fetchall()

    nlp = spacy.load('en_core_web_sm')

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

    conn.close()
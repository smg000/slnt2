from bs4 import BeautifulSoup
import csv
import datetime
import math
from newspaper import Article
import numpy
import os
import pandas
import psycopg2
import re
import requests
import scrapy
import spacy
import textblob
from urllib.request import urlopen

file_sites = '~/Desktop/SLNT/Python/sites.csv'
sites_db = pandas.read_csv(file_sites, header=None, keep_default_na=False)

def TBD(tbd):
    # Environment variables
    SLNT_DB_NAME = os.environ.get('SLNT_DB_NAME')
    SLNT_DB_USER = os.environ.get('SLNT_DB_USER')
    SLNT_DB_PASSWORD = os.environ.get('SLNT_DB_PASSWORD')

    # Establish connection
    conn = psycopg2.connect(host='ec2-54-163-240-54.compute-1.amazonaws.com', dbname=SLNT_DB_NAME, user=SLNT_DB_USER, password=SLNT_DB_PASSWORD, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM slantapp_article")
    records = cursor.fetchall()
    for record in records:
        print(record[1])

def get_links(sites_db):
    urls = []
    counter = 0
    datetime_stamp = datetime.datetime.now()
    datetime_stamp = datetime_stamp.strftime("%m-%d_%H-%M")
    date_stamp = datetime.datetime.now()
    date_stamp = date_stamp.strftime("%m-%d-%Y")
    for i in range(1, sites_db.shape[0]):
        # TODO name columns in dataframe
        site_id = sites_db.ix[i][0]
        site = sites_db.ix[i][3]
        print(site)
        keywords_include = sites_db.ix[i][4].split(',')
        keywords_exclude = sites_db.ix[i][5].split(',')
        url_prepend = sites_db.ix[i][6]
        try:
            webpage = urlopen(site)
            soup = BeautifulSoup(webpage, 'html5lib')
            site_urls = []

            # a_tags
            a_tags = soup.find_all('a')
            for a_tag in a_tags:
                a_tag = a_tag.get('href')
                if a_tag is not None and a_tag not in site_urls:
                    site_urls.append(a_tag)
            for site_url in site_urls:
                if any(keyword_include in site_url for keyword_include in keywords_include) and not any(keyword_exclude in site_url for keyword_exclude in keywords_exclude):
                    if site_url[0] == '/' and url_prepend != '':
                        site_url = url_prepend + site_url
                    urls.append([site_id, site_url, date_stamp])
        except:
            print("Unable to scrape articles from %s." % (sites_db.ix[i][1]))
            pass

    # Output file
    output_filename = 'urls_' + datetime_stamp + '.csv'
    with open(output_filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(urls)
    print('Success! Your URLs have been scraped!')

get_links(sites_db)

file_links = '~/PycharmProjects/slant/get_articles_folder/urls_04-19_08-45.csv'
urls = pandas.read_csv(file_links, header=None, keep_default_na=False)

def get_articles(urls):
    counter = 0
    for i in range(0, urls.shape[0]):
        url = urls.ix[i][1]
        article = Article(url)
        article.download()
        article.parse()

        title = article.title
        authors = article.authors
        publish_date = article.publish_date
        text = article.text

        urls.at[i, 3] = title
        urls.at[i, 4] = authors
        urls.at[i, 5] = publish_date
        urls.at[i, 6] = text

        counter += 1
        print(str(counter))
    urls.to_csv('test_file.csv', sep=',')

# get_articles(urls)

file_articles = '~/PycharmProjects/slant/get_articles_folder/test_file2.csv'
articles = pandas.read_csv(file_articles, encoding = "ISO-8859-1", header=None, keep_default_na=False)

def analyze_articles(articles):
    nlp = spacy.load("en")
    for i in range(1, articles.shape[0]):
        article = articles.iloc[i,7]
        article = nlp(article)
    #     topics = []
    #     for i, token in enumerate(article):
    #         if token.pos_ in ('NOUN', 'PNOUN'):
    #             topics.append([token.lemma_, 1])
    # topics_df = pandas.DataFrame.from_records(topics, columns=['topic', 'frequency'])
    # topics_df1 = topics_df.groupby(['topic']).sum()
    # topics_df2 = topics_df1.sort_values(by=['frequency'], ascending=False)
    # print(topics_df2.describe)

    for i, token in enumerate(article.ents):
        topics = []
        for ent in article.ents:
            topics.append([str(ent), 1])
        topics_df = pandas.DataFrame.from_records(topics, columns=['topic', 'frequency'])
        topics_df_grouped = topics_df.groupby(['topic']).sum()
        topics_df_grouped_sorted = topics_df_grouped .sort_values(by=['frequency'], ascending=False)
    print('Entities approach:')
    print(topics_df_grouped_sorted)


        # Get nouns, proper nouns
        # for i, token in enumerate(article):
        #     if token.pos_ in ('NOUN', 'PNOUN' ):
        #         for child in token.children:
        #             if child.pos_ in ('ADJ', 'VERB', 'ADV'):
        #                 print([token.lemma_, child.text, child.pos_])
        #
        # for sent in article.sents:
        #     print(sent)

        # for i, token in enumerate(article):
        #     if token.pos_ == 'PROPN':
        #         print([token.text, token.pos_])
        #
        # for i, token in enumerate(article):
        #     if token.pos_ == 'PROPN':
        #         print([token.text, token.pos_])

        # for i, token in enumerate(article.noun_chunks):
        #     children = []
        #     for chunk in article.noun_chunks:
        #         print(chunk)





    #     for i, token in enumerate(article):
    #         if token.pos_ not in ('NOUN', 'PROPN'):
    #             continue
    #         for j in range(i+1, len(article)):
    #             if article[j].pos_ == 'ADJ':
    #                 noun_adj_pairs.append((token, article[j]))
    # for pair in noun_adj_pairs:
    #     print(pair)


# noun_adj_pairs = []
# for i,token in enumerate(doc):
#     if token.pos_ not in ('NOUN','PROPN'):
#         continue
#     for j in range(i+1,len(doc)):
#         if doc[j].pos_ == 'ADJ':
#             noun_adj_pairs.append((token,doc[j]))
#             # break
# print(noun_adj_pairs)

# analyze_articles(articles)

# for i in range(1, articles.shape[0]):
#     article = articles.ix[i][7]
#     article = nlp(original_text)
#     entities =[]
#     for ent in article.ents:
#         entities.append(ent.text)
#         print(ent)


# nlp = spacy.load('en')
# doc = nlp(u'Mark and John are sincere employees at Google.')
# noun_adj_pairs = []
# for i,token in enumerate(doc):
#     if token.pos_ not in ('NOUN','PROPN'):
#         continue
#     for j in range(i+1,len(doc)):
#         if doc[j].pos_ == 'ADJ':
#             noun_adj_pairs.append((token,doc[j]))
#             # break
# print(noun_adj_pairs)
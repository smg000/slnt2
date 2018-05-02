from bs4 import BeautifulSoup
import csv
import datetime
import math
from newspaper import Article as n_Article # To avoid ambiguity with slantapp.models.Article
import numpy
import os
import pandas
import psycopg2
import re
import requests
import scrapy
import spacy
import textblob
import time
from urllib.request import urlopen
from slantapp.models import Article, Publication


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

    # Fetch sites to be scraped
    cursor.execute("SELECT publication_name, url_full, url_keys_include, url_keys_exclude, url_prepend FROM slantapp_publication WHERE publication_name='Politico' AND scrape=TRUE")
    publications = cursor.fetchall()

    # Fetch existing urls
    cursor.execute("SELECT url FROM slantapp_article")
    article_urls = cursor.fetchall()

    urls = []

    for publication in publications:
        publication_name = publication[0]
        publication_name_fk = Publication.objects.get(publication_name=publication_name)
        url_full = publication[1]
        keywords_include = publication[2].split(',')
        keywords_exclude = publication[3].split(',')
        url_prepend = publication[4]

        try:
            webpage = urlopen(url_full)
            soup = BeautifulSoup(webpage, 'html5lib')
            site_urls = []
            a_tags = soup.find_all('a')

            for a_tag in a_tags:
                href = a_tag.get('href')
                if href is not None and href not in site_urls:
                    site_urls.append(href)
            print("Scraping articles from: %s." % publication_name)

        except:
            print("Unable to scrape articles from: %s." % publication_name)
            pass

        for site_url in site_urls:
            if any(keyword_include in site_url for keyword_include in keywords_include) and not any(keyword_exclude in site_url for keyword_exclude in keywords_exclude):
                if site_url[0] == '/' and url_prepend not in ('', None):
                    site_url = url_prepend + site_url

                if site_url not in article_urls:
                    try:
                        # Parse article
                        article = n_Article(site_url)
                        article.download()
                        article.parse()

                        # Extract data
                        title = article.title
                        authors = article.authors
                        publish_date = article.publish_date
                        text = article.text

                        # Create instance of Article class
                        a = Article(
                            publication_name=publication_name_fk,
                            title=title,
                            byline=authors,
                            date=publish_date,
                            url=site_url,
                            text=text,
                            scrape_date=datetime.date.today(),
                            bias=50,
                            display=False,
                        )
                        print(a.date)
                        print(type(a.date))
                        # Write to database
                        # a.save()
                        # print("Got text for %s." % title)
                        # print(a)
                    except:
                        pass
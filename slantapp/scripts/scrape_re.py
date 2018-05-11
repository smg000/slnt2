from bs4 import BeautifulSoup
import datetime
from newspaper import Article as n_Article  # To avoid ambiguity with slantapp.models.Article
import os
import psycopg2
import re
from urllib.request import Request
from urllib.request import urlopen
from slantapp.models import Article, Publication


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

    # Fetch sites to be scraped
    cursor.execute("""
        SELECT publication_name, url_full, regex, url_blacklist, prepend, url_prepend
        FROM slantapp_publication
        WHERE scrape = TRUE
        ;
        """)
    publications = cursor.fetchall()

    # Fetch existing urls
    # TODO Restrict query to the last week to cut down query runtime
    cursor.execute("SELECT url FROM slantapp_article;")
    article_urls = [item[0] for item in cursor.fetchall()]

    counter = 0

    for publication in publications:

        publication_name = publication[0]
        publication_name_fk = Publication.objects.get(publication_name=publication_name)
        url_full = publication[1]
        regex = publication[2]
        url_blacklist = publication[3]
        prepend = publication[4]
        url_prepend = publication[5]

        urls = []

        try:
            # More robust
            req = Request(url_full, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'html5lib')  # Possible parsers: html5lib, lxml
            print('Used Request to scrape %s.' % (url_full))

            # TODO Refactor to remove repetitive code
            a_tags = soup.find_all('a')
            for a_tag in a_tags:
                url = str(a_tag.get('href'))
                if re.match(regex, url) and url not in url_blacklist and url not in article_urls:
                    if prepend is True:
                        url = url_prepend + url
                    urls.append(url)
        except:
            try:
                # Less robust
                webpage = urlopen(url_full)
                soup = BeautifulSoup(webpage, 'html5lib')
                print('Used urlopen to scrape %s.' % (url_full))

                a_tags = soup.find_all('a')
                for a_tag in a_tags:
                    url = str(a_tag.get('href'))
                    if re.match(regex, url) and url not in url_blacklist and url not in article_urls:
                        if prepend is True:
                            url = url_prepend + url
                        urls.append(url)
            except:
                print("Unable to scrape articles from: %s." % publication_name)
                pass

        urls_unique = list(set(urls))

        print(publication)
        print("Scraped %d articles." % (len(urls)))

        for url in urls_unique:

            # try:
            # Parse article
            article = n_Article(url)
            article.download()
            article.parse()

            # Extract data
            title = article.title
            authors = article.authors
            if article.publish_date == '':
                publish_date = datetime.date.today()
            else:
                publish_date = article.publish_date
            text = article.text

            # Create instance of Article class
            a = Article(
                publication_name=publication_name_fk,
                title=title,
                byline=authors,
                date=publish_date,
                url=url,
                text=text,
                scrape_date=datetime.date.today(),
                bias=50,
                display=False,
            )

            # Write to database
            a.save()
            counter += 1
            print("Committed article: %s..." % title[:40])
            # except:
            #     pass

    print("Committed %d articles." % (counter))

    conn.close()
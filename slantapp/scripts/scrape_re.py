from bs4 import BeautifulSoup
import datetime
from newspaper import Article as n_Article # To avoid ambiguity with slantapp.models.Article
import os
import psycopg2
import re
from urllib.request import Request
from urllib.request import urlopen
from slantapp.models import Article, Publication

def run():

    # Environment variables
    SLNT_DB_HOST = os.environ.get('SLNT_DB_HOST')
    SLNT_DB_NAME = os.environ.get('SLNT_DB_NAME')
    SLNT_DB_USER = os.environ.get('SLNT_DB_USER')
    SLNT_DB_PASSWORD = os.environ.get('SLNT_DB_PASSWORD')

    # Establish connection
    conn = psycopg2.connect(
        host=SLNT_DB_HOST,
        dbname=SLNT_DB_NAME,
        user=SLNT_DB_USER,
        password=SLNT_DB_PASSWORD,
        sslmode='require'
    )
    cursor = conn.cursor()

    # Fetch sites to be scraped
    cursor.execute("SELECT publication_name, url_full, url_keys_include, url_keys_exclude, url_prepend FROM slantapp_publication WHERE scrape=TRUE;")
    publications = cursor.fetchall()

    # Fetch existing urls
    cursor.execute("SELECT url FROM slantapp_article;")
    article_urls = [item[0] for item in cursor.fetchall()]

    urls = []
    counter = 0

    for publication in publications:
        publication_name = publication[0]
        publication_name_fk = Publication.objects.get(publication_name=publication_name)
        url_full = publication[1]
        # keywords_include = publication[2].split(',')
        # keywords_exclude = publication[3].split(',')
        # prepend =
        url_prepend = publication[4]
        pattern = regex[0]
        # url_blacklist =

        print(publication)

        """

        try:

            try:

                # More robust
                req = Request(url_full, headers={'User-Agent': 'Mozilla/5.0'})
                webpage = urlopen(req).read()
                soup = BeautifulSoup(webpage, 'html5lib') # Possible parsers: html5lib, lxml
                print('Used Request to scrape %s.' % (url_full))

            except:

                # Less robust
                webpage = urlopen(url_full)
                soup = BeautifulSoup(webpage, 'html5lib')
                print('Used urlopen to scrape %s.' % (url_full))

        a_tags = soup.find_all('a')

        #TODO Add URL_BLACKLIST
        for a_tag in a_tags:
            url = str(a_tag.get('href'))
            if re.match(pattern, url) and url not in url_blacklist and url not in urls:
                if prepend == True:
                    url = url_prepend + url
                urls.append(url)
                counter += 1

        except:

            print("Unable to scrape articles from: %s." % publication_name)
            pass

        # Remove duplicates, which should not be there anyway.
        site_urls = list(set(site_urls))

        for site_url in site_urls:
            if any(keyword_include in site_url for keyword_include in keywords_include) and not any(keyword_exclude in site_url for keyword_exclude in keywords_exclude):
                if len(site_url) > 0 and site_url[0] == '/' and url_prepend not in ('', None):
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
                            url=site_url,
                            text=text,
                            scrape_date=datetime.date.today(),
                            bias=50,
                            display=False,
                        )

                        # Write to database
                        a.save()
                        counter += 1
                        print("Committed article: %s..." % title[:40])
                    except:
                        pass
    print("Committed %d articles." % (counter))

    """

    conn.close()
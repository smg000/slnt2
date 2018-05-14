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
        WHERE scrape = TRUE and id in (15)
        ;
        """)
    publications = cursor.fetchall()

    article_counter = 0
    unable_to_scrape_counter = 0

    for publication in publications:

        publication_name = publication[0]
        publication_name_fk = Publication.objects.get(publication_name=publication_name)
        url_full = publication[1]
        regex = publication[2]
        url_blacklist = publication[3]
        prepend = publication[4]
        url_prepend = publication[5]
        # print("\n")
        # print(publication_name)
        # print("-" * len(publication_name))

        print(url_blacklist)
        print(type(url_blacklist))

        # Fetch existing urls
        cursor.execute("""
            SELECT url
            FROM slantapp_article a
            JOIN slantapp_publication p on a.publication_name_id = p.id
            WHERE p.publication_name = '{0}'
            ;
            """.format(publication_name))
        article_urls = sorted([item[0] for item in cursor.fetchall()])

        # Print articles
        print("URLs already in database")
        print(len(article_urls))
        for article in article_urls:
            print(article)

        urls = []

        try:
            # More robust
            req = Request(url_full, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'html5lib')  # Possible parsers: html5lib, lxml
            print('Used Request to scrape %s.' % (url_full))

            # TODO Refactor to remove repetitive code
            a_tags = soup.find_all('a')
            url_counter = 0
            for a_tag in a_tags:
                url = str(a_tag.get('href'))
                if re.match(regex, url) and url not in article_urls:
                    if prepend is True:
                        url = url_prepend + url
                    urls.append(url)
                    url_counter += 1
            print('Added %d urls to list of urls.' % (url_counter))
        except:
            try:
                # Less robust
                webpage = urlopen(url_full)
                soup = BeautifulSoup(webpage, 'html5lib')
                print('Used urlopen to scrape %s.' % (url_full))

                a_tags = soup.find_all('a')
                for a_tag in a_tags:
                    url = str(a_tag.get('href'))
                    if re.match(regex, url) and url not in article_urls:
                        if prepend is True:
                            url = url_prepend + url
                        urls.append(url)
                print('Added urls to url.')
            except:
                unable_to_scrape_counter += 1
                print("Unable to scrape articles from: %s." % publication_name)
                pass

        # try:
        print("URLs")
        print(len(urls))
        for url in sorted(urls):
            print(url)
        print("New URLs")
        new_urls = [url for url in urls if url not in sorted(article_urls)]
        print(len(new_urls))
        for new_url in new_urls:
            print(new_url)
        new_urls_unique = sorted(list(set(new_urls)))
        print(len(new_urls_unique))
        for url in new_urls_unique:
            print(url)


        print("Scraped %d articles from %s." % (len(new_urls_unique), publication_name))

        newspaper3k_counter = 0

        for url in new_urls_unique:

            # try:
            print("Trying #1.")
            # Parse article
            article = n_Article(url)
            article.download()
            article.parse()
            print("Parsed.")

            # Extract data
            article_title = article.title
            print(article_title[:40])
            article_byline = article.authors
            print(article_byline[:40])
            if article.publish_date == '':
                publish_date = datetime.date.today()
            else:
                publish_date = article.publish_date
            print(article_byline[:40])
            article_text = article.text
            print(article_text[:40])
            print("Extracted.")

            newspaper3k_counter += 1

            # Create instance of Article class
            # Article should be committed even if article.download() fails
            a = Article(
                publication_name=publication_name_fk,
                title=article_title,
                byline=article_byline,
                date=publish_date,
                url=url,
                text=article_text,
                scrape_date=datetime.date.today(),
                bias=50,
                display=False,
            )
            
            print("Created class.")

            # Write to database
            # a.save()
            print(a)
            print("Committed article: %s..." % (url))

            # except:
            #     print("Unable to save article.")
            #     continue

        print("Downloaded %d articles with Newspaper3k." % newspaper3k_counter)
        print("Committed %d articles for %s." % (article_counter, publication_name))
        #
        # except:
        #     print("Failed to generate a list of urls for %s." % (publication_name))
        #     continue

    # conn.close()

run()
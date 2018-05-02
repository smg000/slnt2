import datetime
import spacy

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
    cursor.execute("SELECT text FROM slantapp_article")
    publications = cursor.fetchall()

    # Fetch existing urls
    cursor.execute("SELECT url FROM slantapp_article")
    article_urls = [item[0] for item in cursor.fetchall()]
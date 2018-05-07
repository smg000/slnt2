import os
import psycopg2

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

    # Delete duplicate articles in database
    cursor.execute("""
        DELETE
        FROM slantapp_article
        WHERE id IN (
            SELECT id
            FROM ( 
                SELECT id,
		        ROW_NUMBER() OVER (
			        PARTITION BY url
			        ORDER BY  id) AS row_num
			        FROM slantapp_article) t
			        WHERE t.row_num > 1
			        )
        ;
    """)

    conn.close()
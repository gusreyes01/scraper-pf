import psycopg2

DB_NAME = 'scraper_pf'
DB_USER = 'scraper_pf'
DB_HOST = 'localhost'
DB_PWD = 'scraper_pf'


def get_connection():
    try:
        return psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (DB_NAME, DB_USER, DB_HOST, DB_PWD))
    except psycopg2.Error:
        print('Unable to connect to database')

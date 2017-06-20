import requests

from bs4 import BeautifulSoup
from db import get_connection
from scrapers.scraper import WebScraper, log_decorator


def get_sipres_results():
    r = requests.post('http://portal.condusef.gob.mx/SIPRES/jsp/pub/b_insincum_res.jsp', params={'tinc':1})
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find_all('td', {'class': 'contenidotexto'})

    conn = get_connection()
    cursor = conn.cursor()

    try:
        for row in rows:
            query = 'INSERT INTO sipres (institution) VALUES (%s);'
            cursor.execute(query, (row.text,))

        conn.commit()
    finally:
        conn.close()


class CondusefScraper(WebScraper):
    def __init__(self):
        super(CondusefScraper, self).__init__()
        self.agent_id = 2

    @log_decorator
    def execute(self, q=None):
        super(CondusefScraper, self).execute()

        query = "SELECT id, institution FROM sipres WHERE institution LIKE '%{}%';".format(q)
        self.cursor.execute(query)
        query_params = [(record[1], '', record[1], self.agent_id) for record in self.cursor]

        for params in query_params:
            self.cursor.execute('INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);', params)
            self.incr()

        self.conn.commit()


if __name__ == '__main__':
    # get_sipres_results()
    CondusefScraper().execute(q='Agrofina')

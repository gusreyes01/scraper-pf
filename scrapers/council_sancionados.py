import requests

from bs4 import BeautifulSoup
from db import get_connection
from scrapers.scraper import WebScraper, log_decorator


def get_sancionados():
    r = requests.get('https://scsanctions.un.org/consolidated/')
    soup = BeautifulSoup(r.text, 'html.parser')
    individuals = soup.find_all('table', {'id': 'sanctions'})[0]
    rows = individuals.find_all('tr')

    entities = soup.find_all('table', {'id': 'sanctions'})[1]
    rows2 = entities.find_all('tr')

    conn = get_connection()
    cursor = conn.cursor()

    try:
        for row in rows:
            url = ''
            if row.a:
                url = row.a.get('href')
            query = 'INSERT INTO council_sancionados (description, type, url) VALUES (%s, %s, %s);'
            cursor.execute(query, (row.text.strip(), 'individual', url))

        for row in rows2:
            url = ''
            if row.a:
                url = row.a.get('href')

            query = 'INSERT INTO council_sancionados (description, type, url) VALUES (%s, %s, %s);'
            cursor.execute(query, (row.text.strip(), 'entities', url))

        conn.commit()
    finally:
        conn.close()


class CouncilSancionadosScraper(WebScraper):
    def __init__(self):
        super(CouncilSancionadosScraper, self).__init__()
        self.agent_id = 15

    @log_decorator
    def execute(self, q=None):
        super(CouncilSancionadosScraper, self).execute()

        query = "SELECT id, description, url FROM council_sancionados WHERE description LIKE '%{}%';".format(q)
        self.cursor.execute(query)
        query_params = [(record[1][:255], record[2], record[1][:255], self.agent_id) for record in self.cursor]

        for params in query_params:
            self.cursor.execute('INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);', params)
            self.incr()

        self.conn.commit()


if __name__ == '__main__':
    CouncilSancionadosScraper().execute(q='DPRK Ministry of State')
    # get_sancionados()

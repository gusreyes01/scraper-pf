import requests

from bs4 import BeautifulSoup
from scrapers.scraper import WebScraper, log_decorator


class InaiScraper(WebScraper):
    def __init__(self):
        super(InaiScraper, self).__init__()
        self.agent_id = 10

    @log_decorator
    def execute(self, q=None):
        super(InaiScraper, self).execute()

        r = requests.get('http://portaltransparencia.gob.mx/buscador/search/search.do?query={}&idDependenciaZoom'
                         '=&method=search&siglasDependencia=&idFraccionZoom=&searchBy=1'.format(q))

        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.find_all('div', {'id': 'Box-info1'})

        for row in rows:
            spans = row.find_all('span')
            query = 'INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);'

            self.cursor.execute(query, (row.a.text, row.a.get('href'), spans[0].text + spans[1].text, self.agent_id))
            self.incr()

        self.conn.commit()


if __name__ == '__main__':
    InaiScraper().execute(q='juan perez')

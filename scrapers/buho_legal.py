import requests

from bs4 import BeautifulSoup
from scrapers.scraper import WebScraper, log_decorator


class BuhoLegal(WebScraper):
    def __init__(self):
        super(BuhoLegal, self).__init__()
        self.agent_id = 4

    @log_decorator
    def execute(self, nombre=None, paterno=None, materno=None):
        super(BuhoLegal, self).execute()

        params = {
            'nombre': nombre,
            'paterno': paterno,
            'materno': materno,
            'estado': 'Cualquier',
            'ano_inicial': 'Cualquier',
            'ano_fin': 'Cualquier'
        }

        r = requests.post('http://www.buholegal.com/consultasep/', data=params)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', attrs={'id': 'resultadosbusquedacedula'})

        if not table:
            return

        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            query = 'INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);'
            self.cursor.execute(query, (cols[4], 'http://cedula.buholegal.com/' + cols[0], cols[5], self.agent_id))
            self.incr()
        self.conn.commit()


if __name__ == '__main__':
    BuhoLegal().execute(nombre='juan', paterno='perez', materno='perez')

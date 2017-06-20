import requests

from bs4 import BeautifulSoup
from db import get_connection
from scrapers.scraper import WebScraper, log_decorator


def get_sancionados():
    r = requests.post('http://directoriosancionados.funcionpublica.gob.mx/SanFicTec/jsp/Ficha_Tecnica/SancionadosN.jsp',
                      params={'cmdsan': 'ALL', 'tipoqry': 'ALL', 'mostrar_msg': 'SI'})
    soup = BeautifulSoup(r.text, 'html.parser')

    rows = soup.find_all('td', {'align': 'left'})
    conn = get_connection()
    cursor = conn.cursor()

    try:
        for row in rows:
            query = 'INSERT INTO fp_sancionados (name, url) VALUES (%s, %s);'
            cursor.execute(query, (row.text,
                                   'http://directoriosancionados.funcionpublica.gob.mx/SanFicTec/jsp/Ficha_Tecnica/' +
                                   row.a.get('href')))

        conn.commit()
    finally:
        conn.close()


class FuncionPublicaScraper(WebScraper):
    def __init__(self):
        super(FuncionPublicaScraper, self).__init__()
        self.agent_id = 3

    @log_decorator
    def execute(self, q=None):
        super(FuncionPublicaScraper, self).execute()

        query = "SELECT id, name, url FROM fp_sancionados WHERE name LIKE '%{}%';".format(q)
        self.cursor.execute(query)
        query_params = [(record[1], record[2], record[1], self.agent_id) for record in self.cursor]

        for params in query_params:
            self.cursor.execute('INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);', params)
            self.incr()

        self.conn.commit()

if __name__ == '__main__':
    # get_sancionados()
    FuncionPublicaScraper().execute('ACEROS')

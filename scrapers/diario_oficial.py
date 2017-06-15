import requests

from bs4 import BeautifulSoup
from scrapers.scraper import WebScraper, log_decorator


class DiarioOficial(WebScraper):
    def __init__(self):
        super(DiarioOficial, self).__init__()
        self.agent_id = 7

    @log_decorator
    def execute(self, q=None):
        super(DiarioOficial, self).execute()

        r = requests.get('http://www.dof.gob.mx/busqueda_detalle.php?vienede=avanzada&busqueda_cuerpo=&BUSCAR_EN=C&'
                         'textobusqueda={}&TIPO_TEXTO=Y&choosePeriodDate=P&periodoFecha=Y&orga%5B%5D=AV%2C1'.format(q))

        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', {'class': 'bus_det_list'})
        rows = table.find_all('tr')

        for row in rows:
            td = row.find('td', {'class': 'txt_azul'})
            if td:
                date = td.b.text
                link = td.a.get('href')
                notice = td.a.string

                query = 'INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);'
                self.cursor.execute(query, (notice, link, td.text.strip('\t\n\r'), self.agent_id))
                self.incr()

        self.conn.commit()


if __name__ == '__main__':
    DiarioOficial().execute(q='pablo')

import requests

from bs4 import BeautifulSoup
from scrapers.scraper import WebScraper, log_decorator


class ImpiScraper(WebScraper):
    def __init__(self):
        super(ImpiScraper, self).__init__()
        self.agent_id = 8

    @log_decorator
    def execute(self, q=None):
        super(ImpiScraper, self).execute()

        params = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': 'frmBsqDen:busquedaIdButton',
            'javax.faces.partial.execute': 'frmBsqDen:busquedaIdButton frmBsqDen:denominacionId frmBsqDen:swtExacto',
            'javax.faces.partial.render': 'frmBsqDen:pnlBsqDen frmBsqDen:denominacionId frmBsqDen:pnlResultados '
                                          'frmBsqDen:pnlGrdNoRecords',
            'frmBsqDen:busquedaIdButton': 'frmBsqDen:busquedaIdButton',
            'frmBsqDen': 'frmBsqDen',
            'frmBsqDen:denominacionId': q,
            'javax.faces.ViewState': '7200227802800162773:4057735365263285658'
        }

        r = requests.post('http://marcanet.impi.gob.mx/marcanet/vistas/common/home.pgi', params=params)
        soup = BeautifulSoup(r.text, 'xml')
        results = BeautifulSoup(soup.find('update', {'id': 'frmBsqDen:pnlResultados'}).text, 'html.parser')
        table_body = results.find('tbody', {'id': 'frmBsqDen:resultadoExpediente_data'})
        rows = table_body.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if cols[0] == 'Sin registros.':
                return

            query = 'INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);'
            self.cursor.execute(query, (cols[1] + ' ' + cols[2],
                                        'http://marcanet.impi.gob.mx/marcanet/vistas/common/home.pgi',
                                        cols[5], self.agent_id
                                        ))
            self.incr()

        self.conn.commit()


if __name__ == '__main__':
    ImpiScraper().execute(q='pollo')

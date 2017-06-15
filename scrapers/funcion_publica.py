import requests

from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from scrapers.scraper import WebScraper, log_decorator


class FuncionPublicaScraper(WebScraper):
    def __init__(self):
        super(FuncionPublicaScraper, self).__init__()
        self.agent_id = 12

    @log_decorator
    def execute(self, q=None):
        super(FuncionPublicaScraper, self).execute()

        params = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': 'btnBuscar',
            'javax.faces.partial.execute': '@all',
            'javax.faces.partial.render': 'pnlGrpMstr',
            'btnBuscar': 'btnBuscar',
            'form': 'form',
            'txtBusca': q,
            'dtTblConsulta_selection': '',
            'dtTblConsulta_scrollState': '0,0',
            'javax.faces.ViewState': '5519697699859358784:3174503932379279979'
        }

        r = requests.post('http://reniresp.funcionpublica.gob.mx/ppcapf/consulta/consultaServidorPublico.jsf;jsessionid=97ea5787e1306addd3673563eae6',
                          params=params)
        soup = BeautifulSoup(r.text, 'xml')
        results = BeautifulSoup(soup.find('update').text, 'html.parser')
        table_body = results.find('tbody', {'id': 'dtTblConsulta_data'})
        rows = table_body.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            query = 'INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);'
            self.cursor.execute(query, (cols[0],
                                        'http://reniresp.funcionpublica.gob.mx/ppcapf/consulta/consultaServidorPublico.jsf',
                                        cols[1] + ' ' + cols[2], self.agent_id))
            self.incr()

        self.conn.commit()

if __name__ == '__main__':
    FuncionPublicaScraper().execute(q='pablo')

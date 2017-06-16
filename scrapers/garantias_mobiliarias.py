import requests

from bs4 import BeautifulSoup
from scrapers.scraper import WebScraper, log_decorator


class GarantiasMobiliariasScraper(WebScraper):
    def __init__(self):
        super(GarantiasMobiliariasScraper, self).__init__()
        self.agent_id = 11

    @log_decorator
    def execute(self, q=None):
        super(GarantiasMobiliariasScraper, self).execute()

        session = requests.Session()
        session.post('http://www.rug.gob.mx/Rug/j_security_check', data={'j_username': 'fcopantoja@gmail.com',
                                                                         'j_password': 'Alluxi123.'})

        data = {
            'callCount': '1',
            'windowName': '',
            'c0-scriptName': 'BusquedaDwrAction',
            'c0-methodName': 'buscar',
            'c0-id': '0',
            'c0-param0': 'string:',
            'c0-param1': 'string:',
            'c0-param2': 'string:',
            'c0-param3': 'string:%s' % q,
            'c0-param4': 'string:',
            'c0-param5': 'string:%2FRug',
            'batchId': '2',
            'page': '%2FRug%2Fhome%2Fbusqueda.do',
            'httpSessionId': session.cookies['JSESSIONID'],
            'scriptSessionId': session.cookies['JSESSIONID']
        }

        r = session.post('http://www.rug.gob.mx/Rug/dwr/call/plaincall/BusquedaDwrAction.buscar.dwr', data=data)
        response = r.text.split('\n')[4].replace('dwr.engine.remote.handleCallback("2","0",{codeError:0,message:" ', "")
        response = response.replace('"});', '').replace('\\"', '"').replace("\\'", '"')

        soup = BeautifulSoup(response, 'html.parser')
        table_body = soup.find('tbody')
        rows = table_body.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            a = row.find_all('a')
            cols = [ele.text.strip() for ele in cols]

            query = 'INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);'
            self.cursor.execute(query, (cols[3] + ' ' + cols[6], 'http://www.rug.gob.mx/Rug/home/' + a[0].get('href'),
                                        cols[2], self.agent_id))
            self.incr()

        self.conn.commit()

if __name__ == '__main__':
    GarantiasMobiliariasScraper().execute(q='ford fiesta')

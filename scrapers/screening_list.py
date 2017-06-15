import requests

from bs4 import BeautifulSoup
from scrapers.scraper import WebScraper, log_decorator


class ScreeningListScraper(WebScraper):
    def __init__(self):
        super(ScreeningListScraper, self).__init__()
        self.agent_id = 15

    @log_decorator
    def execute(self, q=None):
        super(ScreeningListScraper, self).execute()

        r = requests.get(
            'https://api.trade.gov/consolidated_screening_list/search?api_key=hQ4L7ylI9POH3QuqxOY_l2UC&q={}'.
                format(q))

        if r.status_code != 200:
            return

        response = r.json()
        for result in response['results']:
            query = 'INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);'
            self.cursor.execute(query, (result['name'], result['source_information_url'], result['source'],
                                        self.agent_id))
            self.incr()

        self.conn.commit()

if __name__ == '__main__':
    ScreeningListScraper().execute(q='inmuebles')

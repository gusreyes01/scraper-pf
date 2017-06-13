import requests

from bs4 import BeautifulSoup
from db import get_connection


def scrap_by_keyword(keyword):
    r = requests.get('https://api.trade.gov/consolidated_screening_list/search?api_key=hQ4L7ylI9POH3QuqxOY_l2UC&q={}'.
                     format(keyword))

    if r.status_code != 200:
        return

    response = r.json()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        for result in response['results']:
            query = 'INSERT INTO screening_list (name, source, source_information_url, keyword) VALUES ' \
                    '(%s, %s, %s, %s);'
            cursor.execute(query, (result['name'], result['source'], result['source_information_url'], keyword))

        conn.commit()
    except:
        conn.close()


if __name__ == '__main__':
    scrap_by_keyword('inmuebles')

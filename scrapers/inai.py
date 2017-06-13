import requests

from bs4 import BeautifulSoup
from db import get_connection


def scrap_by_person_name(name):
    r = requests.get('http://portaltransparencia.gob.mx/buscador/search/search.do?query={}&idDependenciaZoom'
                     '=&method=search&siglasDependencia=&idFraccionZoom=&searchBy=1'.format(name))

    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find_all('div', {'id': 'Box-info1'})
    conn = get_connection()
    cursor = conn.cursor()

    try:
        for row in rows:
            spans = row.find_all('span')
            query = 'INSERT INTO inai (position, source, link, person_name) VALUES (%s, %s, %s, %s);'
            cursor.execute(query, (row.a.text, spans[0].text + spans[1].text, row.a.get('href'), name))
        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    scrap_by_person_name('juan perez')

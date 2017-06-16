import requests

from bs4 import BeautifulSoup
from db import get_connection


def get_sancionados():
    r = requests.get('https://scsanctions.un.org/consolidated/')
    soup = BeautifulSoup(r.text, 'html.parser')
    individuals = soup.find_all('table', {'id': 'sanctions'})[0]
    rows = individuals.find_all('tr')

    entities = soup.find_all('table', {'id': 'sanctions'})[1]
    rows2 = entities.find_all('tr')

    conn = get_connection()
    cursor = conn.cursor()

    try:
        for row in rows:
            url = ''
            if row.a:
                url = row.a.get('href')
            query = 'INSERT INTO council_sancionados (description, type, url) VALUES (%s, %s, %s);'
            cursor.execute(query, (row.text.strip(), 'individual', url))

        for row in rows2:
            url = ''
            if row.a:
                url = row.a.get('href')

            query = 'INSERT INTO council_sancionados (description, type, url) VALUES (%s, %s, %s);'
            cursor.execute(query, (row.text.strip(), 'entities', url))

        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    get_sancionados()

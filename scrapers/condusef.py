import requests

from bs4 import BeautifulSoup
from db import get_connection


def get_sipres_results():
    r = requests.post('http://portal.condusef.gob.mx/SIPRES/jsp/pub/b_insincum_res.jsp', params={'tinc':1})
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find_all('td', {'class': 'contenidotexto'})

    conn = get_connection()
    cursor = conn.cursor()

    try:
        for row in rows:
            query = 'INSERT INTO sipres (institution) VALUES (%s);'
            cursor.execute(query, (row.text,))

        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    get_sipres_results()

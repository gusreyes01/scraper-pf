import requests

from bs4 import BeautifulSoup
from db import get_connection


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

if __name__ == '__main__':
    get_sancionados()

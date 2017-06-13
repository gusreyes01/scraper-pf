import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from db import get_connection


def scrap_by_person_name(name, paterno=None, materno=None):
    params = {
        'nombre': name,
        'paterno': paterno,
        'materno': materno,
        'estado': 'Cualquier',
        'ano_inicial': 'Cualquier',
        'ano_fin': 'Cualquier'
    }

    print(params)

    r = requests.post('http://www.buholegal.com/consultasep/', data=params)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table', attrs={'id': 'resultadosbusquedacedula'})

    if not table:
        return

    rows = table.find_all('tr')[1:]
    conn = get_connection()
    cursor = conn.cursor()

    try:
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            query = 'INSERT INTO buho (name, paternal_last_name, maternal_last_name, carrer, college, state, year, ' \
                    'person_name, link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'

            cursor.execute(query, (cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7],
                                   name + ' ' + paterno + ' ' + materno, 'http://cedula.buholegal.com/' + cols[0]))
        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    scrap_by_person_name('luis', paterno='perez', materno='perez')

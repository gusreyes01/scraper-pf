import requests

from bs4 import BeautifulSoup
from db import get_connection


def scrap_by_person_name(name):
    r = requests.get('http://www.dof.gob.mx/busqueda_detalle.php?vienede=avanzada&busqueda_cuerpo=&BUSCAR_EN=C&'
                     'textobusqueda={}&TIPO_TEXTO=Y&choosePeriodDate=P&periodoFecha=Y&orga%5B%5D=AV%2C1'.format(name))

    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', {'class': 'bus_det_list'})
    rows = table.find_all('tr')

    conn = get_connection()
    cursor = conn.cursor()

    try:
        for row in rows:
            td = row.find('td', {'class': 'txt_azul'})
            if td:
                date = td.b.text
                link = td.a.get('href')
                notice = td.a.string

                query = 'INSERT INTO dof (date, notice, link, person_name) VALUES (%s, %s, %s, %s);'
                cursor.execute(query, (date, notice, link, name))

        conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    scrap_by_person_name('pablo')

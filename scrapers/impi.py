import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from db import get_connection


def scrap_by_name(name):
    params = {
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': 'frmBsqDen:busquedaIdButton',
        'javax.faces.partial.execute': 'frmBsqDen:busquedaIdButton frmBsqDen:denominacionId frmBsqDen:swtExacto',
        'javax.faces.partial.render': 'frmBsqDen:pnlBsqDen frmBsqDen:denominacionId frmBsqDen:pnlResultados '
                                      'frmBsqDen:pnlGrdNoRecords',
        'frmBsqDen:busquedaIdButton': 'frmBsqDen:busquedaIdButton',
        'frmBsqDen': 'frmBsqDen',
        'frmBsqDen:denominacionId': name,
        'javax.faces.ViewState':'7200227802800162773:4057735365263285658'
    }

    r = requests.post('http://marcanet.impi.gob.mx/marcanet/vistas/common/home.pgi', params=params)
    soup = BeautifulSoup(r.text, 'xml')
    results = BeautifulSoup(soup.find('update', {'id': 'frmBsqDen:pnlResultados'}).text, 'html.parser')
    table_body = results.find('tbody', {'id': 'frmBsqDen:resultadoExpediente_data'})
    rows = table_body.find_all('tr')

    conn = get_connection()
    cursor = conn.cursor()
    try:
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if cols[0] == 'Sin registros.':
                return

            query = 'INSERT INTO impi (request_type, brand_type, record, registration, denomination, brand_name) ' \
                    'VALUES (%s, %s, %s, %s, %s, %s);'
            cursor.execute(query, (cols[1], cols[2], cols[3], cols[4], cols[5], name))
        conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    scrap_by_name('pollo')

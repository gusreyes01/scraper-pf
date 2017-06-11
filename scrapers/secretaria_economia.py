import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from db import get_connection


def scrap_by_person_name(name):
    params = {
        'v_fechaInicio': (datetime.now() - timedelta(days=365)).strftime('%d/%m/%Y'),
        'v_fechaFinal': datetime.now().strftime('%d/%m/%Y'),
        'v_buscar': name,
        'j_idt4': 'j_idt4',
        'btn_busqueda': 'busqueda',
        'javax.faces.ViewState': '5nfS3cNSLhoq/u8F+OivxCeRm2FJDpsP+BojbsvEwz9Y6bWZjsRR3ZpPjGjZavC4sVE3Y87HwRqlg'
                                 'vNxeiaS4gEWRbn0ZLC0TpVI8AkA7NeoTK7gY3gJ5EbqrFHMF0pCQPUCi5kR25zETvvZbNmzDm0wtUqd'
                                 'ElSh/rpHVxAaNCrdWDg7OBAzRkLEq6oWQidQaTElLu76psLy/d2k8pfIdsu6xlvLGThucwQzH8jZAoa+/'
                                 'Bw5yA4xNCrAPfEG+PhnC6ukukHIQ4BC1AO73T9D68sH6w3LJAk95qPCJjylkAqIB5/0yvIirf2MJ67klD'
                                 'qdKTTkr12Mzk4Irc2g9MIror8Jj5ndb5fja9hpE+4LKPEu7fvD9X/T0j3x+y+cy7FW9P1N0gZfm/HSyi6'
                                 'ygwDacmdkp29qa2zgSspzJUe2PLZ7se4a/RJDKg8UztH3Ao2iqN8iSBKJRH+qDdDTJj1Fws75xsOPf6e'
                                 'rBFCxMpE9ixj3QRIt7qgRNazdpR9DDbFWAf8Q+AX0dtxrUblwYotfz5UZV7ZlWIabUuyNXUDsAfUxN1r'
                                 'ipnAcMLJOvJW4W+Xc'
    }

    r = requests.post('https://psm.economia.gob.mx/PSM/busqueda.jsf', params=params)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table', attrs={'role': 'grid'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    conn = get_connection()
    cursor = conn.cursor()

    try:
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            query = 'INSERT INTO se (publication, date, person_name, business_name) VALUES (%s, %s, %s, %s);'
            cursor.execute(query, (cols[2], cols[4], name, cols[1]))

        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    scrap_by_person_name('juan')

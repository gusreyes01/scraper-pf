import requests

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

from scrapers.scraper import WebScraper, log_decorator


class BuhoLegal(WebScraper):
    def __init__(self):
        super(BuhoLegal, self).__init__()
        self.agent_id = 4

    @log_decorator
    def execute(self, nombre=None, paterno=None, materno=None):
        super(BuhoLegal, self).execute()

        params = {
            'nombre': nombre,
            'paterno': paterno,
            'materno': materno,
            'estado': 'Cualquier',
            'ano_inicial': 'Cualquier',
            'ano_fin': 'Cualquier'
        }

        r = requests.post('http://www.buholegal.com/consultasep/', data=params)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', attrs={'id': 'resultadosbusquedacedula'})

        if not table:
            return

        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            query = 'INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);'
            self.cursor.execute(query, (cols[4], 'http://cedula.buholegal.com/' + cols[0], cols[5], self.agent_id))
            self.incr()
        self.conn.commit()


class BuhoLegalGoogle(WebScraper):
    def __init__(self):
        super(BuhoLegalGoogle, self).__init__()
        self.agent_id = 16

    @log_decorator
    def execute(self, q=None):
        super(BuhoLegalGoogle, self).execute()

        # driver = webdriver.Chrome('/Users/fcopantoja/Downloads/chromedriver')
        driver = webdriver.PhantomJS('/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs')
        driver.set_window_size(1120, 550)
        driver.get('https://www.google.com.mx/search?q=buho+legal+%s' % q)

        RESULTS_LOCATOR = '//div/h3/a'
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))
        page1_results = driver.find_elements(By.XPATH, RESULTS_LOCATOR)
        page1_url_results = [x.get_attribute('href') for x in page1_results]

        for url in page1_url_results:
            print(url)
            driver.get(url)

            try:
                header = driver.find_element_by_xpath(
                    '//*[@id="masterdiv"]/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/div')
            except NoSuchElementException:
                continue

            header = header.text
            RECORDS_DATE_LOCATOR = '//*[@id="masterdiv"]/table/tbody/tr[2]/td/table/tbody/tr[%s]/td[1]/div'
            RECORDS_ACUERDO_LOCATOR = '//*[@id="masterdiv"]/table/tbody/tr[2]/td/table/tbody/tr[%s]/td[2]/div'
            records = []

            for i in range(2, 7):
                date = driver.find_element_by_xpath(RECORDS_DATE_LOCATOR % i)
                if date:
                    records.append(
                        '%s %s' % (date.text, driver.find_element_by_xpath(RECORDS_ACUERDO_LOCATOR % i).text.strip()))

            query = 'INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);'
            self.cursor.execute(query, (header, url, '|'.join(records), self.agent_id))
            self.incr()
            self.conn.commit()

        driver.quit()


if __name__ == '__main__':
    #     BuhoLegalGoogle().execute(nombre='juan', paterno='perez', materno='perez')
    BuhoLegalGoogle().execute(q='gustavo reyes')


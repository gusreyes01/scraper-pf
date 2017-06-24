from selenium import webdriver

from scrapers.scraper import WebScraper, log_decorator


class SecretariaEconomiaListScraper(WebScraper):
    def __init__(self):
        super(SecretariaEconomiaListScraper, self).__init__()
        self.agent_id = 6

    @log_decorator
    def execute(self, q=None):
        super(SecretariaEconomiaListScraper, self).execute()

        driver = webdriver.PhantomJS('/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs')
        driver.set_window_size(1120, 550)
        driver.get('https://psm.economia.gob.mx/PSM/busqueda.jsf')

        input_text = driver.find_element_by_id("textoBuscar")
        input_text.send_keys(q)
        driver.find_element_by_id('btn_buscar').click()

        for i in range(1, 11):
            link = driver.find_elements_by_css_selector(
                '#j_idt7_data > tr:nth-child(' + str(i) + ') > td:nth-child(3) > a')
            if link:
                link[0].click()
                url = driver.find_element_by_xpath('//*[@id="grid"]/tbody/tr[6]/td[2]/div/a').get_attribute('href')
                razon_social = driver.find_element_by_xpath('//*[@id="grid"]/tbody/tr[1]/td[2]/label').text
                nombre = driver.find_element_by_xpath('//*[@id="grid"]/tbody/tr[3]/td[2]/label').text
                print(url)

                query = 'INSERT INTO scraper (header, url, body, fuente_id) VALUES (%s, %s, %s, %s);'
                self.cursor.execute(query, (razon_social, url, nombre, self.agent_id))
                self.incr()
                self.conn.commit()
                driver.back()
            else:
                break

        driver.quit()


if __name__ == '__main__':
    SecretariaEconomiaListScraper().execute(q='juan')

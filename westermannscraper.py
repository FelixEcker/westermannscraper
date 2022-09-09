#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import shutil

def main():
    options = Options()
    options.headless = False
    browser = webdriver.Firefox(options = options)
    browser.get("https://www.westermann.de")

    try:
        # Wait until the input is there
        elem = WebDriverWait(browser, 30).until(
            lambda browser: browser.current_url == "https://bibox2.westermann.de/book/5409/page/1"
        )
    finally:
        # Iterate Pages
        page = 1
        actualPage = 1
        while True:
            elem = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CLASS_NAME, "page")) #This is a dummy element
            )
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            aps = soup.find_all('app-page')

            for ap in aps:
                for img in ap.find_all('img'):
                    r = requests.get(img['src'], stream=True)
                    if r.status_code == 200:
                        with open("output/"+str(actualPage)+".png", 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)

                    actualPage += 1

            page += 2
            
            browser.get("https://bibox2.westermann.de/book/5409/page/"+str(page))

        browser.quit()

if __name__ == "__main__":
    main()
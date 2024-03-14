import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait

N_pressMore = 5
N_scrolls = 5

def parseSearch(request, driver):
    img_links = []
    words = request.split()
    driver.get('https://yandex.ru/images/search?lr=2&text='+"%20".join(words))
    for i in range(N_pressMore):
        for j in range(N_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(5)
        button = driver.find_element(By.CSS_SELECTOR, ".SerpList-LoadButton")
        if not button.is_displayed():
            wait = WebDriverWait(driver, timeout=100)
            wait.until(lambda d: button.is_displayed())
        button.click()
    elems = driver.find_elements(By.CSS_SELECTOR, ".SimpleImage-Cover")
    links = [elem.get_attribute('href') for elem in elems]
    for link in links:
        driver.get(link)
        try:
            img = driver.find_element(By.CSS_SELECTOR, ".MMImage-Origin").get_attribute('src')
        except NoSuchElementException:
            continue
        img_links.append(img)
    return img_links


driver = webdriver.Chrome()
pd.DataFrame(parseSearch("волк мемы", driver)).to_csv("data_wolf.csv", mode = 'w')
pd.DataFrame(parseSearch("cat memes", driver)).to_csv("data_cat.csv", mode = 'w')
driver.close()

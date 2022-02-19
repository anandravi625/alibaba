import math
import re
from concurrent.futures import ProcessPoolExecutor, wait


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from re import findall
import csv
import time

s = Service('chromedriver.exe')



executor = ProcessPoolExecutor(max_workers=1)


def data_extractor(page,r):

    newdriver = webdriver.Chrome(service=s)
    newdriver.maximize_window()
    newdriver.implicitly_wait(5)

    newdriver.get(f"https://www.noon.com/uae-en/search/?page={page}&q={r}")
    elements = newdriver.find_elements(By.XPATH, "//div[contains(@class,'productContainer')]")
    for i in range(1, len(elements) + 1):
        try:
            name = newdriver.find_element(By.XPATH,
                                            f"//div[contains(@class,'productContainer')][{i}]//div/span[1]/span[1]").text
        except:
            name = ''
        try:
            aed = newdriver.find_element(By.XPATH,
                                           f"//div[contains(@class,'productContainer')][{i}]//div[2]/div/div/strong").text
        except:
            aed = ''
        try:
            rating = newdriver.find_element(By.XPATH,
                                              f"//div[contains(@class,'productContainer')][{i}]//div[3]//div[2]/div/span").text
        except:
            rating = ''

        with open('noon_multifile.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            try:
                writer.writerow(
                    [name.replace("\n", " ").replace("\r", "").replace("…", "").replace("‑", " ").strip(), aed.strip(),
                     rating.strip()])
            except:
                pass
    newdriver.quit()


def counte():
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get("https://www.noon.com/uae-en/")
    time.sleep(3)

    a = driver.find_element(By.XPATH, "//input[contains(@id,'searchBar')]")
    time.sleep(2)
    c = input("Enter product to search: ")
    a.send_keys(c)
    a.send_keys(Keys.RETURN)
    time.sleep(5)
    count = driver.find_element(By.XPATH,"//div[contains(@class,'sc-14cxujr-3 gZOAPV')]").text
    counts = re.findall("\d{4}]",count)[0]
    elements = driver.find_elements(By.XPATH, "//div[contains(@class,'productContainer')]")
    time.sleep(3)
    pages = int(math.ceil(int(counts)/len(elements)))
    time.sleep(5)
    header_file = ["NAME", "PRICE(IN AED)", "RATING"]
    with open('noon_multifile.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header_file)

    features = [executor.submit(data_extractor, j,c) for j in range(1, pages)]
    wait(features)
    driver.quit()

if __name__ == "__main__":   #1-16 resut 3000 resut
    counte()
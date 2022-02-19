from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time

s = Service('chromedriver.exe')
def data_extractor():
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.implicitly_wait(5)
    data = []

    driver.get("https://www.noon.com/uae-en/")
    time.sleep(3)

    a = driver.find_element(By.XPATH, "//input[contains(@id,'searchBar')]")
    time.sleep(2)
    a.send_keys(input("Enter product to search: "))
    a.send_keys(Keys.RETURN)
    elements = driver.find_elements(By.XPATH, "//div[contains(@class,'productContainer')]")
    time.sleep(3)

    header_file = ["NAME", "PRICE(IN AED)", "RATING"]
    with open('noon_file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header_file)


    for i in range(1, len(elements) + 1):
        try:
            name = driver.find_element(By.XPATH,
                                       f"//div[contains(@class,'productContainer')][{i}]//div/span[1]/span[1]").text
        except:
            name = ''
        try:
            aed = driver.find_element(By.XPATH,
                                      f"//div[contains(@class,'productContainer')][{i}]//div[2]/div/div/strong").text
        except:
            aed = ''
        try:
            rating = driver.find_element(By.XPATH,
                                         f"//div[contains(@class,'productContainer')][{i}]//div[3]//div[2]/div/span").text
        except:
            rating = ''

        with open('noon_file.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            try:
                writer.writerow(
                    [name.replace("\n", " ").replace("\r", "").replace("…", "").replace("‑", " ").strip(), aed.strip(),
                     rating.strip()])
            except:
                pass
    driver.close()

if __name__ == "__main__":
    data_extractor()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.maximize_window()
driver.implicitly_wait(5)
list=[]

driver.get("https://www.noon.com/uae-en/")
time.sleep(3)

a=driver.find_element(By.XPATH,"//input[contains(@id,'searchBar')]")
time.sleep(2)
a.send_keys(input("Enter product to search: "))
a.send_keys(Keys.RETURN)
elements = driver.find_elements(By.XPATH,"//div[contains(@class,'productContainer')]")
time.sleep(3)
for i in range(1,len(elements)+1):
    try:
        name = driver.find_element(By.XPATH,f"//div[contains(@class,'productContainer')][{i}]//div/span[1]/span[1]").text
        aed = driver.find_element(By.XPATH,f"//div[contains(@class,'productContainer')][{i}]//div[2]/div/div/strong").text
        rating = driver.find_element(By.XPATH,f"//div[contains(@class,'productContainer')][{i}]//div[3]//div[2]/div/span").text
    except:
        pass

    dict={"NAME": name,
      "PRICE(IN AED)": aed,
      "RATING": rating
      }
    list.append(dict)
    df=pd.DataFrame(list)
    print(df)
    df.to_csv("noon.csv",index=False)


driver.close()





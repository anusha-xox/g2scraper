import time
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

page_urls = ["https://www.g2.com/categories/online-backup",
             "https://www.g2.com/categories/online-backup?order=g2_score&page=2#product-list"]
             # "https://www.g2.com/categories/online-backup?order=g2_score&page=3#product-list"]
product_title = []
float_ratings = []
hyperlinks = []

for page in page_urls:
    chrome_driver_path = "C:\Developement\chromedriver.exe"
    # uc.install(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    driver.get(page)
    driver.maximize_window()

    product_t = [element.text for element in
                 driver.find_elements(by=By.CLASS_NAME, value="product-listing__product-name")]
    product_title.extend(product_t)
    print(len(product_title))

    ratings = [element.text for element in driver.find_elements(by=By.CSS_SELECTOR, value="span .fw-semibold")]
    for rating in ratings:
        try:
            rating = float(rating)
            if 0 <= float(rating) < 5:
                float_ratings.append(rating)
        except ValueError:
            if len(float_ratings) == len(product_title):
                pass
            else:
                float_ratings.append(0.1) #Some services didn't have ratings
    print(len(float_ratings))

    hyperl = [element.get_attribute("href") for element in driver.find_elements(by=By.CLASS_NAME, value="ai-c")]
    hyperl = list(filter(None, hyperl))
    hyperl = hyperl[2:]
    hyperlinks.extend(hyperl)
    print(len(hyperlinks))
    driver.quit()

scraped_dict = {"Title": product_title, "Rating": float_ratings, "HyperLinks": hyperlinks}
df = pandas.DataFrame(scraped_dict)
df.to_csv('scraped_data.csv')

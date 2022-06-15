import requests
from bs4 import BeautifulSoup
import lxml
import urllib.parse
import pandas
import time
API_TOKEN = "620937eccb6c48fca718f6eae7592cbc0de44d7e010"
page_urls = ["https://www.g2.com/categories/online-backup",
             "https://www.g2.com/categories/online-backup?order=g2_score&page=2",
             "https://www.g2.com/categories/online-backup?order=g2_score&page=3",
             "https://www.g2.com/categories/online-backup?order=g2_score&page=4"]

product_titles = []
float_ratings = []
hyperlinks = []

for page_no in page_urls:
    url = f"http://api.scrape.do/?token={API_TOKEN}&url={urllib.parse.quote(page_no)}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        p_titles = [product.getText() for product in soup.find_all(class_="product-listing__product-name")]
        product_titles.extend(p_titles)
        print(len(product_titles))
        print(product_titles)

        ratings = [rating.getText() for rating in soup.find_all(name="span", class_="fw-semibold")]
        for rating in ratings:
            try:
                rating = float(rating)
                if 0 <= float(rating) < 5:
                    float_ratings.append(rating)
            except ValueError:
                pass
                # if len(float_ratings) == len(product_titles):
                #     pass
                # else:
                # float_ratings.append(0.1)
        print(len(float_ratings))
        print(float_ratings)

        h_links = soup.find_all(class_="ai-c")
        for i in range(2, len(h_links)):
            try:
                hyperlinks.append(h_links[i]["href"])
            except KeyError:
                pass
        print(len(hyperlinks))
        print(hyperlinks)
        time.sleep(1)

    except requests.exceptions.RequestException:
        soup = "Nothing"
        print(soup)
        break

scraped_dict = {"Title": product_titles, "Rating": float_ratings, "HyperLinks": hyperlinks}
df = pandas.DataFrame(scraped_dict)
df.to_csv('scraped_data_2.csv')

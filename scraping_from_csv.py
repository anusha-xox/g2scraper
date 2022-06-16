import requests
from bs4 import BeautifulSoup
import lxml
import urllib.parse
import pandas
import time
import openpyxl

wb = openpyxl.load_workbook("functionalAreas.xlsx")
ws = wb.get_sheet_by_name("FunctionalAreas")
page_urls = []
for i in range(2, 51):
    page_url = ws.cell(row=i, column=2).hyperlink.target
    page_urls.append(page_url)

API_TOKEN = ""

product_titles = []
hyper_link_titles = []
float_ratings = []
hyperlinks = []

for page_no in page_urls:
    url = f"http://api.scrape.do/?token={API_TOKEN}&super=true&url={urllib.parse.quote(page_no)}"
    try:
        response = requests.get(url)
        if response.status_code >= 300:
            print(response.status_code)
        else:
            print(response.status_code)
            soup = BeautifulSoup(response.text, "html.parser")

            for i in range(len(product_titles) - len(float_ratings) + 2):
                if len(product_titles) > len(float_ratings):
                    float_ratings.append(0)

            p_titles = [product.getText() for product in soup.find_all(class_="product-listing__product-name")]
            product_titles.extend(p_titles)
            print(len(product_titles))
            print(product_titles)

            ratings = [rating.getText() for rating in soup.find_all(name="span", class_="fw-semibold")]
            ratings = ratings[1:len(ratings):2]
            for i in range(len(p_titles) + 1):
                try:
                    rating = float(ratings[i])
                    if -1 <= rating <= 5:
                        float_ratings.append(rating)
                except ValueError:
                    pass
                except IndexError:
                    float_ratings.append(0)
            print(len(float_ratings))
            print(float_ratings)

            for title in p_titles:
                title = title.replace(' ', '-').lower()
                generated_url = f'https://www.g2.com/products/{title}/reviews'
                hyper_link_titles.append(generated_url)
            print(len(hyper_link_titles))
            print(hyper_link_titles)

            h_links = soup.find_all(class_="ai-c")
            for i in range(2, len(h_links)):
                try:
                    hyperlinks.append(h_links[i]["href"])
                except KeyError:
                    pass

    except requests.exceptions.RequestException:
        soup = "Nothing"
        print(soup)
        break

if len(float_ratings) != 0:
    for i in range(10):
        if len(product_titles) > len(float_ratings):
            float_ratings.append(0)
    scraped_dict = {"Title": product_titles, "Rating": float_ratings, "HyperLinks": hyper_link_titles}
    df = pandas.DataFrame(scraped_dict)
    df.to_csv('scraped_from_xlsx.csv')

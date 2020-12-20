import json
from checker.search import ReadShopData, FilterResults, Search
from checker.check import CheckData
import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":

    with open("./files/categories.txt", "r") as text_file:
        text_data = text_file.readlines()

    categories = []
    for t in text_data:
        if t.replace("\n", "") not in categories:
            categories.append(t.replace("\n", ""))

    cities = []
    with open("./files/city_list.txt", "r") as text_file:
        text_data = text_file.readlines()
    for t in text_data:
        cities.append(t.replace("\n", ""))

    for city in cities:
        domains = []
        pages = [
            f"https://search.yahoo.com/search?p=buy {categories[0]} {city}"]
        for page in pages:
            print(page)
            url = page
            html = requests.get(url).text
            bs = BeautifulSoup(html, "html.parser")

            # Ссылки на страницы результатов расположены в h3.
            h3_tags = bs.find_all("h3", {"class": "title"})
            for h3 in h3_tags:
                try:
                    link = h3.find("a").attrs["href"]

                    link = link.rsplit("/", 1)[0]
                    domain = link.split("//", 1)[1].replace("www", "").split(".", 1)[0]
                    if domain not in domains:
                        CheckData(shop_dict=dict(shop_link=link, category=categories[0], city=city))
                        domains.append(domain)
                except AttributeError:
                    pass

            # Добавляем следующие страницы.
            pagination_div = bs.find("div", {"class": "pages"})
            try:
                for a in pagination_div.find_all("a"):
                    if a.attrs["href"] not in pages:
                        pages.append(a.attrs["href"])
            except AttributeError:
                pass
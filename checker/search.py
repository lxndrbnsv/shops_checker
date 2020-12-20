import json

import requests
from bs4 import BeautifulSoup


class Search:
    def __init__(self):
        """Поиск по категориям и запись в файл."""
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

        site_links = []

        for city in cities:
            pages = [f"https://search.yahoo.com/search?p=buy {categories[0]} {city}"]
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
                        if link not in site_links:
                            site_links.append(dict(category=categories[0], shop_link=link, city=city))
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

        json_data = json.dumps(site_links)
        with open("./files/shops.json", "w+") as json_file:
            json_file.write(json_data)


class FilterShops:
    def __init__(self):
        with open("./files/shops.txt", "r") as text_file:
            text_data = text_file.readlines()

        shops_unfiltered = []  # Список без дублей.
        for t in text_data:
            if t.replace("\n", "") not in shops_unfiltered:
                shops_unfiltered.append(t.replace("\n", ""))

        blacklist = [
            "amazon",
            "craiglist",
            "ebay",
            "youtube",
            "facebook",
            "instagram",
            "walmart",
            "forbes",
            "google"
        ]

        shops = []
        for s in shops_unfiltered:
            link = s.replace("www.", "").rsplit("/", 1)[0]
            domain = link.split("//", 1)[1].split(".", 1)[0]
            if blacklist not in domain and domain not in shops:
                if link not in shops and domain not in shops:
                    shops.append(link)

        with open("./files/filtered_shops.txt", "a+") as text_file:
            for s in shops:
                text_file.writelines(f"{s}\n")


class ReadShopData:
    def __init__(self):
        with open("./files/filtered_shops.txt", "r") as text_file:
            text_data = text_file.readlines()

        links = []
        for t in text_data:
            if t.replace("\n", "") not in links:
                links.append(t.replace("\n", ""))

        self.links = links


class FilterResults:
    def __init__(self):
        with open("./results.txt", "r") as text_file:
            text_data = text_file.readlines()

        shops_unfiltered = []  # Список без дублей.
        for t in text_data:
            if t.replace("\n", "") not in shops_unfiltered:
                shops_unfiltered.append(t.replace("\n", ""))

        blacklist = [
            "amazon",
            "craiglist",
            "ebay",
            "youtube",
            "facebook",
            "instagram",
            "walmart",
            "google",
            "forbes"
        ]

        shops = []
        for s in shops_unfiltered:
            link = s.rsplit("/", 1)[0]
            domain = s.split("//", 1)[1].split(".", 1)[0]
            if domain not in blacklist and domain not in shops:
                if link not in shops:
                    shops.append(link)

        with open("./filtered_results.txt", "a+") as text_file:
            for s in shops:
                text_file.writelines(f"{s}\n")

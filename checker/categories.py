import requests
from bs4 import BeautifulSoup


class ReadCategories:
    def __init__(self):
        with open("./files/categories.txt", "r") as text_file:
            text_data = text_file.readlines()

        categories = []
        for t in text_data:
            if t.replace("\n", "") not in categories:
                categories.append(t.replace("\n", ""))

        self.categories = categories

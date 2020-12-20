import json
import csv
import requests


class CheckData:
    def __init__(self, shop_dict):

        print(shop_dict)
        url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?" \
              f"url={shop_dict['shop_link']}&key= AIzaSyDXP2ElzF3MSQQeBiFk0lKG9Kjg0gVfcTo"

        response = requests.get(url)

        if response.status_code == 200:
            response_data = response.json()
            try:
                fcp = response_data[
                    "loadingExperience"
                ]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["percentile"]
                if fcp >= 2500:
                    with open("results_all.csv", mode="a+") as csv_file:
                        csv_write = csv.writer(
                            csv_file,
                            delimiter=";",
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL
                        )
                        csv_write.writerow(
                            [
                                shop_dict["shop_link"],
                                shop_dict["category"],
                                shop_dict["city"]
                            ]
                        )
                    print("***ADDED***")

            except KeyError:
                pass
        else:
            pass

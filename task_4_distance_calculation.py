import requests                     # pip install requests
import re
from bs4 import BeautifulSoup       # pip install beautifulsoup4


class DistanceCalculation:

    def __init__(self):
        self.distances = dict()
        self.dataframe = None

    @staticmethod
    def parse_data(url):
        try:
            realty = requests.get(url)
            inner_soup = BeautifulSoup(realty.content, "html.parser")
            find_km = re.search('"([\d]+,?[\d]*) km', str(inner_soup), re.IGNORECASE)
            find_m = re.search('"([\d]+,?[\d]*) m', str(inner_soup), re.IGNORECASE)
            if find_km:
                return float(find_km.group(1).replace(',', '.')) * 1000
            elif find_m:
                return float(find_km.group(1).replace(',', '.'))
            return None

        except Exception as e:
            print("Error with parsing data:", str(e))
            return None

    def collect_data(self, part_to):
        try:
            part_to = part_to.replace(' ', '%20').lower()

            url = 'https://www.google.com/maps/dir/knez%20mihailova/{}/?hl=sr'.format(part_to)
            # print(url)
            return self.parse_data(url)

        except requests.exceptions.RequestException as e:
            print('Skipping. Connection error.', e)

        except Exception as e:
            print("Error:", e)
            pass

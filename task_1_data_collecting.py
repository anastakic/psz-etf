import requests  # pip install requests
import time

from bs4 import BeautifulSoup  # pip install beautifulsoup4
from task_1_database_connection import DataBase


class DataCollector:

    def __init__(self):
        self.type = None
        self.sell_or_rent = None
        self.size = None
        self.price = None
        self.city = None
        self.part_of_city = None
        self.land_size = None
        self.floor = None
        self.total_floors = None
        self.num_of_rooms = None
        self.num_of_bathrooms = None
        self.registered = False
        self.parking = None
        self.elevator = None
        self.balcony = None
        self.heating = None
        self.year_built = None
        self.construction = None
        self.url = None
        self.data_base = DataBase()

    def start(self):
        print('TASK 1 STARTED...')

        self.data_base = DataBase()
        self.collect_data()
        self.data_base.insert_data()

        print('TASK 1 FINISHED!')
        print('****************')

    def init_data(self):
        self.type = None
        self.sell_or_rent = None
        self.size = None
        self.price = None
        self.city = None
        self.part_of_city = None
        self.land_size = None
        self.floor = None
        self.total_floors = None
        self.num_of_rooms = None
        self.num_of_bathrooms = None
        self.registered = False
        self.parking = None
        self.elevator = None
        self.balcony = None
        self.heating = None
        self.year_built = None
        self.construction = None
        self.url = None

    def get_data(self):
        return (
            self.type,
            self.sell_or_rent,
            self.size,
            self.price,
            self.city,
            self.part_of_city,
            self.land_size,
            self.floor,
            self.total_floors,
            self.num_of_rooms,
            self.num_of_bathrooms,
            self.registered,
            self.parking,
            self.elevator,
            self.balcony,
            self.heating,
            self.year_built,
            self.construction,
            self.url
        )

    @staticmethod
    def get_props(inner_soup):
        amenities_props = inner_soup.findAll('div', {'class': 'property__amenities'})
        for prop in amenities_props:
            if prop.contents[1].text == 'Podaci o nekretnini':
                return prop.contents[3]

    @staticmethod
    def get_props_additional(inner_soup):
        amenities_props = inner_soup.findAll('div', {'class': 'property__amenities'})
        for prop in amenities_props:
            if prop.contents[1].text == 'Dodatna opremljenost':
                return prop.contents[3]

    def get_heating(self, inner_soup):
        heating_content = inner_soup.findAll('div', {'class': 'property__main-details'})
        try:
            heating_content = heating_content[0].contents[1].contents
            for content in heating_content[1::2]:
                if 'Grejanje' in content.text:
                    heating = content.text.replace('Grejanje:', '')
                    heating = heating.replace('-', '')
                    self.heating = heating.strip() if heating.strip() != '' else None
        except Exception:
            self.heating = None

    def get_parking(self, inner_soup):
        parking_content = inner_soup.findAll('div', {'class': 'property__main-details'})
        try:
            parking_content = parking_content[0].contents[1].contents
            for content in parking_content[1::2]:
                if 'Parking' in content.text or 'Garaža' in content.text or 'Garažno mesto' in content.text:
                    parking = content.text.replace('Parking:', '')
                    parking = parking.replace('Garaža:', '')
                    parking = parking.replace('Garažno mesto:', '')
                    if parking.strip().lower() == 'da':
                        self.parking = True
                    elif parking.strip().lower() == 'ne':
                        self.parking = False
                    else:
                        self.parking = None
        except Exception:
            self.parking = None

    def get_bathrooms(self, inner_soup):
        bathrooms_content = inner_soup.findAll('div', {'class': 'property__main-details'})
        try:
            bathrooms_content = bathrooms_content[0].contents[1].contents
            for content in bathrooms_content[1::2]:
                if 'kupatil' in content.text.lower():
                    bathrooms = content.text.replace('Kupatilo:', '')
                    bathrooms = bathrooms.replace('Broj kupatila:', '')
                    bathrooms = bathrooms.replace('Kupatila:', '')
                    number = bathrooms.strip()
                    self.num_of_bathrooms = float(number)
        except Exception:
            self.num_of_bathrooms = None

    def get_elevator(self, additional):
        try:
            additional = additional.contents[1::2]
            if 'Lift' in [ad.contents[0] for ad in additional]:
                self.elevator = True
            else:
                self.elevator = False
        except Exception:
            self.elevator = None

    def get_balcony(self, additional):
        try:
            additional = additional.contents[1::2]
            if 'Terasa' in [ad.contents[0] for ad in additional] \
                    or 'Lođa' in [ad.contents[0] for ad in additional] \
                    or 'Balkon' in [ad.contents[0] for ad in additional]:
                self.balcony = True
            else:
                self.balcony = False
        except Exception:
            self.balcony = None

    def get_price(self, inner_soup):
        price_content = inner_soup.findAll('h4', {'class': 'stickyBox__price'})
        try:
            price = price_content[0].contents[0]
            if 'dogovor' in price.lower():
                return None
            price = price.replace('EUR', '')
            price = price.replace(' ', '')
            self.price = float(price)
        except Exception:
            self.price = None

    def get_sell_or_rent(self, content):
        if 'Transakcija' in content.contents[0]:
            if 'Prodaja' in content.contents[1].string:
                self.sell_or_rent = True
            else:
                self.sell_or_rent = False

    def get_type(self, content):
        if 'Kategorija' in content.contents[0]:
            category = ' '.join([cont.string for cont in content.contents])
            if 'kuća' in category.lower():
                self.type = False
            else:
                self.type = True

    def get_size(self, content):
        if 'Kvadratura' in content.contents[0]:
            square_metrics = ' '.join([cont.string for cont in content.contents])
            square_metrics = square_metrics.replace('Kvadratura:', '')
            square_metrics = square_metrics.replace('m²', '')
            square_metrics = square_metrics.strip()
            try:
                self.size = float(square_metrics)
            except ValueError:
                self.size = None

    def get_construction_type(self, content):
        if 'Stanje nekretnine' in content.contents[0]:
            state = ' '.join([cont.string for cont in content.contents])
            state = state.replace('Stanje nekretnine:', '')
            self.construction = state.strip()

    def get_land_size(self, content):
        if 'Površina zemljišta' in content.contents[0]:
            land_area = ' '.join([cont.string for cont in content.contents])
            land_area = land_area.replace('Površina zemljišta:', '')
            increase = 1
            land_area = land_area.replace('m²', '')
            if land_area.find('ar') >= 0:
                land_area = land_area.replace('ar', '')
                increase = 100
            elif land_area.find('hektar') >= 0 or land_area.find('ha') >= 0:
                land_area = land_area.replace('hektar', '')
                land_area = land_area.replace('ha', '')
                increase = 10000
            land_area = land_area.strip()
            self.land_size = float(land_area) * increase

    def get_registered(self, content):
        if 'Uknjiženo' in content.contents[0]:
            if 'Da' in ' '.join([cont.string for cont in content.contents]):
                self.registered = True
            else:
                self.registered = False

    def get_num_of_rooms(self, content):
        if 'Ukupan broj soba' in content.contents[0]:
            number_of_rooms = ' '.join([cont.string for cont in content.contents])
            number_of_rooms = number_of_rooms.replace('Ukupan broj soba:', '')
            number_of_rooms = number_of_rooms.strip()
            try:
                self.num_of_rooms = float(number_of_rooms)
            except ValueError:
                self.num_of_rooms = None

    def get_total_floors(self, content):
        if 'Ukupan broj spratova' in content.contents[0]:
            total_floors = ' '.join(
                [cont.string for cont in content.contents])
            total_floors = total_floors.replace('Ukupan broj spratova:', '')
            total_floors = total_floors.strip()
            try:
                self.total_floors = float(total_floors)
            except ValueError:
                self.total_floors = None

    def get_floor(self, content):
        if 'Sprat:' in content.contents[0] or 'Spratnost:' in content.contents[0]:
            floor = ' '.join([cont.string for cont in content.contents])  # content.contents[0]
            if 'prizemlje' in floor.lower():  # content.contents[0].lower():
                self.floor = 0
            else:
                floor = floor.replace('Sprat:', '')
                floor = floor.replace('Spratnost:', '')
                floor = floor.strip()
                try:
                    self.floor = float(floor)
                except Exception:
                    self.floor = None

    def get_year_built(self, content):
        if 'Godina izgradnje' in content.contents[0]:
            year_built = ' '.join([cont.string for cont in content.contents])
            year_built = year_built.replace('Godina izgradnje:', '')
            year_built = year_built.strip()
            try:
                self.year_built = int(year_built)
            except ValueError:
                self.year_built = None

    def get_num_of_bathrooms(self, content):
        if 'kupatil' in content.contents[0].lower():
            bathrooms = ' '.join([cont.string for cont in content.contents])
            bathrooms = bathrooms.replace('Kupatilo:', '')
            bathrooms = bathrooms.replace('Broj kupatila:', '')
            bathrooms = bathrooms.replace('Kupatila:', '')
            num_of_bathrooms = bathrooms.strip()
            try:
                self.num_of_bathrooms = float(num_of_bathrooms)
            except ValueError:
                self.num_of_bathrooms = None

    def parse_data(self, url):
        self.init_data()
        try:
            realty = requests.get(url)
            inner_soup = BeautifulSoup(realty.content, "html.parser")

            realty_props = self.get_props(inner_soup)
            additional_props = self.get_props_additional(inner_soup)

            self.url = url
            self.get_price(inner_soup)

            try:
                location_content = inner_soup.findAll('h3', {'class': 'stickyBox__Location'})
                location = location_content[0].contents[0]
            except Exception as exc:
                location = None
                print('Error:', str(exc))

            if (location is not None) and (',' in location):
                location = location.split(',', 1)
                self.city = location[0].strip()
                self.part_of_city = location[1].strip()
            else:
                self.city = str(location).strip()
                self.part_of_city = None

            self.get_heating(inner_soup)
            self.get_parking(inner_soup)
            self.get_bathrooms(inner_soup)
            self.get_elevator(additional_props)
            self.get_balcony(additional_props)

            contents_ = []

            try:
                contents_ = realty_props.contents[1::2]
            except:
                print('Error: Unable to get content.')
                time.sleep(5)

            for content in contents_:
                self.get_type(content)
                self.get_sell_or_rent(content)
                self.get_size(content)
                self.get_construction_type(content)
                self.get_land_size(content)
                self.get_registered(content)
                self.get_num_of_rooms(content)
                self.get_total_floors(content)
                self.get_year_built(content)
                self.get_num_of_bathrooms(content)
                self.get_floor(content)

            self.data_base.add_query(self.get_data())

        except Exception as e:
            print("Error with parsing data:", str(e))
            return

    def collect_data(self):
        num_of_pages = 10
        links = [
            # 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/izdavanje/lista/po-stranici/20/stranica/',
            'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/lista/po-stranici/20/stranica/',
            # 'https://www.nekretnine.rs/stambeni-objekti/kuce/lista/po-stranici/20/stranica/'
        ]
        for link in links:
            for page in range(num_of_pages):
                print('Current page number: ' + str(page))
                search_results_url = link + str(page + 1)
                try:
                    # time.sleep(0.01)
                    response = requests.get(search_results_url)

                    soup = BeautifulSoup(response.content, "html.parser")
                    properties = soup.findAll('div', {'class': 'placeholder-preview-box ratio-1-1'})

                    urls = ['https://www.nekretnine.rs' + p.contents[1].attrs['href'] for p in properties]
                    for url in urls:
                        self.parse_data(url)

                except requests.exceptions.RequestException as e:
                    print('Skipping. Connection error.', e)

                except Exception as e:
                    print("Error:", e)
                    pass

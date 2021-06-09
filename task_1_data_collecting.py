import requests  # pip install requests
import time

from bs4 import BeautifulSoup  # pip install beautifulsoup4
from xml.etree.cElementTree import fromstring
from task_1_fill_database import DataBase

from itertools import cycle


# free proxies, sometimes they do not work so use them only if a proxy is needed
def get_proxies():
    print('DSSSSSSSSSSSSSS')
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    """
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    """
    return proxies


def get_heating(inner_soup):
    heating_content = inner_soup.findAll('div', {'class': 'property__main-details'})
    try:
        heating_content = heating_content[0].contents[1].contents
        for content in heating_content[1::2]:
            if 'Grejanje' in content.text:
                heating = content.text.replace('Grejanje:', '')
                heating = heating.replace('-', '')
                heating = heating.strip()
                if heating == '':
                    return None
                return heating
    except Exception as ext6:
        print("Error6:", ext6)
        return None


def get_parking(inner_soup):
    parking_content = inner_soup.findAll('div', {'class': 'property__main-details'})
    try:
        parking_content = parking_content[0].contents[1].contents
        for content in parking_content[1::2]:
            if 'Parking' in content.text:
                parking = content.text.replace('Parking:', '')
                parking = parking.strip()
                if parking == '':
                    return None
                return parking
    except Exception as ext8:
        print("Error8:", ext8)
        return None


def get_bathrooms(inner_soup):
    bathrooms_content = inner_soup.findAll('div', {'class': 'property__main-details'})
    try:
        bathrooms_content = bathrooms_content[0].contents[1].contents
        for content in bathrooms_content[1::2]:
            if 'kupatil' in content.text.lower():
                bathrooms = content.text.replace('Kupatilo:', '')
                bathrooms = bathrooms.replace('Broj kupatila:', '')
                bathrooms = bathrooms.replace('Kupatila:', '')
                number = bathrooms.strip()
                return float(number)
    except Exception:
        return None


def get_elevator(additional):
    try:
        additional = additional.contents[1::2]
        if 'Lift' in [ad.contents[0] for ad in additional]:
            return 'Da'
        else:
            return 'Ne'
    except Exception:
        return None


def get_balcony(additional):
    try:
        additional = additional.contents[1::2]
        if 'Terasa' in [ad.contents[0] for ad in additional] \
                or 'Lođa' in [ad.contents[0] for ad in additional] \
                or 'Balkon' in [ad.contents[0] for ad in additional]:
            return 'Da'
        else:
            return 'Ne'
    except Exception:
        return None


def get_price(inner_soup):
    price_content = inner_soup.findAll('h4', {'class': 'stickyBox__price'})
    try:
        price = price_content[0].contents[0]
        if 'dogovor' in price.lower():
            return None
        price = price.replace('EUR', '')
        price = price.replace(' ', '')
        return float(price)
    except Exception as ext3:
        print("Error3:", ext3)
        return None


def get_props(inner_soup):
    amenities_props = inner_soup.findAll('div', {'class': 'property__amenities'})
    for propty in amenities_props:
        if propty.contents[1].text == 'Podaci o nekretnini':
            return propty.contents[3]


def get_props_additional(inner_soup):
    amenities_props = inner_soup.findAll('div', {'class': 'property__amenities'})
    for propty in amenities_props:
        if propty.contents[1].text == 'Dodatna opremljenost':
            return propty.contents[3]

def populate():
    total_pages = 1  # 200
    variants = [
        # 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/izdavanje/lista/po-stranici/20/stranica/',
        # 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/lista/po-stranici/20/stranica/',
        'https://www.nekretnine.rs/stambeni-objekti/kuce/lista/po-stranici/20/stranica/'
        ]
    for variant in variants:
        for page in range(total_pages):
            print('Current page number: ' + str(page))
            search_results_url = variant + str(page + 1)
            response = None
            try:
                time.sleep(0.01)
                response = requests.get(search_results_url)
            except:
                try:
                    proxies = get_proxies()
                    proxy_pool = cycle(proxies)
                    proxy = next(proxy_pool)
                    response = requests.get(search_results_url, proxy)
                except:
                    print('Skipping. Connection error')
                    pass
            soup = BeautifulSoup(response.content, "html.parser")
            properties = soup.findAll('div', {'class': 'placeholder-preview-box ratio-1-1'})

            for prop in properties:
                url = 'https://www.nekretnine.rs' + prop.contents[1].attrs['href']

                def run():
                    try:
                        print('Url: ' + url)
                        realty = requests.get(url)
                        inner_soup = BeautifulSoup(realty.content, "html.parser")
                        realty_props = get_props(inner_soup)
                        additional_props = get_props_additional(inner_soup)
                        try:
                            price = get_price(inner_soup)
                        except Exception as exc:
                            price = None
                            print('Error1:', str(exc))
                        try:
                            location_content = inner_soup.findAll('h3', {'class': 'stickyBox__Location'})
                            location = location_content[0].contents[0]
                        except Exception as exc:
                            location = None
                            print('Error2:', str(exc))

                        heating = get_heating(inner_soup)
                        parking = get_parking(inner_soup)
                        num_of_bathrooms = get_bathrooms(inner_soup)
                        elevator = get_elevator(additional_props)
                        balcony = get_balcony(additional_props)

                        if (location is not None) and (',' in location):
                            location = location.split(',', 1)
                            city = location[0].strip()
                            quarter = location[1].strip()
                        else:
                            city = str(location).strip()
                            quarter = None
                        transaction = None
                        category = None
                        square_metrics = None
                        state = None
                        land_area = None
                        registered = False
                        number_of_rooms = None
                        total_floors = None
                        floor = None
                        year_built = None
                        contents_ = None
                        try:
                            contents_ = realty_props.contents[1::2]
                        except:
                            print('no content')
                            time.sleep(5)
                            pass
                        for content in contents_:
                            # print('[', content, ']')
                            if 'Transakcija' in content.contents[0]:
                                if 'Prodaja' in content.contents[0]:
                                    transaction = 'prodaja'
                                else:
                                    transaction = 'izdavanje'
                            if 'Kategorija' in content.contents[0]:
                                # stanovi mogu biti i garsonjere i dupleksi
                                category = ' '.join([cont.string for cont in content.contents])
                                if 'kuća' in category.lower():
                                    category = 'kuca'
                                else:
                                    category = 'stan'
                            if 'Kvadratura' in content.contents[0]:
                                square_metrics = ' '.join([cont.string for cont in content.contents])  # content.contents[1].string
                                square_metrics = square_metrics.replace('Kvadratura:', '')
                                square_metrics = square_metrics.replace('m²', '')
                                square_metrics = square_metrics.strip()
                                square_metrics = float(square_metrics)
                            if 'Stanje nekretnine' in content.contents[0]:
                                state = ' '.join([cont.string for cont in content.contents])
                                state = state.replace('Stanje nekretnine:', '')
                                state = state.strip()
                            if 'Površina zemljišta' in content.contents[0]:
                                land_area = ' '.join([cont.string for cont in content.contents])  # content.contents[0]
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
                                land_area = float(land_area) * increase
                            if 'Uknjiženo' in content.contents[0]:
                                if 'Da' in ' '.join([cont.string for cont in content.contents]):
                                    registered = True
                                else:
                                    registered = False
                            if 'Ukupan broj soba' in content.contents[0]:
                                number_of_rooms = ' '.join([cont.string for cont in content.contents])  # content.contents[0]
                                number_of_rooms = number_of_rooms.replace('Ukupan broj soba:', '')
                                number_of_rooms = number_of_rooms.strip()
                                try:
                                    number_of_rooms = float(number_of_rooms)
                                except ValueError:
                                    number_of_rooms = None
                            if 'Ukupan broj spratova' in content.contents[0]:
                                total_floors = ' '.join([cont.string for cont in content.contents])  # content.contents[0]
                                total_floors = total_floors.replace('Ukupan broj spratova:', '')
                                total_floors = total_floors.strip()
                                try:
                                    total_floors = float(total_floors)
                                except ValueError:
                                    total_floors = None
                            if 'Godina izgradnje' in content.contents[0]:
                                year_built = ' '.join([cont.string for cont in content.contents])
                                year_built = year_built.replace('Godina izgradnje:', '')
                                year_built = year_built.strip()
                                year_built = int(year_built)
                            if 'kupatil' in content.contents[0].lower():
                                bathrooms = ' '.join([cont.string for cont in content.contents])
                                bathrooms = bathrooms.replace('Kupatilo:', '')
                                bathrooms = bathrooms.replace('Broj kupatila:', '')
                                bathrooms = bathrooms.replace('Kupatila:', '')
                                num_of_bathrooms = bathrooms.strip()
                                if num_of_bathrooms == '':
                                    num_of_bathrooms = None
                                try:
                                    num_of_bathrooms = float(num_of_bathrooms)
                                except ValueError:
                                    num_of_bathrooms = None
                            if 'Sprat:' in content.contents[0] or 'Spratnost:' in content.contents[0]:
                                floor = ' '.join([cont.string for cont in content.contents])  # content.contents[0]
                                if 'prizemlje' in floor.lower():  # content.contents[0].lower():
                                    floor = 0
                                else:
                                    floor = floor.replace('Sprat:', '')
                                    floor = floor.replace('Spratnost:', '')
                                    floor = floor.strip()
                                    try:
                                        floor = float(floor)
                                    except Exception:
                                        floor = None

                        data = (category,
                                transaction,
                                heating,
                                city,
                                quarter,
                                url,
                                state,
                                parking,
                                elevator,
                                balcony,
                                registered,
                                square_metrics,
                                year_built,
                                land_area,
                                total_floors,
                                floor,
                                number_of_rooms,
                                num_of_bathrooms,
                                price
                                )
                        # data_base = DataBase()
                        # print('DATA:', data)
                        data_base.add_data(data)

                    except Exception as e:
                        print("Error5:", str(e))
                        return

                try:
                    run()
                except Exception as ext:
                    print(url)
                    print("Error4:", ext)
                    pass


data_base = DataBase()
# #####repository.empty_database()
populate()
data_base.insert_data()
print('SUCCESS')

import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models import AdsModel


def parser(url, pages=999):
    for page in range(pages):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        main_content = soup.find(id="MainContainer")
        ad_elements = main_content.find_all("div", class_="search-item")

        for ad in ad_elements:
            image = ad.find("div", class_="image")
            image = image.find("img")
            try:
                image_url = image['data-src']
            except KeyError:
                image_url = None
            title = ad.find("a", class_="title").text.strip()
            city = ad.find("span", class_="").text.strip()
            date = ad.find("span", class_="date-posted").text.strip()
            # TODO
            if len(date) > 10:
                date = datetime.date.today().strftime("%d-%m-%Y")
            else:
                date = date.replace('/', '-')
            beds = ad.find("span", class_="bedrooms")
            beds = "".join(beds.text.split()[1:])
            description = ad.find("div", class_="description")
            description.div.decompose()
            description = description.text.strip()

            fullprice = ad.find("div", class_="price").text.strip()
            if fullprice == "Please Contact":
                currency = None
                price = None
            else:
                currency = fullprice[0]
                price = float(fullprice[1:].replace(',', ''))
            saving_ad = AdsModel(photo_url=image_url, title=title, city=city,
                                 date=date, beds=beds, description=description,
                                 currency=currency, price=price)
            saving_ad.save_to_db()
        next_page_url = main_content.find("a", attrs={"title": "Next"})
        try:
            next_page_url = next_page_url.get('href')
            url = urljoin(url, next_page_url)
        except AttributeError:
            break

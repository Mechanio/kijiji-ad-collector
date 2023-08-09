import datetime
import json
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from models import AdsModel


def get_data_with_selenium(url):
    """
    Get data about main page for page count by reloading same page with selenium
    :param url:
    :return:
    """
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    opts.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(url=url)
        time.sleep(3)
        driver.refresh()
        time.sleep(22)
        with open("index_sel.html", "w") as file:
            file.write(driver.page_source)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


def parser():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }

    # data = requests.get("https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273", headers=headers)
    # with open("index.html", "w") as file:
    #     file.write(data.text)

    with open("index_sel.html", "r") as file:
        data = file.read()
        soup = BeautifulSoup(data, "lxml")
        # get all pages
        pages_count = int(soup.find("ul", class_="sc-jWEIYm cJqPoY").find_all("li")[-2].text.split()[-1])

        ads_list = []
        count = 0
        for page in range(1, pages_count + 1):
            page_data = requests.get(
                f"https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{page}/c37l1700273",
                headers=headers)
            soup = BeautifulSoup(page_data.text, "lxml")
            main_content = soup.find(id="MainContainer")
            ad_elements = main_content.find_all("div", class_="regular-ad")
            count += 1
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
                if len(date) > 10:
                    date = datetime.date.today().strftime("%d-%m-%Y")
                else:
                    date = date.replace('/', '-')
                try:
                    beds = ad.find("span", class_="bedrooms")
                    beds = "".join(beds.text.split()[1:])
                except Exception as e:
                    print(f"Error-{e}")
                    beds = None
                try:
                    description = ad.find("div", class_="description")
                    description = description.text.strip()
                except Exception as e:
                    print(f"Error-{e}")
                    description = None

                fullprice = ad.find("div", class_="price").text.strip()
                if fullprice == "Please Contact":
                    currency = None
                    price = None
                else:
                    currency = fullprice[0]
                    try:
                        price = float(fullprice[1:].replace(',', ''))
                    except Exception as e:
                        print(f"error - {e}")
                        price = None
                ads_list.append({
                    "photo_url": image_url,
                    "title": title,
                    "city": city,
                    "date": date,
                    "beds": beds,
                    "description": description,
                    "currency": currency,
                    "price": price,
                })
                # saving_ad = AdsModel(photo_url=image_url, title=title, city=city,
                #                      date=date, beds=beds, description=description,
                #                      currency=currency, price=price)
                # saving_ad.save_to_db()
            print(f"Done {page}/{pages_count}")
        with open("data.json", "w") as json_file:
            json.dump(ads_list, json_file, indent=4, ensure_ascii=False)

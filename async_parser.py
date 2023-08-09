import json

from bs4 import BeautifulSoup

import datetime
import asyncio
import aiohttp

ads_list = []


async def get_page_data(session, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }

    async with session.get(url=f"https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{page}/c37l1700273", headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "lxml")
        main_content = soup.find(id="MainContainer")
        ad_elements = main_content.find_all("div", class_="regular-ad")

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
        print(f"Page - {page}")


async def gather_data():
    async with aiohttp.ClientSession() as session:

        with open("index_sel.html", "r") as file:
            data = file.read()
            soup = BeautifulSoup(data, "lxml")
            pages_count = int(soup.find("ul", class_="sc-jWEIYm cJqPoY").find_all("li")[-2].text.split()[-1])
            tasks = []

            for page in range(1, pages_count + 1):
                task = asyncio.Task(get_page_data(session, page))
                tasks.append(task)
            await asyncio.gather(*tasks)


def async_parser():
    asyncio.run(gather_data())
    with open("data_async.json", "w") as json_file:
        json.dump(ads_list, json_file, indent=4, ensure_ascii=False)

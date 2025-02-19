import requests
from bs4 import BeautifulSoup
import csv
import os


print("demarrage du scripts. Veuillez patientez...")
liens = []
categories = []
categories_name = []
en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
           "number_available", "product_description", "category", "review_rating", "image_url"]

if not os.path.exists('images'):
    os.makedirs('images')

site = "https://books.toscrape.com/index.html"
response3 = requests.get(site)


if response3.ok:
    response3.encoding = 'utf8'
    soup3 = BeautifulSoup(response3.text, "html.parser")
    category = soup3.find("ul", class_="nav nav-list").find_all("li")[1:]

for li in category:
    c = li.find('a')
    categor = c["href"]
    categori_name = c.text.strip()
    categories.append("https://books.toscrape.com/" + categor)
    with open(categori_name + " .csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(en_tete)

    url = "https://books.toscrape.com/" + categor
    liens = []
    page_num = 1
    while True:
        url2 = url.replace("index.html", f"page-{page_num}.html") if page_num > 1 else url
        response = requests.get(url2)

        if response.ok:
            response.encoding = 'utf8'
            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.find_all("h3")

        for infos in products:
            a = infos.find('a')
            lien = a['href']
            liens.append("https://books.toscrape.com/catalogue" + lien.replace("../../..", ""))

        if len(products) < 20:
            break
        page_num += 1

    for i in range(len(liens)):
        lien = liens[i].strip()
        response2 = requests.get(lien)
        if response2.ok:
            response2.encoding = "utf8"
            soup2 = BeautifulSoup(response2.text, "html.parser")
            url_prod = response2.url
            upc_prod = soup2.find("th", string="UPC").find_next_sibling("td").text
            title_prod = soup2.find("title").text.strip()
            price_inc_prod = soup2.find("th", string="Price (incl. tax)").find_next_sibling("td").text[1:]
            price_exc_prod = soup2.find("th", string="Price (excl. tax)").find_next_sibling("td").text[1:]
            number_available = soup2.find("th", string="Availability").find_next_sibling("td").text.split()[2][1:]
            try:
                prod_des_prod = soup2.find(id="product_description").find_next_sibling("p").text
            except AttributeError:
                prod_des_prod = "pas de descriptions de produits"
            category_prod = soup2.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
            review_rating_prod = soup2.find(class_="star-rating")['class'][1]
            diction_rev = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            review_rating_prod1 = diction_rev.get(review_rating_prod)
            image_before = soup2.find("img")
            image_url = "https://books.toscrape.com/" + image_before["src"].replace("../..", "")
            image_response = requests.get(image_url)
            image_filename = f"images/{upc_prod}.jpg"
            with open(image_filename, 'wb') as file:
                file.write(image_response.content)

            informations = [url_prod, upc_prod, title_prod, price_inc_prod, price_exc_prod,
                            number_available, prod_des_prod, category_prod, review_rating_prod1, image_url]

            with open(categori_name + " .csv", "a", newline="", encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(informations)
print("Fin du scripts.Merci de consulter les fichiers CSV et le repertoire image")


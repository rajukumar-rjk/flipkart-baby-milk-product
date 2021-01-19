from bs4 import BeautifulSoup
import requests
import csv
from os import path
import re

pageNo = 1
totalPage = 3

csv_file = open('flipkart-baby-milk.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['name', 'product_id', 'rating', 'review_count', 'price'])

while pageNo <= totalPage:
    print('page no -' + str(pageNo))
    if path.isfile('flipkart-baby-milk-'+str(pageNo)+'.html'):
        with open('flipkart-baby-milk-'+str(pageNo)+'.html') as source:
            soup = BeautifulSoup(source, 'html.parser')
    else:
        url = 'https://www.flipkart.com/search?q=baby+milk&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=' + str(
            pageNo)

        source = requests.get(url).content
        soup = BeautifulSoup(source, 'html.parser')

        html_file = open('flipkart-baby-milk-'+str(pageNo)+'.html','w')
        html_file.write(soup.prettify())
        html_file.close()

    for product_div in soup.find_all('div', class_='_13oc-S'):
        for product in product_div.find_all('div', recursive=False):
            name = product.find('a', class_='s1Q9rs').text
            name = " ".join(name.split())

            try:
                link = product.find('a', class_='s1Q9rs')['href']
                link = " ".join(link.split())
                product_id = re.search('pid=(.*)&lid',link)
                product_id = product_id.group(1)
            except:
                product_id = None

            try:
                rating = product.find('div', class_='_3LWZlK').text
                rating = " ".join(rating.split())
            except:
                rating = None

            try:
                review_count = product.find('span', class_='_2_R_DZ').text
                review_count = " ".join(review_count.split())
                review_count = review_count[1:-1]
            except:
                review_count = None

            try:
                price = product.find('div', class_='_30jeq3').text
                price = " ".join(price.split())
            except:
                price = None
            csv_writer.writerow([name, product_id,rating,review_count,price])
    pageNo += 1

csv_file.close()
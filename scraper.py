import csv
import requests
from bs4 import BeautifulSoup

def get_page(url):
    global soup
    response = requests.get(url)
    if not response.ok:
        print('Server Responded:', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail_data(soup):
    try:
        t = soup.find('h1', id='itemTitle').text
        title = t.replace("Details about  ", "").strip()
    except:
        title = ''
    try:
        try:
            p = soup.find('span', id='prcIsum').text.strip()

        except:
            p = soup.find('span', id='prcIsum_bidPrice').text.strip()
        currency, price = p.split(' ')
    except:
        currency = ''
        price = ''
    try:
        sold = soup.find('span', class_='vi-qtyS-hot-red').text.strip().split(' ')[0]
    except:
        sold = ''
    data = {'title': title, 'currency': currency, 'price': price, 'sold': sold}

    return data


def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []
    urls = [item.get('href') for item in links]

    return urls


def write_csv(data):
    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'], data['currency'], data['price'], data['sold']]
        writer.writerow(row)


def main():
    url = 'https://www.ebay.com/sch/i.html?_nkw=perfumes'
    products = get_index_data(get_page(url))

    for link in products:
        data = get_detail_data(get_page(link))
        write_csv(data)
    print("Congratulations")
    print("Data Save Completed")


if __name__ == '__main__':
    main()

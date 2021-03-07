import requests
import json
from bs4 import BeautifulSoup
import glob
import pandas as pd

session = requests.Session()

def login():

    ## Login ke web ecommurz melalui script dibawah dan dibuat mirror pada res.html
    print('login....')
    datas = {
        'username' : 'user',
        'password' : 'user12345'
    }
    res = session.post('http://127.0.0.1:5000/login',data = datas)

    # mengambil jumlah pages

    soup = BeautifulSoup(res.text,'html5lib')

    page_item = soup.find_all('li',attrs={'class':'page-item'})
    total_pages = len(page_item) -2
    return total_pages

def get_urls(page):
    print('getting urls..... page ',format(page))

    params ={
        'page' : page
    }
    ## Get URL for every pages

    res = session.get('http://127.0.0.1:5000/', params=params)

    ##  Mulai mengambil list berdasarkan pagination (jumlah page)

    soup = BeautifulSoup(res.text, 'html5lib')

    titles = soup.find_all('h4', attrs={'class':'card-title'})
    urls = []
    for title in titles:
        url = title.find('a')['href']
        urls.append(url)

    return urls


def get_detail(url):
    print('getting details....{}'.format(url))

    ## get data per products from url
    res = session.get('http://127.0.0.1:5000'+url)

    soup = BeautifulSoup(res.text, 'html5lib')
    title = soup.find('title').text.strip()
    price = soup.find('h4', attrs={'class':'card-price'}).text
    stock = soup.find('span', attrs={'class':'card-stock'}).text.strip().replace('stock: ','')      #clean  'stock:'
    category = soup.find('span', attrs={'class':'card-category'}).text.strip().replace('category: ','')
    description = soup.find('p', attrs={'class':'card-text'}).text.strip().replace('Description: ','')


    dict_data = {
        'title': title,
        'price' : price,
        'stock' : stock,
        'category' : category,
        'description' : description
    }

    with open('./results/{}.json'.format(url.replace('/','')),'w') as outfile:
        json.dump(dict_data,outfile)

def create_csv():
    files = sorted(glob.glob('./results/*.json'))

    datas =[]
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)
    print('creating csv....')

def run():
    ## login into rwidscrapper site
    total_pages = login()

    ## grab all products url
    total_urls = []
    for i in range(total_pages):
        urls = get_urls(i + 1)
        total_urls += urls
    with open('all_urls.json', 'w') as outfile:
        json.dump(total_urls, outfile)

    ## extract all data from products into json files
    with open('all_urls.json') as json_file:
        all_url = json.load(json_file)

    for url in all_url:
        get_detail(url)

    ## create csv files from extracted json data
    create_csv()

if __name__ == '__main__':
    run()
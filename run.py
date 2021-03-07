import requests
import json
from bs4 import BeautifulSoup

session = requests.Session()

def login():

    ## Login ke web ecommurz melalui script dibawah dan dibuat mirror pada res.html
    print('login....')
    datas = {
        'username' : 'user',
        'password' : 'user12345'
    }
    res = session.post('http://127.0.0.1:5000/login',data = datas)

    f = open('./res.html','w+')
    f.write(res.text)
    f.close()

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

    # f = open('./res.html', 'w+')
    # f.write(res.text)
    # f.close()



def get_detail():
    print('getting details....')

def create_csv():
    print('creating csv....')

def run():
    total_pages = login()
    total_urls = []
    for i in range(total_pages):
        urls = get_urls(i + 1)
        total_urls += urls

    with open('all_urls.json', 'w') as outfile:
        json.dump(total_urls, outfile)
    print(total_urls)
    print(len(total_urls))
    get_detail()
    create_csv()

if __name__ == '__main__':
    run()
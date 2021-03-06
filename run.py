import requests
from bs4 import BeautifulSoup

session = requests.Session()

def login():
    print('login....')
    datas = {
        'username' : 'user',
        'password' : 'user12345'
    }
    res = session.post('http://127.0.0.1:5000/login',data = datas)

    f = open('./res.html','w+')
    f.write(res.text)
    f.close

def get_urls():
    print('getting urls.....')

def get_detail():
    print('getting details....')

def create_csv():
    print('creating csv....')

def run():
    login()
    get_urls()
    get_detail()
    create_csv()

if __name__ == '__main__':
    run()
import requests
import json
from api import books_db

URL_API = 'http://127.0.0.1:8000'

def response_treatment(resp: requests.Response):
    '''Print friendly the API response, treating errors'''
    try:
        data = resp.json()
    except ValueError:
        print(f'\nSTATUS: {resp.status_code}')
        print('Response without JSON')
        print(resp.txt)
        return

    if resp.status_code >= 400:
        print(f'\nERROR ({resp.status_code})')
    print(json.dumps(data, indent=4, ensure_ascii=False))
        
def list_books():
    resp = requests.get(f'{URL_API}/books')
    print('\nBooks list: ')
    response_treatment(resp)

def get_book():
    book_uuid = input("What's the book UUID? ").strip()
    resp = requests.get(f'{URL_API}/books/{book_uuid}')
    print('\nBooks details:')
    response_treatment(resp)
    
def menu():
    while True:
        print('\n==== BOOK API CLIENT ====')
        print('1. List books')
        print('2. Get book by UUID')
        print('0. Exit')
        
        option = input('Choose the option: ').strip()
        
        match option:
            case '0': 
                print('Closing client...')
                break
            case '1':
                list_books()
            case '2':
                get_book()

if __name__=='__main__':
    print(books_db)
    menu()
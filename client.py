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
        print(resp.text)
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
    
def insert_book():
    while True:
        print('\nWrite the book informations\n')
        author = input("Author: ")
        if author: 
            title = input("Title: ")
            if title: 
                publisher = input("Publisher: ")
                if publisher:
                    try:
                        year = int(input("Year: "))
                        if year:
                            break
                    except ValueError:
                        print('Year has to be an integer. Try again.')
    payload = {
        'author': author,
        'title': title,
        'publisher': publisher,
        'year': year
    }

    if author and title and publisher and (year >= 0):
        resp = requests.post(f'{URL_API}/books/add', json=payload)
        response_treatment(resp)

def update_book():
    book_uuid = input("What's the book UUID? ").strip()
    
    current_info = requests.get(f'{URL_API}/books/{book_uuid}')
    
    if int(current_info.status_code) == 200:
        print(f'\nCurrent book informations:')
        json_str = current_info.text        
        dict_info = json.loads(json_str)
          
        for key, value in dict_info.items():
            if key.strip().lower() == 'uuid': 
                continue
            else: 
                print(f' - {key.upper()}: {value if key == 'year' else value.capitalize()}')
        while True:
            print('\nWrite the NEW book informations:') 
            author = input("Author: ")
            if author: 
                title = input("Title: ")
                if title: 
                    publisher = input("Publisher: ")
                    if publisher:
                        try:
                            year = int(input("Year: "))
                            if year:
                                break
                        except ValueError:
                            print('Year has to be an integer. Try again.')   
        payload = {
            'author': author,
            'title': title,
            'publisher': publisher,
            'year': year
        }
            
        resp = requests.put(f'{URL_API}/books/{book_uuid}', json=payload)
        response_treatment(resp)
                            
    else:
        print('UUID not found Try a GET method to get the correct UUID.')
           
def partial_update_book():
    book_uuid = input("What's the book UUID? ").strip()
    
    current_info = requests.get(f'{URL_API}/books/{book_uuid}')
    
    if int(current_info.status_code) == 200:
        print(f'\nCurrent book informations:')
        json_str = current_info.text        
        dict_info = json.loads(json_str)
          
        for key, value in dict_info.items():
            if key.strip().lower() == 'uuid': 
                continue
            else: 
                print(f' - {key.upper()}: {value if key == 'year' else value.capitalize()}')
    
        print("\nType the modifications for each field.\nIf you don't want to modify the showed field, just click enter:") 
        author = input("Author: ")
        title = input("Title: ")
        publisher = input("Publisher: ")
        while True:
            year = input("Year: ")
            if year:
                try:
                    int(year)
                    break
                except ValueError:
                    print('Year has to be an integer or null. Try again.')
            else: 
                break
                   
        payload = {}
        
        if author:
            payload['author'] = author
        if title:
            payload['title'] = title
        if publisher:
            payload['publisher'] = publisher
        if year:
            payload['year'] = year
             
        resp = requests.patch(f'{URL_API}/books/update/{book_uuid}', json=payload)
        response_treatment(resp)
                            
    else:
        print('UUID not found Try a GET method to get the correct UUID.')

def menu():
    while True:
        print('\n==== BOOK API CLIENT ====')
        print('1. List books')
        print('2. Get book by UUID')
        print('3. Insert a book')
        print('4. Full update a book')
        print('5. Partial book update')
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
            case '3':
                insert_book()
            case '4':
                update_book()
            case '5':
                partial_update_book()

if __name__=='__main__':
    print(books_db)
    menu()
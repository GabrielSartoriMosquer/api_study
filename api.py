from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI(title='api_livros')

books_db = {
    1: {
        'uuid': uuid4(),
        'author': 'George Orwell',
        'title': '1984',
        'publisher': 'Companhia das Letras',
        'year': 1949
    },
    2: {
        'uuid': uuid4(),
        'author': 'J. K. Rowling',
        'title': 'Harry Potter e a Pedra FIlosofal',
        'publisher': 'Rocco',
        'year': 1997
        }
}

class Book(BaseModel):
    uuid: UUID
    author: str
    title: str
    publisher: str
    year: int
    
class BookPostPut(BaseModel):
    author: str
    title: str
    publisher: str
    year: int
    
class BookPatch(BaseModel):
    author: Optional[str] = None
    title: Optional[str] = None
    publisher: Optional[str] = None
    year: Optional[str] = None
    
# GET - list all books 
@app.get(
    path='/books', 
    response_model=List[Book]
    )
async def list_books() -> List[Book]:
    return [Book(**data) for data in books_db.values()]

# GET - get a specific book 
@app.get(
    path='/books/{book_uuid}', 
    response_model=Book, 
    responses={404: {'description':'book not found'}}
    )
async def get_book(book_uuid: UUID) -> Book:  
    for book in books_db.values():
        if book['uuid'] == book_uuid:
            return Book(**book) # type: ignore
    raise HTTPException(status_code=404, detail='book not found')
    
# POST - book insertion
@app.post(
    path='/books/add', 
    response_model=Book
    )
async def insert_book(book: BookPostPut) -> Book:
    new_uuid = uuid4()
    new_id = max(books_db.keys()) + 1 if books_db else 1
    
    new_book = Book(
        uuid = new_uuid,
        author = book.author,
        title = book.title,
        publisher = book.publisher,
        year = book.year
    )
    
    books_db[new_id] = new_book.model_dump()
    
    return new_book

# PUT - book update
@app.put(
    path='/books/update/{book_uuid}',
    response_model=Book,
    responses={404: {'description':'book not found'}}
    )
async def update_book(book_uuid: UUID, updated_book: BookPostPut) -> Book:
    for ix, book in books_db.items():
            if book['uuid'] == book_uuid:
                books_db[ix] = dict(
                    uuid = book_uuid,
                    author = updated_book.author,
                    title = updated_book.title,
                    publisher = updated_book.publisher,
                    year = updated_book.year
                )
                return Book(**books_db[ix])
    
    raise HTTPException(status_code=404, detail='book not found')

# PATCH - partial book update    
@app.patch(
    path='/books/update/{book_uuid}',
    response_model=Book,
    responses={404: {'description':'book not found'}}
)    
async def update_book_part(book_uuid: UUID, updated_book: BookPatch) -> Book:
    for ix, book in books_db.items():
        if book['uuid'] == book_uuid:
            for key, value in updated_book.model_dump(exclude_defaults=True).items():
                book[key] = value
            
            return Book(**books_db[ix])
    raise HTTPException(status_code=404, detail='book not found')
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
    
# GET - list all books 
@app.get(path='/books', response_model=list[Book])
async def list_books() -> list[Book]:
    return [Book(**data) for data in books_db.values()]

@app.get(path='/books/{book_uuid}', 
         response_model=Book, 
         responses={404: {'description':'book not found'}})
async def get_book(book_uuid: UUID) -> Book:  
    for book in books_db.values():
        if book['uuid'] == book_uuid:
            return Book(**book) # type: ignore
    raise HTTPException(status_code=404, detail='book not found')
        
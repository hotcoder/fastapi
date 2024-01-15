from typing import Optional

from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    rating: int
    published_date: int

    def __init__(self, Id: int, title: str, author: str, rating: int, published_date: int):
        self.id = Id
        self.title = title
        self.author = author
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(None, title="is is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "new book title",
                "author": "new book author",
                "rating": 5,
                "published_date": 2000
            }
        }


BOOKS = [
    Book(1, 'Head First Design', 'Ramesh', 5, 2000),
    Book(2, 'Head Second Software', 'Sai', 4, 1999),
    Book(3, 'Head First GoLanguage', 'Dvishan', 4, 2020),
    Book(4, 'Database internals', 'Dvishan', 5, 2021),
    Book(5, 'Software Arch', 'Sravani', 4, 2022)
]


@app.get('/books' , status_code= status.HTTP_200_OK)
async def books():
    return BOOKS


@app.get('/books/{id}')
async def book(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')


@app.get('/books/')
async def books(rating: int):
    books_by_rating = []
    for book in BOOKS:
        print(book.get("rating"))
        if book.get("rating") == rating:
            books_by_rating.append(book)
    return books_by_rating


@app.post('/books')
async def books(new_book: BookRequest):
    book = Book(**new_book.dict())
    BOOKS.append(find_book_id(book))


@app.put('/books/' ,status_code=status.HTTP_204_NO_CONTENT)
async def books(updated_book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("id") == updated_book.id:
            BOOKS[i] = updated_book


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].get("id") + 1
    # if len(BOOKS) > 0:
    #     book.id = len(BOOKS) + 1
    # else:
    #     book.id = 0
    return book

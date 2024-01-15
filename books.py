import logging

from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'title one', 'author': 'author one', 'description': 'description one'},
    {'title': 'title Horror', 'author': 'author one', 'description': 'description Horror'},
    {'title': 'title Comedy Horror', 'author': 'author one', 'description': 'description Horror'},
    {'title': 'title two', 'author': 'author two', 'description': 'description two'},
    {'title': 'title three', 'author': 'author three', 'description': 'description three'},
    {'title': 'title four', 'author': 'author four', 'description': 'description four'},
    {'title': 'title five', 'author': 'author five', 'description': 'description five'},
    {'title': 'title six', 'author': 'author six', 'description': 'description six'}
]


@app.get('/books')
async def books():
    return BOOKS


@app.get('/books/{title}')
async def book_by_title(title):
    for book in BOOKS:
        if book.get('title').casefold() == title.casefold():
            return book


@app.get('/books/')
async def book_by_title(author: str):
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            return book


@app.get('/books/{author}/')
async def book_by_title(author: str, description: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold() and \
                book.get('description').casefold() == description.casefold():
            books_to_return.append(book)

    return books_to_return


@app.post('/books/')
async def books(new_book=Body()):
    BOOKS.append(new_book)


@app.put('/books')
async def books(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete('/books/{title}/')
def books(title):
    for i in range(len(BOOKS)):
        print(BOOKS[i])
        if BOOKS[i].get('title').casefold() == title.casefold():
            BOOKS.pop(i)
            return
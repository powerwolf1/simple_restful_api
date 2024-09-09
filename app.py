from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
import models
import schemas
import crud
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.post("/books/")
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
async def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.Book)
async def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db_book.title = book.title
    db_book.author = book.author
    db_book.year = book.year

    crud.update_book(db=db, book_id=book_id, book=book)
    return db_book


@app.delete("/books/{book_id}", response_model=schemas.Book)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    crud.delete_book(db=db, book_id=book_id)
    return db_book





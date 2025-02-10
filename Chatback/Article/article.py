from fastapi import APIRouter, HTTPException
from models import BookSeries, Books, Chapters

article = APIRouter()


@article.get("/getbooks")
async def get_books():
    result = []
    bookseries = await BookSeries.all()
    for bookserie in bookseries:
        books = await bookserie.books.all()
        book = books[0]
        chapters = await book.chapters.all()
        chapter = chapters[0]
        result.append({
            "id": bookserie.id,
            "title": bookserie.name,
            "chapter_first_id": chapter.id
        })
    # 获取所有books里面series_id为null的
    books = await Books.filter(series__id__isnull=True).all()
    for book in books:
        chapters = await book.chapters.all()
        chapter = chapters[0]
        result.append({
            "id": book.id,
            "title": book.name,
            "chapter_first_id": chapter.id
        })
    # 获取chapters里面book_id为null的
    chapters = await Chapters.filter(book__id__isnull=True).all()
    for chapter in chapters:
        result.append({
            "id": chapter.id,
            "title": chapter.name,
            "chapter_first_id": chapter.id
        })

    return {
        "success": True,
        "result": result
    }

# {
#     "success": "true",
#     "result": [{
#         "id": 1,
#         "title": "xxx",
#         "chapter_id": 5
#     },{
#         "id":11,
#         "title": "xxx",
#         "chapter_id": 5
#     }]
# }

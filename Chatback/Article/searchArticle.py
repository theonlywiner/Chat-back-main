from fastapi import APIRouter, Response, status, Query
from pydantic import BaseModel
from tortoise.queryset import Q
from models import BookSeries, Books, Chapters

from models import BookSeries

searchArticle = APIRouter()


class get_articles(BaseModel):
    startIndex: int
    endIndex: int


@searchArticle.get("/getArticleList")
async def get_article_list(response: Response, startIndex: int = Query(..., ge=0), endIndex: int = Query(..., ge=0)):
    try:
        article_list = []
        chapters = await Chapters.filter(id__gte=startIndex + 2, id__lte=endIndex + 1)
        for chapter in chapters:
            # 尝试获取关联的Book记录
            book = await chapter.book
            book_name = book.name + "-" if book else ""

            # 尝试获取关联的BookSeries记录
            series = await book.series if book else None
            series_name = series.name + "-" if series else ""
            article_list.append(
                {
                    "id": chapter.id,
                    "title": series_name + book_name + chapter.name,
                    "author": "xxx",
                    "description": chapter.full_ancient_content[:20],
                    "dynasty": "xxx"
                }
            )

        total = await Chapters.all().count()

        return {
            "success": True,
            "result": {
                "total": total,
                "list": article_list
            }
        }
    except Exception as e:
        # 捕获其他异常
        print(f"异常信息：{e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "message": f"系统错误: {str(e)}"
        }


@searchArticle.get("/getArticleDetail")
async def get_article_detail(response: Response, id: int = Query(..., ge=0)):
    navTreeData = []
    try:
        chapter = await Chapters.get(id=id)
        paragraphs = await chapter.paragraphs
        related_book = await chapter.book
        related_serie = await related_book.series if related_book else None
        if related_serie:
            books_all = await related_serie.books.all()
            children_book_all = []
            for book in books_all:
                chapters_all = await book.chapters.all()
                children_chapter_all = [
                    {
                        "id": chapter.id,
                        "label": chapter.name
                    }
                    for chapter in chapters_all
                ]
                children_book = {
                    "id": book.name,
                    "label": book.name,
                    "children": children_chapter_all
                }
                children_book_all.append(children_book)

            navTreeData = [{
                "id": related_serie.name,
                "label": related_serie.name,
                "children": children_book_all
            }]
        elif related_book:
            chapters_all = await related_book.chapters.all()
            children_chapter_all = [
                {
                    "id": chapter.id,
                    "label": chapter.name
                }
                for chapter in chapters_all
            ]
            navTreeData = [{
                "id": related_book.name,
                "label": related_book.name,
                "children": children_chapter_all
            }]
        else:
            navTreeData = [{
                "id": chapter.id,
                "label": chapter
            }]

        content_list = []
        for paragraph in paragraphs:
            content_list.append({
                "ancient_content": paragraph.ancient_text,
                "modern_content": paragraph.modern_text
            })
        return {
            "success": True,
            "result": {
                "title": chapter.name,
                "author": "xxx",
                "dynasty": "xxx",
                "content": chapter.full_ancient_content,
                "content_list": content_list,
                "translation": chapter.full_modern_content,
                "notes": "xxx"
            },
            "navTreeData": navTreeData
        }
    except Exception as e:
        # 捕获其他异常
        print(f"异常信息：{e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "message": f"系统错误: {str(e)}"
        }


@searchArticle.get("/searchArticle")
async def search_article(response: Response, title: str = Query(None)):
    # 保存所有查找到的chapters
    chapters_all = []
    if title is not None:
        for model in [BookSeries, Books, Chapters]:
            results = await model.filter(Q(name__icontains=title))
            for result in results:
                # 数据在Chapters
                if isinstance(result, Chapters):
                    chapters_all.append(result)
                # 数据在 Books里面
                elif isinstance(result, Books):
                    related_chapters = await result.chapters.all()
                    chapters_all.extend(related_chapters)
                # # 数据在BookSeries里面
                elif isinstance(result, BookSeries):
                    related_books = await result.books.all()
                    for book in related_books:
                        related_chapters = await book.chapters.all()
                        chapters_all.extend(related_chapters)

    # 去重
    unique_chapters = []
    chapter_ids = set()
    for chapter in chapters_all:
        if chapter.id not in chapter_ids:
            # author_info = await chapter.author
            # print(author_info.id)
            # print(author_info.dynasty)

            # 尝试获取关联的Book记录
            book = await chapter.book
            book_name = book.name + "-" if book else ""

            # 尝试获取关联的BookSeries记录
            series = await book.series if book else None
            series_name = series.name + "-" if series else ""

            chapter.name = series_name + book_name + chapter.name

            unique_chapters.append(chapter)
            chapter_ids.add(chapter.id)

    result_list = []
    for chapter in unique_chapters:
        result_list.append({
            "id": chapter.id,
            "title": chapter.name,
            "author": "xxx",
            "description": chapter.full_ancient_content[:20],
            "dynasty": "xxx"
        })

    return {
        "success": True,
        "result": {
            "total": len(result_list),
            "list": result_list
        }
    }

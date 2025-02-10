from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from models import Paragraphs, Chapters, Books, BookSeries, Authors
# from ai.apikey import ZhiPu

ai_response = APIRouter()
# zhipu = ZhiPu("c94b92b94a1d46db867ef57d77187c89.ZlF2AlE53yfMd8Pv", 2)


class Query(BaseModel):
    query: str


@ai_response.post('/query')
async def query_content(query_info: Query, response: Response):
    query_text = query_info.query
    print('接收到的查询文本:', query_text)
    
    try:
        # 查找段落
        paragraph = await Paragraphs.filter(ancient_text__icontains=query_text).first()

        if not paragraph:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                'success': False,
                'message': '未找到匹配内容'
            }

        # 调用智谱AI分析古文
        # response = zhipu.zhipuai_chat(f"请解析这句古文（如果存在实虚词，断句划分等等），"
        #                               f"要求只需要按照下面回答结果回答并且不带*号："
        #                               f"实虚词为："
        #                               f"x（实或者虚）并且给出对应的解析；"
        #                               f"段落分句为："
        #                               f"{paragraph.ancient_text}")
        #
        # # 正确提取 content 内容
        # ai_result = response.choices[0].message.content if response else "AI分析失败"

        # 通过外键ID查找关联数据
        # chapter = await Chapters.filter(id=paragraph.chapter_id).first()
        # if chapter:
        #     author = await Authors.filter(id=chapter.author_id).first()
        #     book = await Books.filter(id=chapter.book_id).first()
        #     if book:
        #         series = await BookSeries.filter(id=book.series_id).first()
        #     else:
        #         series = None
        # else:
        #     author = None
        #     book = None
        #     series = None
        chapter = await paragraph.chapter
        chapter_name = chapter.name if chapter else None
        author = await chapter.author
        author_name = author.info if author else None
        book = await chapter.book
        book_name = book.name if book else None
        series = await book.series if book else None
        series_name = series.name if series else None

        result = {
            'ancient_text': paragraph.ancient_text,
            'modern_text': paragraph.modern_text,
            'chapter_name': chapter_name,
            'author_name': author_name,
            'book_name': book_name,
            'series_name': series_name,
            # 'ai_analysis': ai_result
        }
        
        return {
            'success': True,
            'result': result
        }
        
    except Exception as e:
        print('查询错误:', str(e))
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False,
            'message': f'查询错误: {str(e)}'
        }

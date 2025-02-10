from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware

from config import TORTOISE_ORM, FASTAPI_CONFIG
from User.user import user
from ai.ai_response import ai_response
from Article.searchArticle import searchArticle
from Article.article import article

app = FastAPI(**FASTAPI_CONFIG)

app.include_router(user, tags=["用户操作系统"])
app.include_router(ai_response, tags=["ai回答"])
app.include_router(searchArticle, tags=["文章获取"])
app.include_router(article, tags=["首页获取"])

origins = ['*']
# 跨域问题解决
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 注册 Tortoise ORM
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080, reload=True)

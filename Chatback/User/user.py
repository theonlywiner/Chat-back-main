import logging
from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel, constr, field_validator
from models import User
import bcrypt

# 配置日志记录
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

user = APIRouter()


class Users(BaseModel):
    """
    用户模型，用于接收登录和注册请求中的用户信息。
    """
    username: constr(min_length=1, max_length=10)
    password: constr(min_length=6, max_length=15, pattern=r'^\S{6,15}$')

    @field_validator('username', 'password', mode='before')
    def strip_whitespace(cls, v):
        """
        去除用户名和密码前后的空格。
        """
        return v.strip()


def set_response(response, status_code, success, message):
    """
    设置响应状态码和返回信息。
    """
    response.status_code = status_code
    return {
        "success": success,
        "message": message
    }


# 登录
@user.post("/login", summary="用户登录", description="用户使用用户名和密码进行登录")
async def login(user_info: Users, response: Response):
    try:
        if not user_info.username or not user_info.password:
            return set_response(response, status.HTTP_400_BAD_REQUEST, False, "用户名和密码不能为空")

        # 查询用户
        get_user = await User.filter(username=user_info.username).first()

        if get_user and bcrypt.checkpw(user_info.password.encode('utf-8'), get_user.password.encode('utf-8')):
            return {
                "success": True,
                "message": "登录成功",
                "username": user_info.username
            }
        else:
            return set_response(response, status.HTTP_401_UNAUTHORIZED, False, "用户名或密码错误")

    except Exception as e:
        logger.error(f"登录异常：{e}")
        return set_response(response, status.HTTP_500_INTERNAL_SERVER_ERROR, False, "系统错误，请稍后重试")


@user.post("/register", summary="用户注册", description="用户使用用户名和密码进行注册")
async def register(user_info: Users, response: Response):
    try:
        get_user = await User.filter(username=user_info.username).first()
        if get_user:
            return set_response(response, status.HTTP_400_BAD_REQUEST, False, "用户名已存在")

        # 对密码进行哈希处理
        hashed = bcrypt.hashpw(user_info.password.encode('utf-8'), bcrypt.gensalt())
        user_d = user_info.dict()
        user_d['password'] = hashed.decode('utf-8')

        await User.create(**user_d)
        return set_response(response, status.HTTP_201_CREATED, True, "注册成功")
    except Exception as e:
        logger.error(f"注册异常：{e}")
        return set_response(response, status.HTTP_500_INTERNAL_SERVER_ERROR, False, "注册失败，请稍后重试")
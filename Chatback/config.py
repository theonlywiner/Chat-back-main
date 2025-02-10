from typing import Dict, List

TORTOISE_ORM: Dict[str, Dict] = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',  # Mysql or Mariadb
            'credentials': {
                'host': 'localhost',
                'port': 3306,
                'user': 'root',
                'password': '123456',
                'database': 'chatchat',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4',
                'echo': True  # 是否打印SQL语句
            }
        }
    },
    'apps': {
        'models': {
            'models': ['models', 'aerich.models'],  # 对应的模型类
            'default_connection': 'default'
        }
    }
}


# FastAPI 应用配置
FASTAPI_CONFIG = {

    "title": "ChatChat API",

    "description": "古文学习平台API",

    "version": "1.0.0",

}

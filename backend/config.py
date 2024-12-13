import os

class Config:
    # MySQL配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:123456@localhost:3306/ChatChat'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
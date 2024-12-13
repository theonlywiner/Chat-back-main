from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Content, Books
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

# 注册路由
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400
    
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '注册成功'}), 201

# 登录路由
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': '用户名和密码不能为空'
            }), 400
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return jsonify({
                'success': True,
                'message': '登录成功',
                'username': username
            }), 200
        
        return jsonify({
            'success': False,
            'message': '用户名或密码错误'
        }), 401
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'登录失败: {str(e)}'
        }), 500

# 内容查询路由
@app.route('/query', methods=['POST'])
def query_content():
    data = request.get_json()
    query_text = data.get('query')
    
    print('查询文本:', query_text)
    
    try:
        content = Content.query.filter(
            Content.ancient_text.like(f'%{query_text}%')
        ).first()
        
        print('查询结果:', content)
        
        if content:
            return jsonify({
                'ancient_text': content.ancient_text,
                'modern_text': content.modern_text,
                'book_id': content.book_id,
                'book_name': content.book.book_name
            }), 200
        return jsonify({'message': '未找到匹配内容'}), 404
    except Exception as e:
        print('查询错误:', str(e))
        return jsonify({'message': f'查询出错: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
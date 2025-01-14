from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Books, Paragraphs, Chapters, BookSeries, Authors
from config import Config
from apikey import ZhiPu  # 导入 ZhiPu 类

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

# 初始化 ZhiPu 实例
zhipu = ZhiPu("c94b92b94a1d46db867ef57d77187c89.ZlF2AlE53yfMd8Pv", 2)

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
    
    print('接收到的查询文本:', query_text)
    
    try:
        search_pattern = f"{query_text}%"
        print('使用的查询模式:', search_pattern)
        
        paragraph = Paragraphs.query.filter(
            Paragraphs.ancient_text.ilike(search_pattern)
        ).first()
        
        print('查询结果:', paragraph)
        
        if paragraph:
            # 调用智谱AI分析古文
            response = zhipu.zhipuai_chat(f"请解析这句古文（如果存在实虚词，断句划分等等），"
                                          f"要求只需要按照下面回答结果回答并且不带*号："
                                          f"实虚词为："
                                          f"x（实或者虚）并且给出对应的解析；"
                                          f"段落分句为："
                                          f"{paragraph.ancient_text}")
            
            # 正确提取 content 内容
            ai_result = response.choices[0].message.content if response else "AI分析失败"
            
            # 处理可能为 null 的关系
            result = {
                'ancient_text': paragraph.ancient_text,
                'modern_text': paragraph.modern_text,
                'chapter_name': paragraph.chapter.name if paragraph.chapter else None,
                'author_name': paragraph.chapter.author.info if paragraph.chapter and paragraph.chapter.author else None,
                'book_name': paragraph.chapter.book.name if paragraph.chapter and paragraph.chapter.book else None,
                'series_name': paragraph.chapter.book.series.name if paragraph.chapter and paragraph.chapter.book and paragraph.chapter.book.series else None,
                'ai_analysis': ai_result
            }
            return jsonify(result), 200
            
        return jsonify({'message': '未找到匹配内容'}), 404
    except Exception as e:
        print('查询错误:', str(e))
        return jsonify({'message': f'查询出错: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
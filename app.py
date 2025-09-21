import os
from flask import Flask, render_template, session, g, current_app
from config import Config
from models import db, UserInfo, HouseInfo, HouseRecommend

# 引入蓝图
from auth import auth_bp
from property import property_bp
from search import search_bp
from analytics import analytics_bp
from recommend import recommend_bp

app = Flask(__name__)

# 配置静态文件和模板目录
app.template_folder = 'templates'
app.static_folder = 'static'

app.config.from_object(Config)

# 确保 SECRET_KEY 存在
if not app.config.get('SECRET_KEY'):
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)

# 初始化数据库
db.init_app(app)

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(property_bp)
app.register_blueprint(search_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(recommend_bp)

# 创建一个标志来跟踪是否已初始化数据库
db_initialized = False

@app.before_request
def before_first_request():
    global db_initialized
    if not db_initialized:
        with app.app_context():
            db.create_all()
        db_initialized = True

# 主页路由
@app.route('/')
def index():
    # 显示最新的房源（直接从house_info表中获取数据）
    with app.app_context():
        # 从house_info表中获取最新的6条房源数据
        house_infos = HouseInfo.query.order_by(HouseInfo.publish_time.desc()).limit(6).all()
        if house_infos:
            # 转换house_info为properties显示
            properties = [house_info.to_property() for house_info in house_infos]
        else:
            properties = []
    return render_template('index.html', properties=properties)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
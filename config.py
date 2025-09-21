from flask_sqlalchemy import SQLAlchemy  #Flask 的 SQLAlchemy 扩展，用于简化数据库操作（ORM）。
# Python 的 MySQL 客户端库，用于连接 MySQL 数据库
import pymysql 
import os

# 这行代码让 pymysql 模拟 MySQLdb 的行为，使 SQLAlchemy 可以使用 pymysql 作为 MySQL 驱动。
pymysql.install_as_MySQLdb()

# 创建flask-sqlalchemy的实例对象
db = SQLAlchemy()

class Config:
    # 调试模式
    DEBUG = False
    # 指定数据库的链接地址  dialect+driver://username:password@host:port/database
    # dialect：数据库的类型，这里是 mysql，表示使用 MySQL 数据库
    # driver：数据库驱动程序，这里没有指定，默认使用 pymysql。
    # username 和 password：数据库的用户名和密码，这里是 root。
    # host：数据库服务器的地址，这里是 127.0.0.1，表示本地。
    # database：数据库的名称，这里是 house。
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASS', 'root')}@127.0.0.1/house"
    # 用来控制 Flask-SQLAlchemy 是否追踪对象的修改，并发送信号。默认值是 True，但在生产环境中最好设置为 False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

 # 设置连接池相关参数
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 3600  # 1 小时后强制重连
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserInfo(db.Model):
    """用户信息表"""
    __tablename__ = 'user_info'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    addr = db.Column(db.String(200))
    collect_id = db.Column(db.Text)
    seen_id = db.Column(db.Text)
    
    def set_password(self, password):
        """设置用户密码"""
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """检查用户密码"""
        return check_password_hash(self.password, password)
        
    def __repr__(self):
        return f'<UserInfo {self.name}>'

class HouseInfo(db.Model):
    """房源信息表"""
    __tablename__ = 'house_info'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    rooms = db.Column(db.String(50))
    area = db.Column(db.Float)
    price = db.Column(db.Float)
    direction = db.Column(db.String(50))
    rent_type = db.Column(db.String(50))
    region = db.Column(db.String(100))
    block = db.Column(db.String(100))
    address = db.Column(db.String(200))
    traffic = db.Column(db.Text)
    publish_time = db.Column(db.Integer)  # Unix时间戳
    facilities = db.Column(db.Text)
    highlights = db.Column(db.Text)
    matching = db.Column(db.Text)
    travel = db.Column(db.Text)
    page_views = db.Column(db.Integer)
    landlord = db.Column(db.String(100))
    phone_num = db.Column(db.String(20))
    house_num = db.Column(db.String(50))
    
    def to_property(self):
        """将HouseInfo转换为Property对象用于展示"""
        # 解析rooms字段获取卧室和浴室数量
        bedrooms = 1
        bathrooms = 1
        if self.rooms:
            if '室' in self.rooms:
                try:
                    bedrooms = int(self.rooms.split('室')[0]) if self.rooms.split('室')[0].isdigit() else 1
                except:
                    bedrooms = 1
            if '厅' in self.rooms:
                try:
                    bathroom_info = self.rooms.split('室')[1] if '室' in self.rooms else self.rooms
                    if '卫' in bathroom_info:
                        bathrooms = int(bathroom_info.split('卫')[0]) if bathroom_info.split('卫')[0].isdigit() else 1
                except:
                    bathrooms = 1
        
        # 创建Property对象
        prop = Property()
        prop.id = self.id
        prop.title = self.title or '未命名房源'
        prop.description = self.facilities or self.highlights or '暂无描述'
        prop.address = self.address or self.region or '地址未知'
        prop.city = self.region or '未知城市'
        prop.state = self.block or '未知区域'
        prop.zipcode = '000000'
        prop.price = self.price or 0
        prop.bedrooms = bedrooms
        prop.bathrooms = bathrooms
        prop.square_feet = self.area or 0
        prop.property_type = self.rent_type or '整租'
        prop.year_built = None
        prop.owner_id = 1  # 默认用户
        
        return prop
    
    def __repr__(self):
        return f'<HouseInfo {self.title}>'

class HouseRecommend(db.Model):
    """房源推荐表"""
    __tablename__ = 'house_recommend'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    house_id = db.Column(db.Integer)
    score = db.Column(db.Float)
    # 移除了created_at字段，因为它在实际表中不存在
    
    def __repr__(self):
        return f'<HouseRecommend user_id={self.user_id} house_id={self.house_id} score={self.score}>'

class Property:
    """房源展示类（非数据库表）"""
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.address = None
        self.city = None
        self.state = None
        self.zipcode = None
        self.price = None
        self.bedrooms = None
        self.bathrooms = None
        self.square_feet = None
        self.property_type = None
        self.year_built = None
        self.owner_id = None
        self.created_at = None
        self.updated_at = None
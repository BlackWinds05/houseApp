from flask import Blueprint, render_template, current_app
from models import db, HouseInfo, UserInfo, HouseRecommend

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
def dashboard():
    """数据分析仪表板"""
    with current_app.app_context():
        # 获取统计数据
        total_properties = HouseInfo.query.count()
        total_users = UserInfo.query.count()
        total_recommendations = HouseRecommend.query.count()
        
        # 按城市统计房源数量
        properties_by_city = db.session.query(
            HouseInfo.region, 
            db.func.count(HouseInfo.id)
        ).group_by(HouseInfo.region).all()
    
    return render_template('analytics/dashboard.html', 
                          total_properties=total_properties,
                          total_users=total_users,
                          total_recommendations=total_recommendations,
                          properties_by_city=properties_by_city)
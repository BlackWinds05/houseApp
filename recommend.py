from flask import Blueprint, render_template, session, current_app
from models import HouseInfo, HouseRecommend
import random

recommend_bp = Blueprint('recommend', __name__)

@recommend_bp.route('/recommend')
def recommend():
    """房源推荐"""
    recommended_properties = []
    
    with current_app.app_context():
        # 如果用户已登录，尝试从推荐表中获取推荐
        if 'user_id' in session:
            user_id = session['user_id']
            # 获取用户的推荐房源
            recommendations = HouseRecommend.query.filter_by(user_id=user_id)\
                .order_by(HouseRecommend.score.desc())\
                .limit(6).all()
            
            if recommendations:
                # 根据推荐ID获取房源信息
                house_ids = [rec.house_id for rec in recommendations]
                house_infos = HouseInfo.query.filter(HouseInfo.id.in_(house_ids)).all()
                recommended_properties = [house_info.to_property() for house_info in house_infos]
            else:
                # 如果没有推荐数据，则随机推荐
                house_infos = HouseInfo.query.order_by(HouseInfo.publish_time.desc()).limit(6).all()
                recommended_properties = [house_info.to_property() for house_info in house_infos]
        else:
            # 未登录用户推荐最新房源
            house_infos = HouseInfo.query.order_by(HouseInfo.publish_time.desc()).limit(6).all()
            recommended_properties = [house_info.to_property() for house_info in house_infos]
    
    return render_template('recommend/index.html', properties=recommended_properties)
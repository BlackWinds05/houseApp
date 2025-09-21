from flask import Blueprint, render_template, request, current_app
from models import HouseInfo

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    """房源搜索"""
    keyword = request.args.get('keyword', '').strip()
    city = request.args.get('city', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    bedrooms = request.args.get('bedrooms', type=int)
    
    # 构建查询
    with current_app.app_context():
        query = HouseInfo.query
        
        if keyword:
            query = query.filter(HouseInfo.title.contains(keyword) | HouseInfo.facilities.contains(keyword) | HouseInfo.highlights.contains(keyword))
        
        if city:
            query = query.filter(HouseInfo.region == city)
        
        if min_price is not None:
            query = query.filter(HouseInfo.price >= min_price)
        
        if max_price is not None:
            query = query.filter(HouseInfo.price <= max_price)
        
        if bedrooms is not None:
            query = query.filter(HouseInfo.rooms.contains(f"{bedrooms}室"))
        
        page = request.args.get('page', 1, type=int)
        house_infos = query.paginate(page=page, per_page=10)
        # 转换为Property对象用于展示
        properties = [house_info.to_property() for house_info in house_infos.items]
    
    return render_template('search/results.html', 
                          house_infos=house_infos,
                          properties=properties,
                          keyword=keyword,
                          city=city,
                          min_price=min_price,
                          max_price=max_price,
                          bedrooms=bedrooms)
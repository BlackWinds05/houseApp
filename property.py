from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models import db, HouseInfo
from functools import wraps

property_bp = Blueprint('property', __name__)

def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录！', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录！', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash('您没有权限执行此操作！', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@property_bp.route('/properties')
def list_properties():
    """房源列表"""
    page = request.args.get('page', 1, type=int)
    with current_app.app_context():
        # 直接从house_info表中获取数据
        house_infos = HouseInfo.query.paginate(page=page, per_page=10)
        # 转换为Property对象用于展示
        properties = [house_info.to_property() for house_info in house_infos.items]
    return render_template('property/list.html', house_infos=house_infos, properties=properties)

@property_bp.route('/property/<int:property_id>')
def view_property(property_id):
    """查看房源完整详情"""
    with current_app.app_context():
        house_info = HouseInfo.query.get_or_404(property_id)
    return render_template('property/detail_full.html', house_info=house_info)

@property_bp.route('/property/<int:property_id>/simple')
def view_property_simple(property_id):
    """查看房源简要详情"""
    with current_app.app_context():
        house_info = HouseInfo.query.get_or_404(property_id)
        # 转换为Property对象用于展示
        property_obj = house_info.to_property()
    return render_template('property/detail.html', property=property_obj)

@property_bp.route('/property/create', methods=['GET', 'POST'])
@login_required
def create_property():
    """创建房源（这个功能在直接使用数据库的情况下可能不需要）"""
    if request.method == 'POST':
        # 在直接使用现有数据库的模式下，我们不实现创建功能
        flash('在当前模式下不支持创建房源。', 'warning')
        return redirect(url_for('property.list_properties'))
    
    return render_template('property/create.html')

@property_bp.route('/property/<int:property_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    """编辑房源（这个功能在直接使用数据库的情况下可能不需要）"""
    with current_app.app_context():
        house_info = HouseInfo.query.get_or_404(property_id)
    
    # 在直接使用现有数据库的模式下，我们不实现编辑功能
    flash('在当前模式下不支持编辑房源。', 'warning')
    return redirect(url_for('property.view_property', property_id=property_id))

@property_bp.route('/property/<int:property_id>/delete', methods=['POST'])
@login_required
def delete_property(property_id):
    """删除房源（这个功能在直接使用数据库的情况下可能不需要）"""
    # 在直接使用现有数据库的模式下，我们不实现删除功能
    flash('在当前模式下不支持删除房源。', 'warning')
    return redirect(url_for('property.list_properties'))
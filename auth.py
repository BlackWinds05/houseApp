from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models import db, UserInfo

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with current_app.app_context():
            # 从user_info表中读取用户信息
            user = UserInfo.query.filter_by(name=username).first()
        
        # 检查用户是否存在且密码正确
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.name
            session['role'] = 'user'  # 默认为普通用户
            flash('登录成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误！', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        with current_app.app_context():
            # 检查用户名是否已存在
            if UserInfo.query.filter_by(name=username).first():
                flash('用户名已存在！', 'danger')
                return render_template('auth/register.html')
            
            # 检查邮箱是否已存在
            if UserInfo.query.filter_by(email=email).first():
                flash('邮箱已被注册！', 'danger')
                return render_template('auth/register.html')
            
            # 检查密码是否一致
            if password != confirm_password:
                flash('两次输入的密码不一致！', 'danger')
                return render_template('auth/register.html')
            
            # 创建新用户并写入user_info表
            user = UserInfo(name=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        
        flash('注册成功！请登录。', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('您已成功退出登录。', 'info')
    return redirect(url_for('index'))
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from . import auth_bp
from app import db
from models.user import User
from models.customer import Customer
from models.employee import Employee

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '请提供用户名和密码'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
    refresh_token = create_refresh_token(identity=user.id)
    
    # 获取用户详细信息
    if user.role == 'customer':
        profile = Customer.query.filter_by(user_id=user.id).first()
    elif user.role == 'employee':
        profile = Employee.query.filter_by(user_id=user.id).first()
    else:
        profile = None
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'profile': profile.to_dict() if profile else None
        }
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({'error': '请提供用户名、密码和角色'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    # 创建用户
    from werkzeug.security import generate_password_hash
    user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        role=data['role']
    )
    db.session.add(user)
    db.session.flush()  # 获取用户ID但不提交事务
    
    # 创建对应的用户资料
    if data['role'] == 'customer':
        profile = Customer(
            user_id=user.id,
            name=data.get('name', ''),
            age=data.get('age', 0),
            gender=data.get('gender', ''),
            contact=data.get('contact', ''),
            dietary_restrictions=data.get('dietary_restrictions', ''),
            preferences=data.get('preferences', '')
        )
        db.session.add(profile)
    elif data['role'] == 'employee':
        profile = Employee(
            user_id=user.id,
            name=data.get('name', ''),
            position=data.get('position', ''),
            contact=data.get('contact', ''),
            base_salary=data.get('base_salary', 0),
            education=data.get('education', ''),
            work_experience=data.get('work_experience', '')
        )
        db.session.add(profile)
    
    db.session.commit()
    
    return jsonify({'message': '注册成功'}), 201

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # 在实际应用中，可能需要将令牌加入黑名单
    return jsonify({'message': '退出成功'}), 200

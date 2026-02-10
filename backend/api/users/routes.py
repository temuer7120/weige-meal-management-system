from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from . import users_bp
from models.user import User
from models.customer import Customer
from models.employee import Employee
from app import db

@users_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 获取用户详细信息
    if user.role == 'customer':
        profile = Customer.query.filter_by(user_id=user.id).first()
    elif user.role == 'employee':
        profile = Employee.query.filter_by(user_id=user.id).first()
    else:
        profile = None
    
    return jsonify({
        'user': user.to_dict(),
        'profile': profile.to_dict() if profile else None
    }), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        # 只有管理员可以更新其他用户信息
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': '无权限更新其他用户信息'}), 403
    
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 更新用户信息
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    if 'role' in data and User.query.get(current_user_id).role == 'admin':
        user.role = data['role']
    
    # 更新用户资料
    if user.role == 'customer':
        profile = Customer.query.filter_by(user_id=user.id).first()
        if profile and 'profile' in data:
            profile_data = data['profile']
            for key, value in profile_data.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
    elif user.role == 'employee':
        profile = Employee.query.filter_by(user_id=user.id).first()
        if profile and 'profile' in data:
            profile_data = data['profile']
            for key, value in profile_data.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
    
    db.session.commit()
    return jsonify({'message': '用户信息更新成功'}), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # 只有管理员可以删除用户
    user = User.query.get(get_jwt_identity())
    if not user or user.role != 'admin':
        return jsonify({'error': '无权限删除用户'}), 403
    
    user_to_delete = User.query.get(user_id)
    if not user_to_delete:
        return jsonify({'error': '用户不存在'}), 404
    
    # 删除关联的用户资料
    if user_to_delete.role == 'customer':
        profile = Customer.query.filter_by(user_id=user_id).first()
        if profile:
            db.session.delete(profile)
    elif user_to_delete.role == 'employee':
        profile = Employee.query.filter_by(user_id=user_id).first()
        if profile:
            db.session.delete(profile)
    
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({'message': '用户删除成功'}), 200

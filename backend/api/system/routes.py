from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import system_bp
from ...models.system import OperationLog, Permission, RolePermission
from ...models.user import User
from ... import db

@system_bp.route('/permissions', methods=['GET'])
@jwt_required()
def get_permissions():
    # 检查用户是否为管理员
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': '无权限访问'}), 403
    
    permissions = Permission.query.all()
    return jsonify([permission.to_dict() for permission in permissions]), 200

@system_bp.route('/permissions', methods=['POST'])
@jwt_required()
def create_permission():
    # 检查用户是否为管理员
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': '无权限操作'}), 403
    
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': '请提供权限名称'}), 400
    
    # 检查权限是否已存在
    if Permission.query.filter_by(name=data['name']).first():
        return jsonify({'error': '权限已存在'}), 400
    
    permission = Permission(
        name=data['name'],
        description=data.get('description')
    )
    
    db.session.add(permission)
    db.session.commit()
    return jsonify(permission.to_dict()), 201

@system_bp.route('/role-permissions', methods=['GET'])
@jwt_required()
def get_role_permissions():
    # 检查用户是否为管理员
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': '无权限访问'}), 403
    
    # 支持按角色筛选
    role = request.args.get('role')
    
    query = RolePermission.query
    if role:
        query = query.filter_by(role=role)
    
    role_permissions = query.all()
    return jsonify([rp.to_dict() for rp in role_permissions]), 200

@system_bp.route('/role-permissions', methods=['POST'])
@jwt_required()
def create_role_permission():
    # 检查用户是否为管理员
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': '无权限操作'}), 403
    
    data = request.get_json()
    if not data or not data.get('role') or not data.get('permission_id'):
        return jsonify({'error': '请提供角色和权限ID'}), 400
    
    # 检查权限是否存在
    permission = Permission.query.get(data['permission_id'])
    if not permission:
        return jsonify({'error': '权限不存在'}), 404
    
    # 检查角色权限关联是否已存在
    if RolePermission.query.filter_by(role=data['role'], permission_id=data['permission_id']).first():
        return jsonify({'error': '角色权限关联已存在'}), 400
    
    role_permission = RolePermission(
        role=data['role'],
        permission_id=data['permission_id']
    )
    
    db.session.add(role_permission)
    db.session.commit()
    return jsonify(role_permission.to_dict()), 201

@system_bp.route('/role-permissions/<int:rp_id>', methods=['DELETE'])
@jwt_required()
def delete_role_permission(rp_id):
    # 检查用户是否为管理员
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': '无权限操作'}), 403
    
    role_permission = RolePermission.query.get(rp_id)
    if not role_permission:
        return jsonify({'error': '角色权限关联不存在'}), 404
    
    db.session.delete(role_permission)
    db.session.commit()
    return jsonify({'message': '角色权限关联删除成功'}), 200

@system_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_operation_logs():
    # 检查用户是否为管理员
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': '无权限访问'}), 403
    
    # 支持按用户ID、操作类型、状态等筛选
    user_id = request.args.get('user_id', type=int)
    operation_type = request.args.get('operation_type')
    status = request.args.get('status')
    
    query = OperationLog.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    if operation_type:
        query = query.filter_by(operation_type=operation_type)
    if status:
        query = query.filter_by(status=status)
    
    logs = query.order_by(OperationLog.operation_time.desc()).all()
    return jsonify([{
        'id': log.id,
        'user_id': log.user_id,
        'operation_type': log.operation_type,
        'operation_time': log.operation_time.isoformat() if log.operation_time else None,
        'ip_address': log.ip_address,
        'status': log.status,
        'details': log.details
    } for log in logs]), 200

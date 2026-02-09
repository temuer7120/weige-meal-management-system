from flask import request, jsonify
from flask_jwt_extended import jwt_required
from .. import suppliers_bp
from ...models.supplier import Supplier
from ... import db

@suppliers_bp.route('', methods=['GET'])
@jwt_required()
def get_suppliers():
    # 支持按评分排序
    sort_by_rating = request.args.get('sort_by_rating', type=bool)
    
    query = Supplier.query
    
    if sort_by_rating:
        query = query.order_by(Supplier.rating.desc())
    
    suppliers = query.all()
    return jsonify([supplier.to_dict() for supplier in suppliers]), 200

@suppliers_bp.route('/<int:supplier_id>', methods=['GET'])
@jwt_required()
def get_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({'error': '供应商不存在'}), 404
    
    # 获取该供应商提供的食材
    from ...models.ingredient import Ingredient
    ingredients = Ingredient.query.filter_by(supplier_id=supplier_id).all()
    
    return jsonify({
        'supplier': supplier.to_dict(),
        'ingredients': [ingredient.to_dict() for ingredient in ingredients]
    }), 200

@suppliers_bp.route('', methods=['POST'])
@jwt_required()
def create_supplier():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('contact_person') or not data.get('contact_phone'):
        return jsonify({'error': '请提供供应商名称、联系人姓名和联系电话'}), 400
    
    supplier = Supplier(
        name=data['name'],
        contact_person=data['contact_person'],
        contact_phone=data['contact_phone'],
        address=data.get('address'),
        products=data.get('products'),
        rating=data.get('rating', 0)
    )
    
    db.session.add(supplier)
    db.session.commit()
    return jsonify(supplier.to_dict()), 201

@suppliers_bp.route('/<int:supplier_id>', methods=['PUT'])
@jwt_required()
def update_supplier(supplier_id):
    data = request.get_json()
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({'error': '供应商不存在'}), 404
    
    # 更新供应商信息
    for key, value in data.items():
        if hasattr(supplier, key):
            setattr(supplier, key, value)
    
    db.session.commit()
    return jsonify(supplier.to_dict()), 200

@suppliers_bp.route('/<int:supplier_id>', methods=['DELETE'])
@jwt_required()
def delete_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({'error': '供应商不存在'}), 404
    
    # 检查是否有食材关联
    from ...models.ingredient import Ingredient
    ingredients = Ingredient.query.filter_by(supplier_id=supplier_id).first()
    if ingredients:
        return jsonify({'error': '该供应商有食材关联，无法删除'}), 400
    
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': '供应商删除成功'}), 200

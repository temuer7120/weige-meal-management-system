from flask import request, jsonify
from flask_jwt_extended import jwt_required
from .. import ingredients_bp
from ...models.ingredient import Ingredient
from ...models.supplier import Supplier
from ... import db

@ingredients_bp.route('', methods=['GET'])
@jwt_required()
def get_ingredients():
    # 支持按类别、供应商等筛选
    category = request.args.get('category')
    supplier_id = request.args.get('supplier_id', type=int)
    low_stock = request.args.get('low_stock', type=bool)
    
    query = Ingredient.query
    
    if category:
        query = query.filter_by(category=category)
    if supplier_id:
        query = query.filter_by(supplier_id=supplier_id)
    if low_stock:
        query = query.filter(Ingredient.current_stock <= Ingredient.minimum_stock)
    
    ingredients = query.all()
    return jsonify([ingredient.to_dict() for ingredient in ingredients]), 200

@ingredients_bp.route('/<int:ingredient_id>', methods=['GET'])
@jwt_required()
def get_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': '食材不存在'}), 404
    
    # 获取供应商信息
    supplier = Supplier.query.get(ingredient.supplier_id)
    
    return jsonify({
        'ingredient': ingredient.to_dict(),
        'supplier': supplier.to_dict() if supplier else None
    }), 200

@ingredients_bp.route('', methods=['POST'])
@jwt_required()
def create_ingredient():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('category') or not data.get('unit'):
        return jsonify({'error': '请提供食材名称、类别和单位'}), 400
    
    ingredient = Ingredient(
        name=data['name'],
        category=data['category'],
        unit=data['unit'],
        current_stock=data.get('current_stock', 0),
        minimum_stock=data.get('minimum_stock', 0),
        supplier_id=data.get('supplier_id'),
        price=data.get('price', 0),
        expiry_date=data.get('expiry_date'),
        nutrition_info=data.get('nutrition_info'),
        calories=data.get('calories'),
        restrictions=data.get('restrictions'),
        purchaser=data.get('purchaser'),
        origin=data.get('origin')
    )
    
    db.session.add(ingredient)
    db.session.commit()
    return jsonify(ingredient.to_dict()), 201

@ingredients_bp.route('/<int:ingredient_id>', methods=['PUT'])
@jwt_required()
def update_ingredient(ingredient_id):
    data = request.get_json()
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': '食材不存在'}), 404
    
    # 更新食材信息
    for key, value in data.items():
        if hasattr(ingredient, key):
            setattr(ingredient, key, value)
    
    db.session.commit()
    return jsonify(ingredient.to_dict()), 200

@ingredients_bp.route('/<int:ingredient_id>', methods=['DELETE'])
@jwt_required()
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': '食材不存在'}), 404
    
    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({'message': '食材删除成功'}), 200

@ingredients_bp.route('/<int:ingredient_id>/stock', methods=['PUT'])
@jwt_required()
def update_stock(ingredient_id):
    data = request.get_json()
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': '食材不存在'}), 404
    
    if 'quantity' not in data or 'type' not in data:
        return jsonify({'error': '请提供数量和操作类型（in或out）'}), 400
    
    quantity = data['quantity']
    if quantity <= 0:
        return jsonify({'error': '数量必须大于0'}), 400
    
    if data['type'] == 'in':
        # 入库
        ingredient.current_stock += quantity
    elif data['type'] == 'out':
        # 出库
        if ingredient.current_stock < quantity:
            return jsonify({'error': '库存不足'}), 400
        ingredient.current_stock -= quantity
    else:
        return jsonify({'error': '操作类型必须是in或out'}), 400
    
    db.session.commit()
    return jsonify({
        'message': '库存更新成功',
        'current_stock': ingredient.current_stock
    }), 200

@ingredients_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    # 获取所有食材类别
    categories = db.session.query(Ingredient.category).distinct().all()
    return jsonify([category[0] for category in categories]), 200

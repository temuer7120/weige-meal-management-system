from flask import request, jsonify
from flask_jwt_extended import jwt_required
from .. import dishes_bp
from ...models.dish import Dish
from ... import db

@dishes_bp.route('', methods=['GET'])
@jwt_required()
def get_dishes():
    # 支持按类别、状态等筛选
    category = request.args.get('category')
    status = request.args.get('status')
    
    query = Dish.query
    
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    
    dishes = query.all()
    return jsonify([dish.to_dict() for dish in dishes]), 200

@dishes_bp.route('/<int:dish_id>', methods=['GET'])
@jwt_required()
def get_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': '菜品不存在'}), 404
    
    return jsonify(dish.to_dict()), 200

@dishes_bp.route('', methods=['POST'])
@jwt_required()
def create_dish():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('category'):
        return jsonify({'error': '请提供菜品名称和类别'}), 400
    
    dish = Dish(
        name=data['name'],
        category=data['category'],
        description=data.get('description'),
        ingredients=data.get('ingredients'),
        restrictions=data.get('restrictions'),
        calories=data.get('calories'),
        price=data.get('price'),
        status=data.get('status', 'active')
    )
    
    db.session.add(dish)
    db.session.commit()
    return jsonify(dish.to_dict()), 201

@dishes_bp.route('/<int:dish_id>', methods=['PUT'])
@jwt_required()
def update_dish(dish_id):
    data = request.get_json()
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': '菜品不存在'}), 404
    
    # 更新菜品信息
    for key, value in data.items():
        if hasattr(dish, key):
            setattr(dish, key, value)
    
    db.session.commit()
    return jsonify(dish.to_dict()), 200

@dishes_bp.route('/<int:dish_id>', methods=['DELETE'])
@jwt_required()
def delete_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': '菜品不存在'}), 404
    
    db.session.delete(dish)
    db.session.commit()
    return jsonify({'message': '菜品删除成功'}), 200

@dishes_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    # 获取所有菜品类别
    categories = db.session.query(Dish.category).distinct().all()
    return jsonify([category[0] for category in categories]), 200

@dishes_bp.route('/check-restrictions', methods=['POST'])
@jwt_required()
def check_restrictions():
    data = request.get_json()
    if not data or not data.get('dish_ids') or not data.get('dietary_restrictions'):
        return jsonify({'error': '请提供菜品ID列表和饮食禁忌'}), 400
    
    dish_ids = data['dish_ids']
    restrictions = data['dietary_restrictions'].split(',')
    
    restricted_dishes = []
    
    for dish_id in dish_ids:
        dish = Dish.query.get(dish_id)
        if dish and dish.restrictions:
            dish_restrictions = dish.restrictions.split(',')
            for restriction in restrictions:
                if restriction.strip() in dish_restrictions:
                    restricted_dishes.append({
                        'dish_id': dish.id,
                        'dish_name': dish.name,
                        'restriction': restriction.strip()
                    })
                    break
    
    return jsonify({
        'restricted_dishes': restricted_dishes,
        'has_restrictions': len(restricted_dishes) > 0
    }), 200

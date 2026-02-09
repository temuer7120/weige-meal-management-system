from flask import request, jsonify
from flask_jwt_extended import jwt_required
from .. import menus_bp
from ...models.menu import Menu, MenuDish, CustomerMenu
from ...models.dish import Dish
from ...models.customer import Customer
from ... import db

@menus_bp.route('', methods=['GET'])
@jwt_required()
def get_menus():
    # 支持按类型、状态等筛选
    menu_type = request.args.get('type')
    status = request.args.get('status')
    
    query = Menu.query
    
    if menu_type:
        query = query.filter_by(type=menu_type)
    if status:
        query = query.filter_by(status=status)
    
    menus = query.all()
    return jsonify([menu.to_dict() for menu in menus]), 200

@menus_bp.route('/<int:menu_id>', methods=['GET'])
@jwt_required()
def get_menu(menu_id):
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({'error': '菜单不存在'}), 404
    
    # 获取菜单包含的菜品
    menu_dishes = MenuDish.query.filter_by(menu_id=menu_id).all()
    dish_ids = [md.dish_id for md in menu_dishes]
    dishes = Dish.query.filter(Dish.id.in_(dish_ids)).all()
    
    # 构建菜品与数量的映射
    dish_quantity_map = {md.dish_id: md.quantity for md in menu_dishes}
    dishes_with_quantity = []
    for dish in dishes:
        dish_dict = dish.to_dict()
        dish_dict['quantity'] = dish_quantity_map.get(dish.id, 1)
        dishes_with_quantity.append(dish_dict)
    
    return jsonify({
        'menu': menu.to_dict(),
        'dishes': dishes_with_quantity
    }), 200

@menus_bp.route('', methods=['POST'])
@jwt_required()
def create_menu():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('type'):
        return jsonify({'error': '请提供菜单名称和类型'}), 400
    
    menu = Menu(
        name=data['name'],
        description=data.get('description'),
        type=data['type'],
        price=data.get('price'),
        status=data.get('status', 'active')
    )
    
    db.session.add(menu)
    db.session.flush()  # 获取菜单ID但不提交事务
    
    # 添加菜单菜品关联
    if 'dishes' in data:
        for dish_item in data['dishes']:
            if 'dish_id' in dish_item and 'quantity' in dish_item:
                menu_dish = MenuDish(
                    menu_id=menu.id,
                    dish_id=dish_item['dish_id'],
                    quantity=dish_item['quantity']
                )
                db.session.add(menu_dish)
    
    db.session.commit()
    return jsonify(menu.to_dict()), 201

@menus_bp.route('/<int:menu_id>', methods=['PUT'])
@jwt_required()
def update_menu(menu_id):
    data = request.get_json()
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({'error': '菜单不存在'}), 404
    
    # 更新菜单信息
    if 'name' in data:
        menu.name = data['name']
    if 'description' in data:
        menu.description = data['description']
    if 'type' in data:
        menu.type = data['type']
    if 'price' in data:
        menu.price = data['price']
    if 'status' in data:
        menu.status = data['status']
    
    # 更新菜单菜品关联
    if 'dishes' in data:
        # 删除现有关联
        MenuDish.query.filter_by(menu_id=menu_id).delete()
        # 添加新关联
        for dish_item in data['dishes']:
            if 'dish_id' in dish_item and 'quantity' in dish_item:
                menu_dish = MenuDish(
                    menu_id=menu_id,
                    dish_id=dish_item['dish_id'],
                    quantity=dish_item['quantity']
                )
                db.session.add(menu_dish)
    
    db.session.commit()
    return jsonify(menu.to_dict()), 200

@menus_bp.route('/<int:menu_id>', methods=['DELETE'])
@jwt_required()
def delete_menu(menu_id):
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({'error': '菜单不存在'}), 404
    
    # 删除菜单菜品关联
    MenuDish.query.filter_by(menu_id=menu_id).delete()
    # 删除菜单客户关联
    CustomerMenu.query.filter_by(menu_id=menu_id).delete()
    # 删除菜单
    db.session.delete(menu)
    
    db.session.commit()
    return jsonify({'message': '菜单删除成功'}), 200

@menus_bp.route('/<int:menu_id>/add-dish', methods=['POST'])
@jwt_required()
def add_dish_to_menu(menu_id):
    data = request.get_json()
    if not data or not data.get('dish_id') or not data.get('quantity'):
        return jsonify({'error': '请提供菜品ID和数量'}), 400
    
    # 检查菜单是否存在
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({'error': '菜单不存在'}), 404
    
    # 检查菜品是否存在
    dish = Dish.query.get(data['dish_id'])
    if not dish:
        return jsonify({'error': '菜品不存在'}), 404
    
    # 检查关联是否已存在
    existing = MenuDish.query.filter_by(menu_id=menu_id, dish_id=data['dish_id']).first()
    if existing:
        existing.quantity = data['quantity']
    else:
        menu_dish = MenuDish(
            menu_id=menu_id,
            dish_id=data['dish_id'],
            quantity=data['quantity']
        )
        db.session.add(menu_dish)
    
    db.session.commit()
    return jsonify({'message': '菜品添加成功'}), 200

@menus_bp.route('/<int:menu_id>/remove-dish/<int:dish_id>', methods=['DELETE'])
@jwt_required()
def remove_dish_from_menu(menu_id, dish_id):
    menu_dish = MenuDish.query.filter_by(menu_id=menu_id, dish_id=dish_id).first()
    if not menu_dish:
        return jsonify({'error': '菜品不在菜单中'}), 404
    
    db.session.delete(menu_dish)
    db.session.commit()
    return jsonify({'message': '菜品移除成功'}), 200

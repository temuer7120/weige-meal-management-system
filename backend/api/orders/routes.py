from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import orders_bp
from ...models.order import CustomerOrder, OrderItem
from ...models.customer import Customer
from ...models.employee import Employee
from ...models.dish import Dish
from ...models.menu import Menu
from ... import db

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    # 支持按订单类型、状态、客户ID等筛选
    order_type = request.args.get('order_type')
    status = request.args.get('status')
    customer_id = request.args.get('customer_id', type=int)
    
    query = CustomerOrder.query
    
    if order_type:
        query = query.filter_by(order_type=order_type)
    if status:
        query = query.filter_by(status=status)
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    
    orders = query.all()
    return jsonify([order.to_dict() for order in orders]), 200

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    order = CustomerOrder.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    # 获取订单包含的项目
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    
    # 获取项目详细信息
    items_with_details = []
    for item in order_items:
        item_dict = item.to_dict()
        # 根据项目类型获取详细信息
        if item.item_type == 'dish':
            dish = Dish.query.get(item.item_id)
            if dish:
                item_dict['details'] = dish.to_dict()
        elif item.item_type == 'menu':
            menu = Menu.query.get(item.item_id)
            if menu:
                item_dict['details'] = menu.to_dict()
        elif item.item_type == 'service':
            # 服务项目的详细信息可以从其他表获取
            pass
        items_with_details.append(item_dict)
    
    # 获取客户信息
    customer = Customer.query.get(order.customer_id)
    # 获取服务员工信息
    employee = Employee.query.get(order.service_employee_id)
    
    return jsonify({
        'order': order.to_dict(),
        'items': items_with_details,
        'customer': customer.to_dict() if customer else None,
        'employee': employee.to_dict() if employee else None
    }), 200

@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    if not data or not data.get('customer_id') or not data.get('order_type') or not data.get('items'):
        return jsonify({'error': '请提供客户ID、订单类型和订单项目'}), 400
    
    # 计算总金额
    total_amount = 0
    for item in data['items']:
        if 'subtotal' in item:
            total_amount += item['subtotal']
    
    order = CustomerOrder(
        customer_id=data['customer_id'],
        order_type=data['order_type'],
        total_amount=total_amount,
        delivery_date=data.get('delivery_date'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        duration=data.get('duration'),
        payment_method=data.get('payment_method'),
        booker_name=data.get('booker_name'),
        booker_role=data.get('booker_role'),
        service_employee_id=data.get('service_employee_id'),
        delivery_address=data.get('delivery_address'),
        notes=data.get('notes')
    )
    
    db.session.add(order)
    db.session.flush()  # 获取订单ID但不提交事务
    
    # 添加订单项
    for item in data['items']:
        if not item.get('item_type') or not item.get('item_id') or not item.get('quantity') or not item.get('unit_price'):
            return jsonify({'error': '订单项信息不完整'}), 400
        
        order_item = OrderItem(
            order_id=order.id,
            item_type=item['item_type'],
            item_id=item['item_id'],
            quantity=item['quantity'],
            unit_price=item['unit_price'],
            subtotal=item.get('subtotal', item['quantity'] * item['unit_price'])
        )
        db.session.add(order_item)
    
    db.session.commit()
    return jsonify(order.to_dict()), 201

@orders_bp.route('/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    data = request.get_json()
    order = CustomerOrder.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    # 更新订单信息
    updateable_fields = ['status', 'payment_status', 'payment_method', 'service_employee_id', 'notes', 'rating', 'feedback']
    for field in updateable_fields:
        if field in data:
            setattr(order, field, data[field])
    
    db.session.commit()
    return jsonify(order.to_dict()), 200

@orders_bp.route('/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    order = CustomerOrder.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    # 只有未完成的订单可以删除
    if order.status == 'completed':
        return jsonify({'error': '已完成的订单不能删除'}), 400
    
    # 删除订单项
    OrderItem.query.filter_by(order_id=order_id).delete()
    # 删除订单
    db.session.delete(order)
    
    db.session.commit()
    return jsonify({'message': '订单删除成功'}), 200

@orders_bp.route('/<int:order_id>/items', methods=['POST'])
@jwt_required()
def add_order_item(order_id):
    data = request.get_json()
    if not data or not data.get('item_type') or not data.get('item_id') or not data.get('quantity') or not data.get('unit_price'):
        return jsonify({'error': '请提供项目类型、项目ID、数量和单价'}), 400
    
    # 检查订单是否存在
    order = CustomerOrder.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    # 计算小计
    subtotal = data['quantity'] * data['unit_price']
    
    # 创建订单项
    order_item = OrderItem(
        order_id=order_id,
        item_type=data['item_type'],
        item_id=data['item_id'],
        quantity=data['quantity'],
        unit_price=data['unit_price'],
        subtotal=subtotal
    )
    db.session.add(order_item)
    
    # 更新订单总金额
    order.total_amount += subtotal
    
    db.session.commit()
    return jsonify({'message': '项目添加成功'}), 200

@orders_bp.route('/<int:order_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_order_item(order_id, item_id):
    order_item = OrderItem.query.filter_by(order_id=order_id, id=item_id).first()
    if not order_item:
        return jsonify({'error': '订单项不存在'}), 404
    
    # 更新订单总金额
    order = CustomerOrder.query.get(order_id)
    if order:
        order.total_amount -= order_item.subtotal
    
    # 删除订单项
    db.session.delete(order_item)
    
    db.session.commit()
    return jsonify({'message': '项目移除成功'}), 200

@orders_bp.route('/<int:order_id>/pay', methods=['POST'])
@jwt_required()
def pay_order(order_id):
    data = request.get_json()
    if not data or not data.get('payment_method'):
        return jsonify({'error': '请提供支付方式'}), 400
    
    order = CustomerOrder.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    if order.payment_status == 'paid':
        return jsonify({'error': '订单已经支付'}), 400
    
    # 更新支付状态
    order.payment_status = 'paid'
    order.payment_method = data['payment_method']
    
    # 这里可以集成第三方支付API
    # 例如：调用微信支付、支付宝等API
    
    db.session.commit()
    return jsonify({'message': '支付成功'}), 200

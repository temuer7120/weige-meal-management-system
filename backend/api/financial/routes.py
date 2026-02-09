from flask import request, jsonify
from flask_jwt_extended import jwt_required
from .. import financial_bp
from ...models.financial import Transaction, Attendance, Workload, Salary, PurchaseOrder, PurchaseOrderItem, PaymentTransaction
from ... import db

@financial_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    # 支持按类型、状态等筛选
    transaction_type = request.args.get('type')
    status = request.args.get('status')
    
    query = Transaction.query
    
    if transaction_type:
        query = query.filter_by(type=transaction_type)
    if status:
        query = query.filter_by(status=status)
    
    transactions = query.all()
    return jsonify([{
        'id': t.id,
        'amount': t.amount,
        'type': t.type,
        'status': t.status,
        'payment_method': t.payment_method,
        'transaction_date': t.transaction_date.isoformat() if t.transaction_date else None,
        'description': t.description
    } for t in transactions]), 200

@financial_bp.route('/workloads', methods=['GET'])
@jwt_required()
def get_workloads():
    # 支持按员工ID、日期范围等筛选
    employee_id = request.args.get('employee_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Workload.query
    
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if start_date:
        query = query.filter(Workload.date >= start_date)
    if end_date:
        query = query.filter(Workload.date <= end_date)
    
    workloads = query.all()
    return jsonify([{
        'id': w.id,
        'employee_id': w.employee_id,
        'date': w.date.isoformat() if w.date else None,
        'hours': w.hours,
        'amount': w.amount,
        'description': w.description
    } for w in workloads]), 200

@financial_bp.route('/workloads', methods=['POST'])
@jwt_required()
def create_workload():
    data = request.get_json()
    if not data or not data.get('employee_id') or not data.get('date') or not data.get('hours'):
        return jsonify({'error': '请提供员工ID、日期和工作时长'}), 400
    
    workload = Workload(
        employee_id=data['employee_id'],
        date=data['date'],
        hours=data['hours'],
        amount=data.get('amount'),
        description=data.get('description')
    )
    
    db.session.add(workload)
    db.session.commit()
    return jsonify({
        'id': workload.id,
        'employee_id': workload.employee_id,
        'date': workload.date.isoformat() if workload.date else None,
        'hours': workload.hours,
        'amount': workload.amount,
        'description': workload.description
    }), 201

@financial_bp.route('/salaries', methods=['GET'])
@jwt_required()
def get_salaries():
    # 支持按员工ID、年份、月份等筛选
    employee_id = request.args.get('employee_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    query = Salary.query
    
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if year:
        query = query.filter_by(year=year)
    if month:
        query = query.filter_by(month=month)
    
    salaries = query.all()
    return jsonify([{
        'id': s.id,
        'employee_id': s.employee_id,
        'year': s.year,
        'month': s.month,
        'base_salary': s.base_salary,
        'allowance': s.allowance,
        'bonus': s.bonus,
        'deduction': s.deduction,
        'net_salary': s.net_salary,
        'status': s.status,
        'payment_date': s.payment_date.isoformat() if s.payment_date else None
    } for s in salaries]), 200

@financial_bp.route('/salaries', methods=['POST'])
@jwt_required()
def create_salary():
    data = request.get_json()
    if not data or not data.get('employee_id') or not data.get('year') or not data.get('month'):
        return jsonify({'error': '请提供员工ID、年份和月份'}), 400
    
    # 计算净工资
    base_salary = data.get('base_salary', 0)
    allowance = data.get('allowance', 0)
    bonus = data.get('bonus', 0)
    deduction = data.get('deduction', 0)
    net_salary = base_salary + allowance + bonus - deduction
    
    salary = Salary(
        employee_id=data['employee_id'],
        year=data['year'],
        month=data['month'],
        base_salary=base_salary,
        allowance=allowance,
        bonus=bonus,
        deduction=deduction,
        net_salary=net_salary,
        status=data.get('status', 'pending'),
        payment_date=data.get('payment_date')
    )
    
    db.session.add(salary)
    db.session.commit()
    return jsonify({
        'id': salary.id,
        'employee_id': salary.employee_id,
        'year': salary.year,
        'month': salary.month,
        'base_salary': salary.base_salary,
        'allowance': salary.allowance,
        'bonus': salary.bonus,
        'deduction': salary.deduction,
        'net_salary': salary.net_salary,
        'status': salary.status,
        'payment_date': salary.payment_date.isoformat() if salary.payment_date else None
    }), 201

@financial_bp.route('/purchase-orders', methods=['GET'])
@jwt_required()
def get_purchase_orders():
    # 支持按状态筛选
    status = request.args.get('status')
    
    query = PurchaseOrder.query
    
    if status:
        query = query.filter_by(status=status)
    
    purchase_orders = query.all()
    return jsonify([{
        'id': po.id,
        'supplier_id': po.supplier_id,
        'order_date': po.order_date.isoformat() if po.order_date else None,
        'total_amount': po.total_amount,
        'status': po.status,
        'notes': po.notes
    } for po in purchase_orders]), 200

@financial_bp.route('/purchase-orders', methods=['POST'])
@jwt_required()
def create_purchase_order():
    data = request.get_json()
    if not data or not data.get('supplier_id') or not data.get('items'):
        return jsonify({'error': '请提供供应商ID和采购项目'}), 400
    
    # 计算总金额
    total_amount = 0
    for item in data['items']:
        if 'subtotal' in item:
            total_amount += item['subtotal']
    
    purchase_order = PurchaseOrder(
        supplier_id=data['supplier_id'],
        total_amount=total_amount,
        status=data.get('status', 'pending'),
        notes=data.get('notes')
    )
    
    db.session.add(purchase_order)
    db.session.flush()  # 获取采购订单ID但不提交事务
    
    # 添加采购项目
    for item in data['items']:
        if not item.get('ingredient_id') or not item.get('quantity') or not item.get('unit_price'):
            return jsonify({'error': '采购项目信息不完整'}), 400
        
        purchase_item = PurchaseOrderItem(
            purchase_order_id=purchase_order.id,
            ingredient_id=item['ingredient_id'],
            quantity=item['quantity'],
            unit_price=item['unit_price'],
            subtotal=item.get('subtotal', item['quantity'] * item['unit_price'])
        )
        db.session.add(purchase_item)
    
    db.session.commit()
    return jsonify({
        'id': purchase_order.id,
        'supplier_id': purchase_order.supplier_id,
        'order_date': purchase_order.order_date.isoformat() if purchase_order.order_date else None,
        'total_amount': purchase_order.total_amount,
        'status': purchase_order.status,
        'notes': purchase_order.notes
    }), 201

from flask import request, jsonify
from flask_jwt_extended import jwt_required
from .. import employees_bp
from ...models.employee import Employee
from ...models.order import CustomerOrder
from ...models.financial import Workload, Salary
from ... import db

@employees_bp.route('', methods=['GET'])
@jwt_required()
def get_employees():
    # 支持按职位、状态等筛选
    position = request.args.get('position')
    status = request.args.get('status')
    
    query = Employee.query
    
    if position:
        query = query.filter_by(position=position)
    if status:
        query = query.filter_by(status=status)
    
    employees = query.all()
    return jsonify([employee.to_dict() for employee in employees]), 200

@employees_bp.route('/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': '员工不存在'}), 404
    
    return jsonify(employee.to_dict()), 200

@employees_bp.route('', methods=['POST'])
@jwt_required()
def create_employee():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('position') or not data.get('contact'):
        return jsonify({'error': '请提供员工姓名、职位和联系方式'}), 400
    
    employee = Employee(
        user_id=data.get('user_id'),
        name=data['name'],
        position=data['position'],
        contact=data['contact'],
        base_salary=data.get('base_salary'),
        joining_date=data.get('joining_date'),
        education=data.get('education'),
        work_experience=data.get('work_experience'),
        work_performance=data.get('work_performance'),
        status=data.get('status', 'active')
    )
    
    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201

@employees_bp.route('/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    data = request.get_json()
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': '员工不存在'}), 404
    
    # 更新员工信息
    for key, value in data.items():
        if hasattr(employee, key):
            setattr(employee, key, value)
    
    db.session.commit()
    return jsonify(employee.to_dict()), 200

@employees_bp.route('/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': '员工不存在'}), 404
    
    # 检查是否有关联的订单
    orders = CustomerOrder.query.filter_by(service_employee_id=employee_id).first()
    if orders:
        return jsonify({'error': '该员工有服务订单关联，无法删除'}), 400
    
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': '员工删除成功'}), 200

@employees_bp.route('/<int:employee_id>/workload', methods=['GET'])
@jwt_required()
def get_employee_workload(employee_id):
    # 检查员工是否存在
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': '员工不存在'}), 404
    
    # 获取查询参数
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # 查询员工的工作量记录
    query = Workload.query.filter_by(employee_id=employee_id)
    if start_date:
        query = query.filter(Workload.date >= start_date)
    if end_date:
        query = query.filter(Workload.date <= end_date)
    
    workloads = query.all()
    
    # 计算总工作量
    total_hours = sum(w.hours for w in workloads)
    total_amount = sum(w.amount for w in workloads)
    
    return jsonify({
        'employee': employee.to_dict(),
        'workloads': [{
            'id': w.id,
            'date': w.date.isoformat() if w.date else None,
            'hours': w.hours,
            'amount': w.amount,
            'description': w.description
        } for w in workloads],
        'summary': {
            'total_hours': total_hours,
            'total_amount': total_amount
        }
    }), 200

@employees_bp.route('/<int:employee_id>/salary', methods=['GET'])
@jwt_required()
def get_employee_salary(employee_id):
    # 检查员工是否存在
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': '员工不存在'}), 404
    
    # 获取查询参数
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    # 查询员工的薪资记录
    query = Salary.query.filter_by(employee_id=employee_id)
    if year:
        query = query.filter_by(year=year)
    if month:
        query = query.filter_by(month=month)
    
    salaries = query.all()
    
    return jsonify({
        'employee': employee.to_dict(),
        'salaries': [{
            'id': s.id,
            'year': s.year,
            'month': s.month,
            'base_salary': s.base_salary,
            'allowance': s.allowance,
            'bonus': s.bonus,
            'deduction': s.deduction,
            'net_salary': s.net_salary,
            'status': s.status,
            'payment_date': s.payment_date.isoformat() if s.payment_date else None
        } for s in salaries]
    }), 200

@employees_bp.route('/<int:employee_id>/orders', methods=['GET'])
@jwt_required()
def get_employee_orders(employee_id):
    # 检查员工是否存在
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': '员工不存在'}), 404
    
    # 查询员工服务的订单
    orders = CustomerOrder.query.filter_by(service_employee_id=employee_id).all()
    
    return jsonify({
        'employee': employee.to_dict(),
        'orders': [order.to_dict() for order in orders]
    }), 200

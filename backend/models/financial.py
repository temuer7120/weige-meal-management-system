from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(20), nullable=False)  # income/expense
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Decimal(10, 2), nullable=False)
    description = db.Column(db.Text)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(20))  # wechat/alipay/bank/cash
    status = db.Column(db.String(20), default='completed')  # pending/completed/cancelled
    related_id = db.Column(db.Integer)  # 关联ID（客户ID/员工ID/供应商ID）
    related_type = db.Column(db.String(20))  # 关联类型（customer/employee/supplier）
    
    def __repr__(self):
        return f'<Transaction {self.id} {self.type}>'

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    date = db.Column(db.Date, nullable=False)
    check_in_time = db.Column(db.Time)
    check_out_time = db.Column(db.Time)
    work_hours = db.Column(db.Decimal(5, 2))
    status = db.Column(db.String(20), default='present')  # present/absent/leave
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Attendance employee_id={self.employee_id} date={self.date}>'

class Workload(db.Model):
    __tablename__ = 'workload'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    date = db.Column(db.Date, nullable=False)
    work_type = db.Column(db.String(20), nullable=False)  # normal/overtime/accompany/care
    hours = db.Column(db.Decimal(5, 2), nullable=False)
    description = db.Column(db.Text)
    rate_multiplier = db.Column(db.Decimal(3, 2), default=1.0)  # 薪资倍率
    
    def __repr__(self):
        return f'<Workload employee_id={self.employee_id} date={self.date}>'

class Salary(db.Model):
    __tablename__ = 'salary'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    pay_period = db.Column(db.String(20), nullable=False)  # 薪资周期
    base_salary = db.Column(db.Decimal(10, 2), nullable=False)
    overtime_pay = db.Column(db.Decimal(10, 2), default=0)  # 加班费
    allowance = db.Column(db.Decimal(10, 2), default=0)  # 津贴
    deductions = db.Column(db.Decimal(10, 2), default=0)  # 扣除项
    net_salary = db.Column(db.Decimal(10, 2), nullable=False)  # 实发薪资
    payment_date = db.Column(db.Date)  # 发放日期
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    status = db.Column(db.String(20), default='pending')  # pending/paid
    
    def __repr__(self):
        return f'<Salary employee_id={self.employee_id} pay_period={self.pay_period}>'

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    order_date = db.Column(db.Date, nullable=False)
    expected_delivery = db.Column(db.Date)  # 预计送达日期
    total_amount = db.Column(db.Decimal(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending/delivered/cancelled
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    
    def __repr__(self):
        return f'<PurchaseOrder {self.id} supplier_id={self.supplier_id}>'

class PurchaseOrderItem(db.Model):
    __tablename__ = 'purchase_order_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    quantity = db.Column(db.Decimal(10, 2), nullable=False)
    unit_price = db.Column(db.Decimal(10, 2), nullable=False)
    subtotal = db.Column(db.Decimal(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<PurchaseOrderItem order_id={self.order_id} ingredient_id={self.ingredient_id}>'

class PaymentTransaction(db.Model):
    __tablename__ = 'payment_transactions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    payment_method = db.Column(db.String(20), nullable=False)  # wechat/alipay/bank
    payment_amount = db.Column(db.Decimal(10, 2), nullable=False)
    transaction_status = db.Column(db.String(20), default='pending')  # pending/success/failed
    transaction_time = db.Column(db.DateTime)
    transaction_id_external = db.Column(db.String(100))  # 外部交易ID
    error_message = db.Column(db.Text)  # 错误信息
    
    def __repr__(self):
        return f'<PaymentTransaction {self.id} payment_method={self.payment_method}>'

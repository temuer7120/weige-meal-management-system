from app import db
from datetime import datetime

class CustomerOrder(db.Model):
    __tablename__ = 'customer_orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_date = db.Column(db.Date)
    start_time = db.Column(db.Time)  # 开始时间
    end_time = db.Column(db.Time)  # 结束时间
    duration = db.Column(db.Decimal(5, 2))  # 时长
    order_type = db.Column(db.String(20), nullable=False)  # 订单类型（meal/service）
    total_amount = db.Column(db.Decimal(10, 2), nullable=False)
    payment_status = db.Column(db.String(20), default='pending')  # pending/paid/cancelled
    payment_method = db.Column(db.String(20))  # wechat/alipay/bank/cash
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    status = db.Column(db.String(20), default='pending')  # pending/confirmed/completed/cancelled
    booker_name = db.Column(db.String(50))  # 预定人姓名
    booker_role = db.Column(db.String(20))  # 预定人角色（customer/employee/nutritionist）
    service_employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))  # 服务员工ID
    delivery_address = db.Column(db.Text)  # 配送地址
    notes = db.Column(db.Text)  # 备注
    rating = db.Column(db.Integer)  # 评分（1-5）
    feedback = db.Column(db.Text)  # 评价反馈
    
    def __repr__(self):
        return f'<CustomerOrder {self.id} {self.order_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'order_type': self.order_type,
            'total_amount': self.total_amount,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'booker_name': self.booker_name,
            'booker_role': self.booker_role,
            'service_employee_id': self.service_employee_id,
            'delivery_address': self.delivery_address,
            'notes': self.notes,
            'rating': self.rating,
            'feedback': self.feedback
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('customer_orders.id'))
    item_type = db.Column(db.String(20), nullable=False)  # 项目类型（dish/service）
    item_id = db.Column(db.Integer)  # 项目ID（菜品ID/服务ID）
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Decimal(10, 2), nullable=False)
    subtotal = db.Column(db.Decimal(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<OrderItem order_id={self.order_id} item_type={self.item_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'item_type': self.item_type,
            'item_id': self.item_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'subtotal': self.subtotal
        }

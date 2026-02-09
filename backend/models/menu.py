from app import db
from datetime import datetime

class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(20), nullable=False)  # breakfast/lunch/dinner
    price = db.Column(db.Decimal(10, 2))
    status = db.Column(db.String(20), default='active')  # active/inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Menu {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'price': self.price,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class MenuDish(db.Model):
    __tablename__ = 'menu_dishes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f'<MenuDish Menu={self.menu_id}, Dish={self.dish_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'menu_id': self.menu_id,
            'dish_id': self.dish_id,
            'quantity': self.quantity
        }

class CustomerMenu(db.Model):
    __tablename__ = 'customer_menus'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='ordered')  # ordered, delivered, cancelled
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5
    
    def __repr__(self):
        return f'<CustomerMenu Customer={self.customer_id}, Menu={self.menu_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'menu_id': self.menu_id,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'status': self.status,
            'feedback': self.feedback,
            'rating': self.rating
        }

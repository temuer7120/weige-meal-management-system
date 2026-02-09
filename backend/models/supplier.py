from app import db
from datetime import datetime

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(50), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    products = db.Column(db.Text)  # 供应产品
    rating = db.Column(db.Decimal(3, 1), default=0)  # 评分
    
    def __repr__(self):
        return f'<Supplier {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'products': self.products,
            'rating': self.rating
        }

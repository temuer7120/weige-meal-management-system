from app import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(100))
    delivery_date = db.Column(db.Date)
    check_in_date = db.Column(db.Date)
    check_out_date = db.Column(db.Date)
    dietary_restrictions = db.Column(db.Text)
    preferences = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active/inactive
    
    def __repr__(self):
        return f'<Customer {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'contact': self.contact,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None,
            'dietary_restrictions': self.dietary_restrictions,
            'preferences': self.preferences,
            'status': self.status
        }

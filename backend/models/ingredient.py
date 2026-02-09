from app import db
from datetime import datetime

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    current_stock = db.Column(db.Decimal(10, 2), default=0)
    minimum_stock = db.Column(db.Decimal(10, 2), default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    price = db.Column(db.Decimal(10, 2))
    expiry_date = db.Column(db.Date)
    nutrition_info = db.Column(db.Text)  # 营养成分
    calories = db.Column(db.Decimal(8, 2))  # 热量
    restrictions = db.Column(db.Text)  # 禁忌信息
    purchaser = db.Column(db.String(50))  # 购买人
    origin = db.Column(db.Text)  # 食材溯源
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'unit': self.unit,
            'current_stock': self.current_stock,
            'minimum_stock': self.minimum_stock,
            'supplier_id': self.supplier_id,
            'price': self.price,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'nutrition_info': self.nutrition_info,
            'calories': self.calories,
            'restrictions': self.restrictions,
            'purchaser': self.purchaser,
            'origin': self.origin
        }

from app import db
from datetime import datetime

class Dish(db.Model):
    __tablename__ = 'dishes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 汤品/点心/肉菜/蔬菜等
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)  # 食材组成
    restrictions = db.Column(db.Text)  # 禁忌食材
    calories = db.Column(db.Integer)  # 卡路里
    price = db.Column(db.Decimal(10, 2))  # 价格
    status = db.Column(db.String(20), default='active')  # active/inactive
    
    def __repr__(self):
        return f'<Dish {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'ingredients': self.ingredients,
            'restrictions': self.restrictions,
            'calories': self.calories,
            'price': self.price,
            'status': self.status
        }

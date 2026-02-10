from app import db
from datetime import datetime
from sqlalchemy import DECIMAL

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(100))
    base_salary = db.Column(DECIMAL(10, 2), nullable=False)
    joining_date = db.Column(db.Date, nullable=False)
    education = db.Column(db.Text)  # 学历
    work_experience = db.Column(db.Text)  # 工作经历
    work_performance = db.Column(db.Text)  # 工作业绩
    status = db.Column(db.String(20), default='active')  # active/inactive
    
    def __repr__(self):
        return f'<Employee {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'position': self.position,
            'contact': self.contact,
            'base_salary': self.base_salary,
            'joining_date': self.joining_date.isoformat() if self.joining_date else None,
            'education': self.education,
            'work_experience': self.work_experience,
            'work_performance': self.work_performance,
            'status': self.status
        }

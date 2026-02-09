from app import db
from datetime import datetime

class ConfinementMealPlan(db.Model):
    __tablename__ = 'confinement_meal_plans'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    total_days = db.Column(db.Integer)
    total_weeks = db.Column(db.Integer)
    meal_plan_type = db.Column(db.String(20))  # 计划类型
    total_calories_per_day = db.Column(db.Decimal(8, 2))  # 每日总卡路里
    total_price = db.Column(db.Decimal(12, 2), default=0)
    discount_amount = db.Column(db.Decimal(10, 2))  # 折扣金额
    final_price = db.Column(db.Decimal(12, 2), default=0)  # 最终价格
    status = db.Column(db.String(20), default='draft')  # draft/active/completed
    notes = db.Column(db.Text)  # 备注
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 创建人ID
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 审批人ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ConfinementMealPlan {self.plan_number}>'

class ConfinementWeekPlan(db.Model):
    __tablename__ = 'confinement_week_plans'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('confinement_meal_plans.id'))
    week_number = db.Column(db.Integer, nullable=False)
    focus_area = db.Column(db.String(100))  # 重点区域
    nutrition_goals = db.Column(db.Text)  # 营养目标
    avoid_foods = db.Column(db.Text)  # 禁忌食物
    recommended_foods = db.Column(db.Text)  # 推荐食物
    notes = db.Column(db.Text)  # 备注
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ConfinementWeekPlan meal_plan_id={self.meal_plan_id} week_number={self.week_number}>'

class ConfinementDayPlan(db.Model):
    __tablename__ = 'confinement_day_plans'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    week_plan_id = db.Column(db.Integer, db.ForeignKey('confinement_week_plans.id'))
    day_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date)
    total_calories = db.Column(db.Decimal(8, 2))  # 总卡路里
    nutrition_summary = db.Column(db.Text)  # 营养总结
    special_notes = db.Column(db.Text)  # 特别备注
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ConfinementDayPlan week_plan_id={self.week_plan_id} day_number={self.day_number}>'

class ConfinementMealItem(db.Model):
    __tablename__ = 'confinement_meal_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day_plan_id = db.Column(db.Integer, db.ForeignKey('confinement_day_plans.id'))
    meal_type = db.Column(db.String(50), nullable=False)  # 餐食类型
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'))
    serving_time = db.Column(db.Time)  # 供应时间
    quantity = db.Column(db.Integer, default=1)
    calories = db.Column(db.Decimal(8, 2))  # 卡路里
    nutrition_details = db.Column(db.Text)  # 营养详情
    special_instructions = db.Column(db.Text)  # 特别说明
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ConfinementMealItem day_plan_id={self.day_plan_id} meal_type={self.meal_type}>'

class HealthRecord(db.Model):
    __tablename__ = 'health_records'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    record_type = db.Column(db.String(50), nullable=False)  # 记录类型
    record_date = db.Column(db.Date, nullable=False)
    health_data = db.Column(db.Text)  # 健康数据
    notes = db.Column(db.Text)  # 备注
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 创建人ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<HealthRecord customer_id={self.customer_id} record_type={self.record_type}>'

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    service_type = db.Column(db.String(50), nullable=False)  # 服务类型
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending/confirmed/completed/cancelled
    notes = db.Column(db.Text)  # 备注
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 创建人ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Appointment customer_id={self.customer_id} service_type={self.service_type}>'

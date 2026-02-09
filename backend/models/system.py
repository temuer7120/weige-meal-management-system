from app import db
from datetime import datetime

class OperationLog(db.Model):
    __tablename__ = 'operation_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    operation_type = db.Column(db.String(50), nullable=False)
    operation_time = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.Text)
    details = db.Column(db.Text)
    status = db.Column(db.String(20), default='success')  # success/failed
    
    def __repr__(self):
        return f'<OperationLog user_id={self.user_id} operation_type={self.operation_type}>'

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Permission {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(20), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    
    def __repr__(self):
        return f'<RolePermission role={self.role} permission_id={self.permission_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'permission_id': self.permission_id
        }

class Backup(db.Model):
    __tablename__ = 'backups'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    backup_time = db.Column(db.DateTime, default=datetime.utcnow)
    backup_path = db.Column(db.Text, nullable=False)
    backup_size = db.Column(db.BigInteger)
    status = db.Column(db.String(20), default='success')  # success/failed
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Backup id={self.id} backup_time={self.backup_time}>'

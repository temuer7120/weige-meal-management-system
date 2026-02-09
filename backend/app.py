from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用实例
app = Flask(__name__)

# 配置应用
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'mysql+pymysql://MySQL:MySQL@localhost/meal_system')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')

# 初始化扩展
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# 注册API蓝图
from api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# 创建数据库表
with app.app_context():
    db.create_all()
    
    # 初始化默认管理员用户
    from models.user import User
    from werkzeug.security import generate_password_hash
    
    # 检查是否存在admin用户
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        # 创建默认管理员用户
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print('默认管理员用户创建成功: admin/admin123')

if __name__ == '__main__':
    app.run(debug=True)

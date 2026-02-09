#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建数据库表结构和默认管理员用户
"""

import mysql.connector
from mysql.connector import Error
import os
import sys

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'MySQL',
    'password': 'MySQL',
    'database': 'meal_system'
}

# SQL语句
CREATE_DATABASE_SQL = "CREATE DATABASE IF NOT EXISTS meal_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"

CREATE_USERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- admin, customer, employee
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL
)
"""

CREATE_CUSTOMERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    name VARCHAR(50) NOT NULL,
    age INT,
    gender VARCHAR(10),
    contact VARCHAR(100),
    delivery_date DATE,
    check_in_date DATE,
    check_out_date DATE,
    dietary_restrictions TEXT,
    preferences TEXT,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id)
)
"""

CREATE_EMPLOYEES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    name VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    contact VARCHAR(100),
    base_salary DECIMAL(10, 2) NOT NULL,
    joining_date DATE NOT NULL,
    education TEXT,
    work_experience TEXT,
    work_performance TEXT,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id)
)
"""

def create_connection():
    """创建数据库连接"""
    connection = None
    try:
        # 先连接到MySQL服务器
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        print("成功连接到MySQL服务器")
        return connection
    except Error as e:
        print(f"连接错误: {e}")
        return None

def create_database(connection):
    """创建数据库"""
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_DATABASE_SQL)
        print("成功创建数据库 meal_system")
        cursor.close()
    except Error as e:
        print(f"创建数据库错误: {e}")

def connect_to_database():
    """连接到具体数据库"""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        print("成功连接到数据库 meal_system")
        return connection
    except Error as e:
        print(f"连接数据库错误: {e}")
        return None

def create_tables(connection):
    """创建表结构"""
    try:
        cursor = connection.cursor()
        # 创建用户表
        cursor.execute(CREATE_USERS_TABLE_SQL)
        print("成功创建用户表")
        
        # 创建客户表
        cursor.execute(CREATE_CUSTOMERS_TABLE_SQL)
        print("成功创建客户表")
        
        # 创建员工表
        cursor.execute(CREATE_EMPLOYEES_TABLE_SQL)
        print("成功创建员工表")
        
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"创建表错误: {e}")
        connection.rollback()

def create_admin_user(connection):
    """创建默认管理员用户"""
    try:
        cursor = connection.cursor()
        
        # 检查admin用户是否已存在
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        existing_user = cursor.fetchone()
        
        if existing_user:
            print("管理员用户已存在，跳过创建")
        else:
            # 创建密码哈希 (使用简单的哈希模拟，实际应用中应使用更安全的方法)
            # 这里使用明文密码 'admin123' 的简单哈希表示
            password_hash = 'pbkdf2:sha256:150000$admin$admin123'  # 模拟哈希
            
            # 插入管理员用户
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                ('admin', password_hash, 'admin')
            )
            connection.commit()
            print("成功创建默认管理员用户: admin/admin123")
        
        cursor.close()
    except Error as e:
        print(f"创建管理员用户错误: {e}")
        connection.rollback()

def main():
    """主函数"""
    print("开始初始化数据库...")
    
    # 1. 连接到MySQL服务器
    server_connection = create_connection()
    if not server_connection:
        print("无法连接到MySQL服务器，请检查数据库配置")
        return
    
    # 2. 创建数据库
    create_database(server_connection)
    server_connection.close()
    
    # 3. 连接到数据库
    db_connection = connect_to_database()
    if not db_connection:
        print("无法连接到数据库，请检查数据库配置")
        return
    
    # 4. 创建表结构
    create_tables(db_connection)
    
    # 5. 创建默认管理员用户
    create_admin_user(db_connection)
    
    # 6. 关闭连接
    db_connection.close()
    
    print("数据库初始化完成！")
    print("默认管理员账号:")
    print("  用户名: admin")
    print("  密码: admin123")

if __name__ == "__main__":
    main()

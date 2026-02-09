# 餐食关系系统后端API设计文档

## 1. 架构概述

### 1.1 技术栈

- **语言**：Python 3.8+
- **Web框架**：Flask 2.0+
- **ORM**：SQLAlchemy 1.4+
- **数据库**：MySQL
- **认证**：JWT（JSON Web Token）
- **缓存**：Redis（可选，用于提升性能）
- **支付集成**：微信支付API、支付宝API、银行卡支付API

### 1.2 架构风格

- **RESTful API**：使用HTTP方法和状态码表示操作和结果
- **分层架构**：
  - **路由层**：处理HTTP请求和响应
  - **业务逻辑层**：实现核心业务逻辑
  - **数据访问层**：与数据库交互
  - **服务层**：提供外部服务集成

### 1.3 多平台支持

- **API设计**：统一的RESTful API，支持所有平台
- **认证机制**：JWT token认证，无状态，便于水平扩展
- **响应格式**：统一的JSON格式，包含状态码、消息和数据
- **错误处理**：标准化的错误响应格式

### 1.4 部署方案

- **开发环境**：本地开发服务器
- **测试环境**：专用测试服务器
- **生产环境**：Docker容器化部署，支持负载均衡

## 2. 目录结构

```
backend/
├── app/
│   ├── __init__.py          # 应用初始化
│   ├── config.py            # 配置文件
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py          # 用户模型
│   │   ├── customer.py      # 客户模型
│   │   ├── dish.py          # 菜品模型
│   │   ├── employee.py      # 员工模型
│   │   ├── financial.py     # 财务模型
│   │   └── payment.py       # 支付模型
│   ├── routes/              # API路由
│   │   ├── __init__.py
│   │   ├── auth.py          # 认证路由
│   │   ├── customer.py      # 客户路由
│   │   ├── dish.py          # 菜品路由
│   │   ├── employee.py      # 员工路由
│   │   ├── financial.py     # 财务路由
│   │   ├── payment.py       # 支付路由
│   │   └── wechat.py        # 微信小程序路由
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   ├── auth_service.py  # 认证服务
│   │   ├── customer_service.py  # 客户服务
│   │   ├── dish_service.py  # 菜品服务
│   │   ├── employee_service.py  # 员工服务
│   │   ├── financial_service.py  # 财务服务
│   │   ├── payment_service.py  # 支付服务
│   │   └── wechat_service.py  # 微信服务
│   ├── utils/               # 工具函数
│   │   ├── __init__.py
│   │   ├── jwt.py           # JWT工具
│   │   ├── password.py      # 密码工具
│   │   ├── logger.py        # 日志工具
│   │   └── backup.py        # 备份工具
│   └── middlewares/         # 中间件
│       ├── __init__.py
│       ├── auth.py          # 认证中间件
│       ├── cors.py          # CORS中间件
│       └── error.py         # 错误处理中间件
├── migrations/              # 数据库迁移
├── tests/                   # 测试代码
├── requirements.txt         # 依赖文件
├── run.py                   # 启动脚本
└── Dockerfile               # Docker配置
```

## 3. API接口设计

### 3.1 认证接口

#### 3.1.1 登录

- **URL**：`/api/auth/login`
- **方法**：POST
- **参数**：
  - `username`：用户名（必填）
  - `password`：密码（必填）
- **响应**：
  ```json
  {
    "code": 200,
    "message": "登录成功",
    "data": {
      "token": "jwt_token",
      "user": {
        "id": 1,
        "username": "admin",
        "role": "admin",
        "name": "管理员"
      }
    }
  }
  ```

#### 3.1.2 微信登录

- **URL**：`/api/auth/wechat/login`
- **方法**：POST
- **参数**：
  - `code`：微信登录码（必填）
- **响应**：
  ```json
  {
    "code": 200,
    "message": "登录成功",
    "data": {
      "token": "jwt_token",
      "user": {
        "id": 2,
        "username": "wechat_user",
        "role": "customer",
        "name": "微信用户"
      }
    }
  }
  ```

#### 3.1.3 刷新token

- **URL**：`/api/auth/refresh`
- **方法**：POST
- **参数**：无（使用Authorization头）
- **响应**：
  ```json
  {
    "code": 200,
    "message": "刷新成功",
    "data": {
      "token": "new_jwt_token"
    }
  }
  ```

### 3.2 客户接口

#### 3.2.1 获取客户列表

- **URL**：`/api/customers`
- **方法**：GET
- **参数**：
  - `page`：页码（默认1）
  - `page_size`：每页数量（默认10）
  - `search`：搜索关键词
  - `status`：状态筛选
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "total": 100,
      "page": 1,
      "page_size": 10,
      "items": [
        {
          "id": 1,
          "name": "张三",
          "age": 30,
          "gender": "女",
          "contact": "13800138000",
          "delivery_date": "2024-01-01",
          "check_in_date": "2024-01-02",
          "status": "active"
        }
      ]
    }
  }
  ```

#### 3.2.2 获取客户详情

- **URL**：`/api/customers/<id>`
- **方法**：GET
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "id": 1,
      "name": "张三",
      "age": 30,
      "gender": "女",
      "contact": "13800138000",
      "delivery_date": "2024-01-01",
      "check_in_date": "2024-01-02",
      "check_out_date": null,
      "dietary_restrictions": "海鲜、辣",
      "preferences": "清淡",
      "status": "active"
    }
  }
  ```

#### 3.2.3 添加客户

- **URL**：`/api/customers`
- **方法**：POST
- **参数**：
  - `name`：姓名（必填）
  - `age`：年龄
  - `gender`：性别
  - `contact`：联系方式
  - `delivery_date`：预产期/分娩日期
  - `check_in_date`：入住日期
  - `dietary_restrictions`：饮食禁忌
  - `preferences`：口味偏好
- **响应**：
  ```json
  {
    "code": 201,
    "message": "添加成功",
    "data": {
      "id": 2,
      "name": "李四",
      "age": 28,
      "gender": "女",
      "contact": "13900139000",
      "delivery_date": "2024-02-01",
      "check_in_date": "2024-02-02",
      "status": "active"
    }
  }
  ```

#### 3.2.4 更新客户

- **URL**：`/api/customers/<id>`
- **方法**：PUT
- **参数**：
  - `name`：姓名
  - `age`：年龄
  - `gender`：性别
  - `contact`：联系方式
  - `delivery_date`：预产期/分娩日期
  - `check_in_date`：入住日期
  - `check_out_date`：退房日期
  - `dietary_restrictions`：饮食禁忌
  - `preferences`：口味偏好
  - `status`：状态
- **响应**：
  ```json
  {
    "code": 200,
    "message": "更新成功",
    "data": {
      "id": 1,
      "name": "张三",
      "age": 30,
      "gender": "女",
      "contact": "13800138000",
      "delivery_date": "2024-01-01",
      "check_in_date": "2024-01-02",
      "check_out_date": "2024-01-10",
      "status": "inactive"
    }
  }
  ```

#### 3.2.5 删除客户

- **URL**：`/api/customers/<id>`
- **方法**：DELETE
- **响应**：
  ```json
  {
    "code": 200,
    "message": "删除成功"
  }
  ```

### 3.3 菜品接口

#### 3.3.1 获取菜品列表

- **URL**：`/api/dishes`
- **方法**：GET
- **参数**：
  - `page`：页码（默认1）
  - `page_size`：每页数量（默认10）
  - `category`：分类筛选
  - `search`：搜索关键词
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "total": 50,
      "page": 1,
      "page_size": 10,
      "items": [
        {
          "id": 1,
          "name": "清蒸鱼",
          "category": "肉菜",
          "description": "清淡可口",
          "ingredients": "鱼、姜、葱",
          "restrictions": "无",
          "calories": 200,
          "price": 58.00,
          "status": "active"
        }
      ]
    }
  }
  ```

#### 3.3.2 获取菜品详情

- **URL**：`/api/dishes/<id>`
- **方法**：GET
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "id": 1,
      "name": "清蒸鱼",
      "category": "肉菜",
      "description": "清淡可口",
      "ingredients": "鱼、姜、葱",
      "restrictions": "无",
      "calories": 200,
      "price": 58.00,
      "status": "active"
    }
  }
  ```

#### 3.3.3 添加菜品

- **URL**：`/api/dishes`
- **方法**：POST
- **参数**：
  - `name`：菜品名称（必填）
  - `category`：分类（必填）
  - `description`：描述
  - `ingredients`：食材组成
  - `restrictions`：禁忌食材
  - `calories`：卡路里
  - `price`：价格
- **响应**：
  ```json
  {
    "code": 201,
    "message": "添加成功",
    "data": {
      "id": 2,
      "name": "红烧肉",
      "category": "肉菜",
      "description": "肥而不腻",
      "ingredients": "五花肉、酱油、糖",
      "restrictions": "高血脂患者慎食",
      "calories": 350,
      "price": 68.00,
      "status": "active"
    }
  }
  ```

### 3.4 排餐接口

#### 3.4.1 获取排餐列表

- **URL**：`/api/menus`
- **方法**：GET
- **参数**：
  - `date`：日期（YYYY-MM-DD）
  - `type`：餐型（breakfast/lunch/dinner）
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": [
      {
        "id": 1,
        "date": "2024-01-01",
        "type": "lunch",
        "dishes": [
          {
            "id": 1,
            "name": "清蒸鱼",
            "category": "肉菜",
            "quantity": 2
          }
        ]
      }
    ]
  }
  ```

#### 3.4.2 自动排餐

- **URL**：`/api/menus/auto`
- **方法**：POST
- **参数**：
  - `date`：日期（必填）
  - `customer_ids`：客户ID列表
- **响应**：
  ```json
  {
    "code": 200,
    "message": "排餐成功",
    "data": {
      "breakfast": {
        "id": 1,
        "date": "2024-01-01",
        "type": "breakfast",
        "dishes": []
      },
      "lunch": {
        "id": 2,
        "date": "2024-01-01",
        "type": "lunch",
        "dishes": []
      },
      "dinner": {
        "id": 3,
        "date": "2024-01-01",
        "type": "dinner",
        "dishes": []
      }
    }
  }
  ```

### 3.5 员工接口

#### 3.5.1 获取员工列表

- **URL**：`/api/employees`
- **方法**：GET
- **参数**：
  - `page`：页码（默认1）
  - `page_size`：每页数量（默认10）
  - `position`：职位筛选
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "total": 20,
      "page": 1,
      "page_size": 10,
      "items": [
        {
          "id": 1,
          "name": "王五",
          "position": "厨师",
          "contact": "13700137000",
          "base_salary": 5000.00,
          "joining_date": "2023-01-01",
          "status": "active"
        }
      ]
    }
  }
  ```

#### 3.5.2 员工考勤打卡

- **URL**：`/api/employees/attendance`
- **方法**：POST
- **参数**：
  - `employee_id`：员工ID（必填）
  - `type`：打卡类型（check_in/check_out）
- **响应**：
  ```json
  {
    "code": 200,
    "message": "打卡成功",
    "data": {
      "id": 1,
      "employee_id": 1,
      "date": "2024-01-01",
      "check_in_time": "08:00:00",
      "check_out_time": null,
      "status": "present"
    }
  }
  ```

#### 3.5.3 员工工作量统计

- **URL**：`/api/employees/workload`
- **方法**：GET
- **参数**：
  - `employee_id`：员工ID
  - `start_date`：开始日期
  - `end_date`：结束日期
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "employee_id": 1,
      "employee_name": "王五",
      "period": "2024-01-01至2024-01-31",
      "total_hours": 160,
      "overtime_hours": 10,
      "accompany_hours": 20,
      "care_hours": 15
    }
  }
  ```

### 3.6 财务接口

#### 3.6.1 获取收支记录

- **URL**：`/api/finance/transactions`
- **方法**：GET
- **参数**：
  - `page`：页码（默认1）
  - `page_size`：每页数量（默认10）
  - `type`：类型（income/expense）
  - `start_date`：开始日期
  - `end_date`：结束日期
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "total": 200,
      "page": 1,
      "page_size": 10,
      "items": [
        {
          "id": 1,
          "type": "income",
          "category": "餐费",
          "amount": 1000.00,
          "description": "张三的餐费",
          "transaction_date": "2024-01-01T10:00:00",
          "payment_method": "wechat",
          "status": "completed",
          "related_id": 1,
          "related_type": "customer"
        }
      ]
    }
  }
  ```

#### 3.6.2 添加收支记录

- **URL**：`/api/finance/transactions`
- **方法**：POST
- **参数**：
  - `type`：类型（income/expense）
  - `category`：分类
  - `amount`：金额
  - `description`：描述
  - `payment_method`：支付方式
  - `related_id`：关联ID
  - `related_type`：关联类型
- **响应**：
  ```json
  {
    "code": 201,
    "message": "添加成功",
    "data": {
      "id": 2,
      "type": "expense",
      "category": "食材采购",
      "amount": 500.00,
      "description": "购买蔬菜",
      "transaction_date": "2024-01-01T14:00:00",
      "payment_method": "alipay",
      "status": "completed",
      "related_id": 1,
      "related_type": "supplier"
    }
  }
  ```

#### 3.6.3 生成财务报表

- **URL**：`/api/finance/reports`
- **方法**：GET
- **参数**：
  - `report_type`：报表类型（daily/weekly/monthly/yearly）
  - `start_date`：开始日期
  - `end_date`：结束日期
- **响应**：
  ```json
  {
    "code": 200,
    "message": "生成成功",
    "data": {
      "report_type": "monthly",
      "period": "2024-01",
      "income": 50000.00,
      "expense": 30000.00,
      "profit": 20000.00,
      "details": {
        "income": [
          {"category": "餐费", "amount": 40000.00},
          {"category": "服务费", "amount": 10000.00}
        ],
        "expense": [
          {"category": "食材采购", "amount": 15000.00},
          {"category": "员工薪资", "amount": 10000.00},
          {"category": "其他", "amount": 5000.00}
        ]
      }
    }
  }
  ```

#### 3.6.4 计算员工薪资

- **URL**：`/api/finance/salary/calculate`
- **方法**：POST
- **参数**：
  - `employee_id`：员工ID
  - `pay_period`：薪资周期
- **响应**：
  ```json
  {
    "code": 200,
    "message": "计算成功",
    "data": {
      "id": 1,
      "employee_id": 1,
      "employee_name": "王五",
      "pay_period": "2024-01",
      "base_salary": 5000.00,
      "overtime_pay": 500.00,
      "allowance": 300.00,
      "deductions": 200.00,
      "net_salary": 5600.00
    }
  }
  ```

### 3.7 支付接口

#### 3.7.1 创建支付订单

- **URL**：`/api/payment/orders`
- **方法**：POST
- **参数**：
  - `amount`：金额（必填）
  - `payment_method`：支付方式（wechat/alipay/bank）
  - `order_type`：订单类型（customer_order/salary/supplier_payment）
  - `related_id`：关联ID
- **响应**：
  ```json
  {
    "code": 201,
    "message": "创建成功",
    "data": {
      "order_id": "P202401010001",
      "amount": 1000.00,
      "payment_method": "wechat",
      "payment_url": "weixin://wxpay/bizpayurl?pr=xxx",
      "expire_time": "2024-01-01T11:00:00"
    }
  }
  ```

#### 3.7.2 支付回调

- **URL**：`/api/payment/callback/<payment_method>`
- **方法**：POST
- **参数**：支付平台回调参数
- **响应**：
  ```json
  {
    "code": 200,
    "message": "处理成功"
  }
  ```

#### 3.7.3 查询支付状态

- **URL**：`/api/payment/orders/<order_id>`
- **方法**：GET
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "order_id": "P202401010001",
      "amount": 1000.00,
      "payment_method": "wechat",
      "status": "paid",
      "transaction_time": "2024-01-01T10:30:00"
    }
  }
  ```

### 3.8 微信小程序接口

#### 3.8.1 客户端接口

##### 3.8.1.1 获取今日餐单

- **URL**：`/api/wechat/customer/menu`
- **方法**：GET
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "date": "2024-01-01",
      "breakfast": [
        {
          "id": 1,
          "name": "小米粥",
          "category": "汤品",
          "description": "营养丰富"
        }
      ],
      "lunch": [],
      "dinner": []
    }
  }
  ```

##### 3.8.1.2 提交预约

- **URL**：`/api/wechat/customer/appointment`
- **方法**：POST
- **参数**：
  - `service_type`：服务类型
  - `date`：预约日期
  - `time`：预约时间
  - `requirements`：特殊需求
- **响应**：
  ```json
  {
    "code": 201,
    "message": "预约成功",
    "data": {
      "appointment_id": 1,
      "service_type": "陪护",
      "date": "2024-01-02",
      "time": "14:00",
      "status": "pending"
    }
  }
  ```

#### 3.8.2 管理端接口

##### 3.8.2.1 获取工作台数据

- **URL**：`/api/wechat/admin/dashboard`
- **方法**：GET
- **响应**：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "today_customers": 10,
      "today_orders": 5,
      "pending_tasks": 3,
      "recent_notifications": [
        {
          "id": 1,
          "title": "新客户预约",
          "content": "张三预约了明天的服务",
          "time": "2024-01-01T09:00:00"
        }
      ]
    }
  }
  ```

##### 3.8.2.2 员工打卡

- **URL**：`/api/wechat/admin/attendance`
- **方法**：POST
- **参数**：
  - `type`：打卡类型（check_in/check_out）
- **响应**：
  ```json
  {
    "code": 200,
    "message": "打卡成功",
    "data": {
      "status": "success",
      "message": "上班打卡成功，时间：08:00:00"
    }
  }
  ```

## 4. 认证与授权

### 4.1 认证机制

- **JWT Token**：使用JSON Web Token进行身份认证
- **Token生成**：登录成功后生成，包含用户ID、角色等信息
- **Token验证**：每次API请求通过Authorization头携带token
- **Token过期**：设置合理的过期时间，支持刷新token

### 4.2 授权机制

- **基于角色的访问控制（RBAC）**：
  - **客户**：只能访问自己的信息、餐单、预约等
  - **员工**：可以访问工作相关的信息，如考勤、工作量等
  - **管理员**：可以访问所有信息，具有全部操作权限

### 4.3 权限管理

- **权限定义**：在数据库中定义权限列表
- **角色权限**：为不同角色分配不同权限
- **权限检查**：API请求时检查用户是否有权限执行操作

## 5. 错误处理

### 5.1 错误响应格式

```json
{
  "code": 400,
  "message": "请求参数错误",
  "data": {
    "field": "name",
    "error": "姓名不能为空"
  }
}
```

### 5.2 错误码定义

- **200**：成功
- **201**：创建成功
- **400**：请求参数错误
- **401**：未授权
- **403**：禁止访问
- **404**：资源不存在
- **500**：服务器内部错误

### 5.3 异常处理

- **全局异常处理**：捕获所有未处理的异常
- **业务异常**：自定义业务异常类，处理业务逻辑错误
- **数据库异常**：处理数据库操作错误
- **第三方服务异常**：处理支付、微信等第三方服务错误

## 6. 性能优化

### 6.1 数据库优化

- **索引设计**：为常用查询字段创建索引
- **查询优化**：使用ORM的延迟加载、批量查询等特性
- **数据库连接池**：使用连接池管理数据库连接
- **缓存**：缓存热点数据，减少数据库查询

### 6.2 API优化

- **分页**：所有列表接口支持分页
- **字段过滤**：支持只返回需要的字段
- **批量操作**：支持批量添加、更新、删除
- **异步处理**：耗时操作使用异步处理

### 6.3 缓存策略

- **Redis缓存**：使用Redis缓存热点数据
- **缓存失效策略**：合理设置缓存过期时间
- **缓存一致性**：确保缓存与数据库数据一致

### 6.4 部署优化

- **Docker容器化**：使用Docker容器化部署
- **负载均衡**：多实例部署，使用负载均衡
- **CDN**：静态资源使用CDN加速

## 7. 安全措施

### 7.1 数据安全

- **密码加密**：使用bcrypt等算法加密存储密码
- **数据传输加密**：使用HTTPS传输数据
- **敏感数据加密**：敏感数据加密存储
- **SQL注入防护**：使用ORM和参数化查询

### 7.2 API安全

- **CORS配置**：合理配置跨域资源共享
- **请求频率限制**：防止API滥用
- **输入验证**：严格验证所有输入参数
- **XSS防护**：防止跨站脚本攻击

### 7.3 操作安全

- **操作日志**：记录所有敏感操作
- **权限控制**：严格的权限检查
- **数据备份**：定期备份数据库
- **应急响应**：制定安全事件应急响应方案

## 8. 监控与日志

### 8.1 日志系统

- **日志级别**：DEBUG、INFO、WARNING、ERROR、CRITICAL
- **日志格式**：包含时间、级别、模块、消息等信息
- **日志存储**：按日期分割，定期归档
- **日志分析**：使用ELK等工具分析日志

### 8.2 监控系统

- **系统监控**：CPU、内存、磁盘等系统资源监控
- **API监控**：API响应时间、错误率监控
- **数据库监控**：数据库连接数、查询性能监控
- **告警机制**：设置阈值，超过阈值时告警

## 9. 扩展性考虑

### 9.1 模块扩展

- **插件系统**：支持功能插件扩展
- **服务注册**：新服务自动注册到系统
- **配置管理**：集中管理配置，支持动态配置

### 9.2 数据扩展

- **数据库分表**：大数据表考虑分表
- **数据分片**：支持水平分片
- **读写分离**：支持主从复制，读写分离

### 9.3 服务扩展

- **微服务架构**：可逐步拆分为微服务
- **消息队列**：使用消息队列解耦服务
- **API网关**：统一API入口，支持限流、认证等

## 10. 总结

本API设计文档详细描述了餐食关系系统的后端API架构和接口设计。系统采用RESTful API风格，使用Flask框架实现，支持多平台访问，集成了财务系统和支付功能。

API设计遵循了RESTful原则，提供了统一的接口格式和错误处理机制，确保了系统的可维护性和可扩展性。同时，设计还考虑了安全性、性能优化和监控等方面，确保系统的稳定运行。

通过本设计，系统将为前端应用和微信小程序提供强大的后端支持，实现完整的餐食关系管理功能。

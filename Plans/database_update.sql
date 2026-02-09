-- 餐食管理系统数据库更新脚本
-- 日期：2026-02-09

-- 1. 扩展食材表，添加营养成分、热量、禁忌、购买人等字段
ALTER TABLE ingredients
ADD COLUMN nutrition_info TEXT COMMENT '营养成分',
ADD COLUMN calories DECIMAL(10,2) COMMENT '热量',
ADD COLUMN restrictions TEXT COMMENT '禁忌',
ADD COLUMN purchaser_id INTEGER COMMENT '购买人ID，关联employees表',
ADD COLUMN purchase_date DATE COMMENT '购买日期',
ADD COLUMN stock_in_date DATE COMMENT '入库日期',
ADD COLUMN stock_out_date DATE COMMENT '出库日期',
ADD COLUMN last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
ADD FOREIGN KEY (purchaser_id) REFERENCES employees(id);

-- 2. 创建食材与菜品的关联表，实现多对多关系
CREATE TABLE ingredient_dish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    quantity DECIMAL(10,2) NOT NULL COMMENT '使用量',
    unit VARCHAR(20) NOT NULL COMMENT '单位',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    FOREIGN KEY (dish_id) REFERENCES dishes(id),
    UNIQUE(ingredient_id, dish_id)
);

-- 3. 扩展员工表，添加学历、经历、工作业绩等字段
ALTER TABLE employees
ADD COLUMN education VARCHAR(100) COMMENT '学历',
ADD COLUMN experience TEXT COMMENT '工作经历',
ADD COLUMN achievements TEXT COMMENT '工作业绩',
ADD COLUMN department VARCHAR(50) COMMENT '部门',
ADD COLUMN hire_date DATE COMMENT '入职日期',
ADD COLUMN last_promotion_date DATE COMMENT '最后晋升日期',
ADD COLUMN performance_rating DECIMAL(3,1) COMMENT '绩效评分',
ADD COLUMN skills TEXT COMMENT '技能特长';

-- 4. 更新订单相关表
-- 4.1 修改客户订单表，添加订单类型和预定人信息
ALTER TABLE customer_orders
ADD COLUMN order_type VARCHAR(20) NOT NULL DEFAULT 'meal' COMMENT '订单类型（meal/service）',
ADD COLUMN orderer_name VARCHAR(50) COMMENT '预定人姓名',
ADD COLUMN orderer_role VARCHAR(20) COMMENT '预定人角色（customer/employee/dietitian）',
ADD COLUMN start_time DATETIME COMMENT '开始时间',
ADD COLUMN end_time DATETIME COMMENT '结束时间',
ADD COLUMN duration DECIMAL(5,2) COMMENT '时长（小时）',
ADD COLUMN service_employee_id INTEGER COMMENT '服务员工ID',
ADD COLUMN rating INTEGER COMMENT '评分（1-5）',
ADD COLUMN review TEXT COMMENT '评价',
ADD FOREIGN KEY (service_employee_id) REFERENCES employees(id);

-- 4.2 修改订单明细表，适应服务订单
ALTER TABLE order_items
ADD COLUMN service_item_name VARCHAR(100) COMMENT '服务项目名称（当item_type为service时使用）',
ADD COLUMN service_description TEXT COMMENT '服务描述';

-- 5. 创建服务项目表和服务项目价格表
-- 5.1 服务项目表
CREATE TABLE service_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '服务项目名称',
    category VARCHAR(50) NOT NULL COMMENT '服务类别（如母婴服务）',
    description TEXT COMMENT '服务描述',
    duration DECIMAL(5,2) NOT NULL COMMENT '服务时长（小时）',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 5.2 服务项目价格表
CREATE TABLE service_item_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_item_id INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL COMMENT '价格',
    effective_date DATE NOT NULL COMMENT '生效日期',
    expire_date DATE COMMENT '失效日期',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (service_item_id) REFERENCES service_items(id)
);

-- 6. 完善工作量表，实现与订单的关联
ALTER TABLE workload
ADD COLUMN order_id INTEGER COMMENT '关联订单ID',
ADD COLUMN service_item_id INTEGER COMMENT '关联服务项目ID',
ADD COLUMN customer_id INTEGER COMMENT '关联客户ID',
ADD FOREIGN KEY (order_id) REFERENCES customer_orders(id),
ADD FOREIGN KEY (service_item_id) REFERENCES service_items(id),
ADD FOREIGN KEY (customer_id) REFERENCES customers(id);

-- 7. 完善薪资表，添加奖金和补助字段
ALTER TABLE salary
ADD COLUMN bonus DECIMAL(10,2) DEFAULT 0 COMMENT '奖金',
ADD COLUMN allowance DECIMAL(10,2) DEFAULT 0 COMMENT '补助',
ADD COLUMN workload_based_pay DECIMAL(10,2) DEFAULT 0 COMMENT '基于工作量的工资',
ADD COLUMN performance_bonus DECIMAL(10,2) DEFAULT 0 COMMENT '绩效奖金';

-- 8. 创建营养成分和禁忌冲突管理相关表
-- 8.1 营养成分表
CREATE TABLE nutrition_facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '营养成分名称',
    unit VARCHAR(20) NOT NULL COMMENT '单位',
    description TEXT COMMENT '描述'
);

-- 8.2 食材营养成分表
CREATE TABLE ingredient_nutrition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER NOT NULL,
    nutrition_id INTEGER NOT NULL,
    value DECIMAL(10,2) NOT NULL COMMENT '含量',
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    FOREIGN KEY (nutrition_id) REFERENCES nutrition_facts(id)
);

-- 8.3 禁忌表
CREATE TABLE restrictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '禁忌名称',
    type VARCHAR(20) NOT NULL COMMENT '禁忌类型（dietary/health）',
    description TEXT COMMENT '描述'
);

-- 8.4 食材禁忌表
CREATE TABLE ingredient_restrictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER NOT NULL,
    restriction_id INTEGER NOT NULL,
    severity VARCHAR(20) COMMENT '严重程度（mild/moderate/severe）',
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    FOREIGN KEY (restriction_id) REFERENCES restrictions(id)
);

-- 8.5 客户禁忌表
CREATE TABLE customer_restrictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    restriction_id INTEGER NOT NULL,
    notes TEXT COMMENT '备注',
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (restriction_id) REFERENCES restrictions(id)
);

-- 9. 添加数据流程控制，包括触发器和存储过程

-- 9.1 触发器：当订单状态更新时，自动更新员工工作量
CREATE TRIGGER update_workload_after_order_update
AFTER UPDATE ON customer_orders
FOR EACH ROW
BEGIN
    -- 当订单类型为服务订单且状态为已完成时，更新工作量
    IF NEW.order_type = 'service' AND NEW.payment_status = 'paid' THEN
        INSERT INTO workload (employee_id, date, work_type, hours, description, order_id, service_item_id, customer_id)
        VALUES (NEW.service_employee_id, DATE(NEW.end_time), 'service', NEW.duration, 
                CONCAT('服务订单: ', NEW.orderer_name), NEW.id, 
                (SELECT item_id FROM order_items WHERE order_id = NEW.id LIMIT 1), 
                NEW.customer_id)
        ON CONFLICT(order_id) DO UPDATE SET
            hours = NEW.duration,
            description = CONCAT('服务订单: ', NEW.orderer_name);
    END IF;
END;

-- 9.2 触发器：当食材库存低于最低库存时，生成预警
CREATE TRIGGER inventory_alert_trigger
AFTER UPDATE ON ingredients
FOR EACH ROW
BEGIN
    IF NEW.current_stock < NEW.minimum_stock THEN
        -- 这里可以插入预警记录到预警表
        -- 假设有一个预警表 alert_records
        -- INSERT INTO alert_records (type, message, related_id, status) 
        -- VALUES ('inventory', CONCAT('食材 ', NEW.name, ' 库存不足'), NEW.id, 'pending');
    END IF;
END;

-- 9.3 存储过程：计算员工薪资（基于工作量）
DELIMITER //
CREATE PROCEDURE calculate_salary(IN employee_id INT, IN pay_period VARCHAR(20))
BEGIN
    DECLARE base_salary DECIMAL(10,2);
    DECLARE total_work_hours DECIMAL(10,2);
    DECLARE overtime_hours DECIMAL(10,2);
    DECLARE workload_pay DECIMAL(10,2);
    DECLARE bonus DECIMAL(10,2);
    DECLARE allowance DECIMAL(10,2);
    DECLARE deductions DECIMAL(10,2);
    DECLARE net_salary DECIMAL(10,2);
    
    -- 获取员工基础薪资
    SELECT base_salary INTO base_salary FROM employees WHERE id = employee_id;
    
    -- 计算总工作时长和加班时长
    SELECT 
        SUM(hours) INTO total_work_hours
    FROM workload
    WHERE employee_id = employee_id
    AND date BETWEEN 
        CASE 
            WHEN pay_period LIKE '%-%' THEN SUBSTR(pay_period, 1, 10)
            ELSE DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
        END
    AND 
        CASE 
            WHEN pay_period LIKE '%-%' THEN SUBSTR(pay_period, 12, 10)
            ELSE CURRENT_DATE
        END;
    
    -- 计算加班时长（假设每月标准工作时长为160小时）
    SET overtime_hours = GREATEST(total_work_hours - 160, 0);
    
    -- 计算基于工作量的工资（假设每小时工资为基础薪资/160）
    SET workload_pay = (base_salary / 160) * total_work_hours;
    
    -- 计算奖金（假设为工作量工资的10%）
    SET bonus = workload_pay * 0.1;
    
    -- 计算补助（假设为固定值）
    SET allowance = 500;
    
    -- 计算扣除项（假设为基础薪资的20%）
    SET deductions = base_salary * 0.2;
    
    -- 计算实发工资
    SET net_salary = workload_pay + bonus + allowance - deductions;
    
    -- 插入或更新薪资记录
    INSERT INTO salary (employee_id, pay_period, base_salary, overtime_pay, allowance, deductions, net_salary, bonus, workload_based_pay, performance_bonus)
    VALUES (employee_id, pay_period, base_salary, (overtime_hours * (base_salary / 160) * 1.5), allowance, deductions, net_salary, bonus, workload_pay, bonus)
    ON CONFLICT(employee_id, pay_period) DO UPDATE SET
        base_salary = base_salary,
        overtime_pay = (overtime_hours * (base_salary / 160) * 1.5),
        allowance = allowance,
        deductions = deductions,
        net_salary = net_salary,
        bonus = bonus,
        workload_based_pay = workload_pay,
        performance_bonus = bonus;
    
    -- 返回计算结果
    SELECT * FROM salary WHERE employee_id = employee_id AND pay_period = pay_period;
END //
DELIMITER ;

-- 9.4 存储过程：基于订单计算员工工作量
DELIMITER //
CREATE PROCEDURE calculate_workload_from_orders(IN employee_id INT, IN start_date DATE, IN end_date DATE)
BEGIN
    -- 计算指定时间段内员工的服务订单工作量
    INSERT INTO workload (employee_id, date, work_type, hours, description, order_id, customer_id)
    SELECT 
        co.service_employee_id,
        DATE(co.end_time) as date,
        'service' as work_type,
        co.duration as hours,
        CONCAT('服务订单: ', co.orderer_name) as description,
        co.id as order_id,
        co.customer_id
    FROM customer_orders co
    WHERE co.service_employee_id = employee_id
    AND co.order_type = 'service'
    AND co.end_time BETWEEN start_date AND end_date
    AND co.id NOT IN (SELECT order_id FROM workload WHERE employee_id = employee_id);
    
    -- 返回计算结果
    SELECT * FROM workload 
    WHERE employee_id = employee_id
    AND date BETWEEN start_date AND end_date;
END //
DELIMITER ;

-- 10. 创建索引以优化查询性能
-- 食材表索引
CREATE INDEX idx_ingredients_category ON ingredients(category);
CREATE INDEX idx_ingredients_stock ON ingredients(current_stock, minimum_stock);

-- 订单表索引
CREATE INDEX idx_customer_orders_type ON customer_orders(order_type);
CREATE INDEX idx_customer_orders_time ON customer_orders(start_time, end_time);
CREATE INDEX idx_customer_orders_employee ON customer_orders(service_employee_id);

-- 工作量表索引
CREATE INDEX idx_workload_employee_date ON workload(employee_id, date);
CREATE INDEX idx_workload_order ON workload(order_id);

-- 薪资表索引
CREATE INDEX idx_salary_employee_period ON salary(employee_id, pay_period);

-- 服务项目表索引
CREATE INDEX idx_service_items_category ON service_items(category);

-- 服务项目价格表索引
CREATE INDEX idx_service_item_prices_item ON service_item_prices(service_item_id);
CREATE INDEX idx_service_item_prices_date ON service_item_prices(effective_date, expire_date);

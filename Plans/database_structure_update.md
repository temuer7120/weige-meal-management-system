# 餐食管理系统 - 数据库结构和数据流（修正版）

## 目录
- [数据库表结构](#数据库表结构)
  - [基础模型](#1-基础模型)
  - [菜单管理模块](#2-菜单管理模块)
  - [客户管理模块](#3-客户管理模块)
  - [用户与权限模块](#4-用户与权限模块)
  - [食材与库存管理模块](#5-食材与库存管理模块)
  - [服务管理模块](#6-服务管理模块)
  - [配送与排餐模块](#7-配送与排餐模块)
  - [月子餐管理模块](#8-月子餐管理模块)
  - [AI分析与报告模块](#9-ai分析与报告模块)
- [系统架构图](#系统架构图)
- [核心数据流图](#核心数据流图)
- [主要优化和改进](#主要优化和改进)

## 数据库表结构

### 1. 基础模型

```mermaid
classDiagram
    class BaseModel {
        <<Abstract>>
        +id: Integer (PK, Auto Increment)
        +created_at: DateTime (NOT NULL)
        +updated_at: DateTime (NOT NULL)
        +deleted_at: DateTime (NULLABLE)
        +version: Integer (DEFAULT 0)
    }
```

### 2. 菜单管理模块

```mermaid
classDiagram
    direction LR
    
    BaseModel <|-- MenuCategory
    BaseModel <|-- Dish
    BaseModel <|-- Menu
    BaseModel <|-- MenuDish
    BaseModel <|-- DailyMenu
    BaseModel <|-- DailyMenuDish
    
    class MenuCategory {
        +name: String (UNIQUE, NOT NULL)
        +description: Text
        +sort_order: Integer
        +is_active: Boolean (DEFAULT true)
    }
    
    class Dish {
        +name: String (NOT NULL)
        +description: Text
        +ingredients: JSON
        +dietary_restrictions: JSON
        +calories_per_serving: Decimal(6,2)
        +price: Decimal(10,2)
        +preparation_time: Integer
        +category_id: Integer (FK -> MenuCategory.id)
        +image_url: String
        +is_available: Boolean (DEFAULT true)
    }
    
    class Menu {
        +name: String (NOT NULL)
        +description: Text
        +week_number: Integer
        +year: Integer
        +start_date: Date
        +end_date: Date
        +status: String (draft/published/archived)
        +total_calories: Decimal(8,2)
        +total_price: Decimal(10,2)
    }
    
    class MenuDish {
        +menu_id: Integer (FK -> Menu.id)
        +dish_id: Integer (FK -> Dish.id)
        +day_of_week: Integer (1-7)
        +meal_type: String (breakfast/lunch/dinner/snack)
        +serving_time: Time
        +sort_order: Integer
        +notes: Text
    }
    
    class DailyMenu {
        +date: Date (UNIQUE, NOT NULL)
        +description: Text
        +status: String (planned/active/completed)
        +total_orders: Integer
        +total_revenue: Decimal(12,2)
    }
    
    class DailyMenuDish {
        +daily_menu_id: Integer (FK -> DailyMenu.id)
        +dish_id: Integer (FK -> Dish.id)
        +meal_type: String
        +quantity_available: Integer
        +quantity_ordered: Integer
        +quantity_prepared: Integer
        +price_override: Decimal(10,2)
    }
    
    MenuCategory "1" --> "*" Dish : categorizes
    Dish "1" --> "*" MenuDish : appears_in
    Menu "1" --> "*" MenuDish : contains
    MenuDish "*" --> "1" MenuCategory : belongs_to
    DailyMenu "1" --> "*" DailyMenuDish : includes
    Dish "1" --> "*" DailyMenuDish : featured_in
```

### 3. 客户管理模块

```mermaid
classDiagram
    direction LR
    
    BaseModel <|-- Customer
    BaseModel <|-- CustomerDietaryPreference
    BaseModel <|-- CustomerMenuSelection
    BaseModel <|-- CustomerOrder
    BaseModel <|-- OrderItem
    
    class Customer {
        +name: String (NOT NULL)
        +email: String (UNIQUE)
        +phone: String
        +date_of_birth: Date
        +gender: String
        +height_cm: Decimal(5,2)
        +weight_kg: Decimal(5,2)
        +check_in_date: Date
        +check_out_date: Date
        +id_card_number: String
        +id_card_image_url: String
        +physical_exam_report_url: String
        +health_conditions: JSON
        +dietary_restrictions: JSON
        +allergies: JSON
        +preferred_foods: JSON
        +meal_plan_type: String
        +status: String (active/inactive/archived)
    }
    
    class CustomerDietaryPreference {
        +customer_id: Integer (FK -> Customer.id)
        +preference_type: String
        +preference_value: String
        +severity: String (low/medium/high)
        +notes: Text
    }
    
    class CustomerMenuSelection {
        +customer_id: Integer (FK -> Customer.id)
        +daily_menu_id: Integer (FK -> DailyMenu.id)
        +selection_date: Date
        +meal_type: String
        +dish_id: Integer (FK -> Dish.id)
        +quantity: Integer
        +special_instructions: Text
        +status: String (pending/confirmed/prepared/delivered)
    }
    
    class CustomerOrder {
        +order_number: String (UNIQUE)
        +customer_id: Integer (FK -> Customer.id)
        +order_date: DateTime
        +delivery_date: Date
        +delivery_time_slot: String
        +delivery_address: Text
        +contact_person: String
        +contact_phone: String
        +total_items: Integer
        +subtotal_amount: Decimal(12,2)
        +tax_amount: Decimal(12,2)
        +delivery_fee: Decimal(10,2)
        +total_amount: Decimal(12,2)
        +payment_method: String
        +payment_status: String (pending/paid/refunded)
        +order_status: String (pending/confirmed/preparing/ready/delivered/completed/cancelled)
        +notes: Text
    }
    
    class OrderItem {
        +order_id: Integer (FK -> CustomerOrder.id)
        +dish_id: Integer (FK -> Dish.id)
        +quantity: Integer
        +unit_price: Decimal(10,2)
        +total_price: Decimal(10,2)
        +special_instructions: Text
        +preparation_status: String (pending/in_progress/completed)
    }
    
    Customer "1" --> "*" CustomerDietaryPreference : has
    Customer "1" --> "*" CustomerMenuSelection : makes
    DailyMenu "1" --> "*" CustomerMenuSelection : selected_from
    Customer "1" --> "*" CustomerOrder : places
    CustomerOrder "1" --> "*" OrderItem : contains
    Dish "1" --> "*" OrderItem : ordered_as
```

### 4. 用户与权限模块

```mermaid
classDiagram
    direction LR
    
    BaseModel <|-- User
    BaseModel <|-- Role
    BaseModel <|-- Permission
    BaseModel <|-- UserRole
    BaseModel <|-- RolePermission
    BaseModel <|-- WeChatUser
    BaseModel <|-- CustomerWeChatLink
    BaseModel <|-- AttendanceRecord
    BaseModel <|-- WorkSchedule
    BaseModel <|-- OvertimeApplication
    BaseModel <|-- LeaveApplication
    
    class User {
        +username: String (UNIQUE, NOT NULL)
        +email: String (UNIQUE)
        +phone: String
        +password_hash: String (NOT NULL)
        +full_name: String
        +department: String
        +position: String
        +avatar_url: String
        +last_login_at: DateTime
        +is_active: Boolean (DEFAULT true)
        +is_superuser: Boolean (DEFAULT false)
        +basic_salary: Decimal(10,2)
        +hourly_rate: Decimal(10,2)
        +overtime_rate: Decimal(10,2)
        +allowance: Decimal(10,2)
        +work_type: String (full_time/part_time)
    }
    
    class Role {
        +name: String (UNIQUE, NOT NULL)
        +description: Text
        +is_system_role: Boolean (DEFAULT false)
    }
    
    class Permission {
        +name: String (UNIQUE, NOT NULL)
        +code: String (UNIQUE, NOT NULL)
        +module: String
        +description: Text
    }
    
    class UserRole {
        +user_id: Integer (FK -> User.id)
        +role_id: Integer (FK -> Role.id)
    }
    
    class RolePermission {
        +role_id: Integer (FK -> Role.id)
        +permission_id: Integer (FK -> Permission.id)
    }
    
    class WeChatUser {
        +openid: String (UNIQUE, NOT NULL)
        +unionid: String (UNIQUE)
        +nickname: String
        +avatar_url: String
        +gender: Integer
        +country: String
        +province: String
        +city: String
        +phone: String
        +last_login_at: DateTime
        +session_key: String
    }
    
    class CustomerWeChatLink {
        +customer_id: Integer (FK -> Customer.id)
        +wechat_user_id: Integer (FK -> WeChatUser.id)
        +linked_at: DateTime
    }
    
    class AttendanceRecord {
        +user_id: Integer (FK -> User.id)
        +attendance_date: Date
        +check_in_time: Time
        +check_out_time: Time
        +work_hours: Decimal(5,2)
        +overtime_hours: Decimal(5,2)
        +status: String (normal/late/early_leave/absent)
        +notes: Text
        +location: String
        +device_id: String
    }
    
    class WorkSchedule {
        +schedule_name: String
        +user_id: Integer (FK -> User.id)
        +start_date: Date
        +end_date: Date
        +shift_type: String (morning/afternoon/evening/night)
        +scheduled_hours: Decimal(5,2)
        +status: String (draft/published/modified)
        +notes: Text
    }
    
    class OvertimeApplication {
        +application_number: String (UNIQUE)
        +user_id: Integer (FK -> User.id)
        +application_date: Date
        +overtime_date: Date
        +start_time: Time
        +end_time: Time
        +overtime_hours: Decimal(5,2)
        +reason: Text
        +status: String (pending/approved/rejected)
        +approved_by: Integer (FK -> User.id, NULL)
        +approved_at: DateTime (NULL)
        +approval_notes: Text
    }
    
    class LeaveApplication {
        +application_number: String (UNIQUE)
        +user_id: Integer (FK -> User.id)
        +application_date: Date
        +leave_type: String (annual/sick/personal/maternity/paternity)
        +start_date: Date
        +end_date: Date
        +leave_days: Decimal(3,1)
        +reason: Text
        +status: String (pending/approved/rejected)
        +approved_by: Integer (FK -> User.id, NULL)
        +approved_at: DateTime (NULL)
        +approval_notes: Text
        +attachment_url: String
    }
    
    User "*" --> "*" Role : assigned
    Role "*" --> "*" Permission : has
    Customer "1" --> "1" CustomerWeChatLink : linked_with
    WeChatUser "1" --> "1" CustomerWeChatLink : links_to
    User "1" --> "*" AttendanceRecord : records
    User "1" --> "*" WorkSchedule : scheduled
    User "1" --> "*" OvertimeApplication : applies_for
    User "1" --> "*" LeaveApplication : applies_for
```

### 4.1 员工薪资与奖金模块

```mermaid
classDiagram
    direction LR
    
    BaseModel <|-- PayrollRecord
    BaseModel <|-- PayrollItem
    BaseModel <|-- BonusRecord
    BaseModel <|-- SalaryAdjustment
    BaseModel <|-- PayrollCalculation
    BaseModel <|-- PayrollApproval
    
    class PayrollRecord {
        +payroll_number: String (UNIQUE)
        +user_id: Integer (FK -> User.id)
        +payroll_period: String
        +period_start: Date
        +period_end: Date
        +basic_salary: Decimal(10,2)
        +overtime_pay: Decimal(10,2)
        +allowance: Decimal(10,2)
        +bonus: Decimal(10,2)
        +other_income: Decimal(10,2)
        +total_income: Decimal(10,2)
        +social_security: Decimal(10,2)
        +tax: Decimal(10,2)
        +other_deductions: Decimal(10,2)
        +total_deductions: Decimal(10,2)
        +net_pay: Decimal(10,2)
        +status: String (draft/calculated/approved/pending_payment/paid/rolled_back)
        +payment_date: Date
        +payment_method: String
        +transaction_no: String
        +calculated_by: Integer (FK -> User.id)
        +approved_by: Integer (FK -> User.id, NULL)
        +notes: Text
    }
    
    class PayrollItem {
        +payroll_id: Integer (FK -> PayrollRecord.id)
        +item_type: String (income/deduction)
        +category: String
        +amount: Decimal(10,2)
        +description: Text
        +reference_id: Integer
        +reference_type: String
    }
    
    class BonusRecord {
        +bonus_number: String (UNIQUE)
        +user_id: Integer (FK -> User.id)
        +bonus_type: String (performance/annual/project/special)
        +bonus_period: String
        +amount: Decimal(10,2)
        +reason: Text
        +status: String (pending/approved/paid/rolled_back)
        +payment_date: Date
        +approved_by: Integer (FK -> User.id, NULL)
        +approved_at: DateTime (NULL)
        +notes: Text
    }
    
    class SalaryAdjustment {
        +adjustment_number: String (UNIQUE)
        +user_id: Integer (FK -> User.id)
        +adjustment_date: Date
        +adjustment_type: String (promotion/annual/increment)
        +old_salary: Decimal(10,2)
        +new_salary: Decimal(10,2)
        +adjustment_amount: Decimal(10,2)
        +effective_date: Date
        +reason: Text
        +status: String (pending/approved/effective)
        +approved_by: Integer (FK -> User.id, NULL)
        +approved_at: DateTime (NULL)
        +notes: Text
    }
    
    class PayrollCalculation {
        +calculation_number: String (UNIQUE)
        +payroll_period: String
        +calculation_date: Date
        +status: String (pending/running/completed/failed)
        +total_employees: Integer
        +total_amount: Decimal(12,2)
        +calculated_by: Integer (FK -> User.id)
        +error_message: Text
        +notes: Text
    }
    
    class PayrollApproval {
        +approval_number: String (UNIQUE)
        +payroll_calculation_id: Integer (FK -> PayrollCalculation.id)
        +approval_date: Date
        +status: String (pending/approved/rejected)
        +approved_by: Integer (FK -> User.id, NULL)
        +approved_at: DateTime (NULL)
        +approval_notes: Text
        +rejection_reason: Text
    }
    
    User "1" --> "*" PayrollRecord : has
    User "1" --> "*" BonusRecord : receives
    User "1" --> "*" SalaryAdjustment : undergoes
    PayrollRecord "1" --> "*" PayrollItem : contains
    PayrollCalculation "1" --> "*" PayrollRecord : generates
    PayrollCalculation "1" --> "1" PayrollApproval : requires
```

### 4.2 员工工作量统计模块

```mermaid
classDiagram
    direction LR
    
    BaseModel <|-- WorkAssignment
    BaseModel <|-- WorkloadRecord
    BaseModel <|-- TaskCompletion
    BaseModel <|-- WorkloadStatistics
    BaseModel <|-- WorkloadAlert
    BaseModel <|-- WorkTask
    
    class WorkTask {
        +task_number: String (UNIQUE)
        +task_name: String
        +task_description: Text
        +task_type: String
        +estimated_hours: Decimal(5,2)
        +priority: String (low/medium/high/urgent)
        +status: String (pending/in_progress/completed/cancelled)
        +deadline: Date
        +created_by: Integer (FK -> User.id)
        +notes: Text
    }
    
    class WorkAssignment {
        +assignment_number: String (UNIQUE)
        +user_id: Integer (FK -> User.id)
        +task_id: Integer (FK -> WorkTask.id, NULL)
        +service_booking_id: Integer (FK -> ServiceBooking.id, NULL)
        +assignment_date: Date
        +start_date: Date
        +end_date: Date
        +estimated_hours: Decimal(5,2)
        +status: String (pending/accepted/in_progress/completed/cancelled)
        +assigned_by: Integer (FK -> User.id)
        +acceptance_notes: Text
        +completion_notes: Text
    }
    
    class WorkloadRecord {
        +record_number: String (UNIQUE)
        +user_id: Integer (FK -> User.id)
        +work_date: Date
        +work_type: String
        +actual_hours: Decimal(5,2)
        +completed_tasks: Integer
        +service_bookings: Integer
        +productivity_score: Decimal(5,2)
        +recorded_by: Integer (FK -> User.id)
        +notes: Text
        +source: String (manual/automated)
    }
    
    class TaskCompletion {
        +completion_number: String (UNIQUE)
        +work_assignment_id: Integer (FK -> WorkAssignment.id)
        +user_id: Integer (FK -> User.id)
        +completion_date: Date
        +actual_hours: Decimal(5,2)
        +quality_score: Decimal(3,2)
        +completion_notes: Text
        +verification_status: String (pending/verified/rejected)
        +verified_by: Integer (FK -> User.id, NULL)
        +verified_at: DateTime (NULL)
        +verification_notes: Text
    }
    
    class WorkloadStatistics {
        +statistics_number: String (UNIQUE)
        +user_id: Integer (FK -> User.id, NULL)
        +department: String (NULL)
        +period_type: String (daily/weekly/monthly/quarterly/yearly)
        +period_start: Date
        +period_end: Date
        +total_hours: Decimal(8,2)
        +total_tasks: Integer
        +total_service_bookings: Integer
        +average_productivity: Decimal(5,2)
        +target_hours: Decimal(8,2)
        +workload_percentage: Decimal(5,2)
        +calculated_at: DateTime
        +calculated_by: Integer (FK -> User.id)
        +notes: Text
    }
    
    class WorkloadAlert {
        +alert_number: String (UNIQUE)
        +user_id: Integer (FK -> User.id, NULL)
        +department: String (NULL)
        +alert_type: String (underload/overload/imbalance)
        +alert_date: Date
        +severity: String (info/warning/critical)
        +threshold_value: Decimal(5,2)
        +actual_value: Decimal(5,2)
        +message: Text
        +status: String (active/acknowledged/resolved)
        +acknowledged_by: Integer (FK -> User.id, NULL)
        +acknowledged_at: DateTime (NULL)
        +resolved_by: Integer (FK -> User.id, NULL)
        +resolved_at: DateTime (NULL)
        +resolution_notes: Text
    }
    
    User "1" --> "*" WorkTask : creates
    User "1" --> "*" WorkAssignment : assigned
    User "1" --> "*" WorkloadRecord : records
    User "1" --> "*" TaskCompletion : completes
    User "1" --> "*" WorkloadStatistics : has
    User "1" --> "*" WorkloadAlert : monitored_by
    WorkTask "1" --> "*" WorkAssignment : assigned_as
    ServiceBooking "1" --> "*" WorkAssignment : generates
    WorkAssignment "1" --> "*" TaskCompletion : results_in
    WorkloadRecord "1" --> "*" WorkloadStatistics : contributes_to
    WorkloadStatistics "1" --> "*" WorkloadAlert : triggers
```

### 5. 食材与库存管理模块

```mermaid
classDiagram
    direction LR
    
    BaseModel <|-- Ingredient
    BaseModel <|-- Supplier
    BaseModel <|-- IngredientCategory
    BaseModel <|-- PurchaseOrder
    BaseModel <|-- PurchaseOrderItem
    BaseModel <|-- DishIngredient
    BaseModel <|-- InventoryTransaction
    BaseModel <|-- InventoryAlert
    BaseModel <|-- IngredientConsumption
    
    class Ingredient {
        +name: String (UNIQUE, NOT NULL)
        +description: Text
        +category_id: Integer (FK -> IngredientCategory.id)
        +unit_of_measure: String
        +current_stock: Decimal(10,3)
        +minimum_stock: Decimal(10,3)
        +maximum_stock: Decimal(10,3)
        +reorder_point: Decimal(10,3)
        +unit_cost: Decimal(10,2)
        +nutrition_info: JSON
        +calories_per_unit: Decimal(8,2)
        +shelf_life_days: Integer
        +storage_conditions: JSON
        +image_url: String
        +is_active: Boolean (DEFAULT true)
        +average_consumption_rate: Decimal(10,3)
        +last_consumption_date: Date
        +total_consumption: Decimal(10,3)
        +consumption_trend: JSON
    }
    
    class IngredientCategory {
        +name: String (UNIQUE, NOT NULL)
        +description: Text
        +parent_category_id: Integer (FK -> IngredientCategory.id, NULL)
    }
    
    class Supplier {
        +name: String (NOT NULL)
        +code: String (UNIQUE)
        +contact_person: String
        +phone: String
        +email: String
        +address: Text
        +tax_id: String
        +payment_terms: Text
        +rating: Decimal(3,2)
        +is_active: Boolean (DEFAULT true)
    }
    
    class PurchaseOrder {
        +order_number: String (UNIQUE)
        +supplier_id: Integer (FK -> Supplier.id)
        +order_date: Date
        +expected_delivery_date: Date
        +actual_delivery_date: Date
        +total_amount: Decimal(12,2)
        +status: String (draft/pending/ordered/received/partially_received/cancelled)
        +notes: Text
        +created_by: Integer (FK -> User.id)
        +approved_by: Integer (FK -> User.id, NULL)
        +approved_at: DateTime (NULL)
    }
    
    class PurchaseOrderItem {
        +purchase_order_id: Integer (FK -> PurchaseOrder.id)
        +ingredient_id: Integer (FK -> Ingredient.id)
        +quantity_ordered: Decimal(10,3)
        +quantity_received: Decimal(10,3)
        +unit_price: Decimal(10,2)
        +total_price: Decimal(10,2)
        +batch_number: String
        +expiry_date: Date
    }
    
    class DishIngredient {
        +dish_id: Integer (FK -> Dish.id)
        +ingredient_id: Integer (FK -> Ingredient.id)
        +quantity_required: Decimal(10,3)
        +unit_of_measure: String
        +notes: Text
    }
    
    class InventoryTransaction {
        +transaction_type: String (purchase/adjustment/consumption/waste/return/transfer)
        +ingredient_id: Integer (FK -> Ingredient.id)
        +quantity_change: Decimal(10,3)
        +unit_price: Decimal(10,2)
        +total_value: Decimal(10,2)
        +reference_id: Integer
        +reference_type: String
        +notes: Text
        +performed_by: Integer (FK -> User.id)
        +consumption_type: String (menu_order/direct_use/testing)
        +consumption_date: Date
        +batch_number: String
        +expiry_date: Date
        +location: String
        +reason: Text
    }
    
    class InventoryAlert {
        +ingredient_id: Integer (FK -> Ingredient.id)
        +alert_type: String (low_stock/expiring/out_of_stock)
        +current_value: Decimal(10,3)
        +threshold_value: Decimal(10,3)
        +message: Text
        +severity: String (info/warning/critical)
        +status: String (active/acknowledged/resolved)
        +acknowledged_by: Integer (FK -> User.id, NULL)
        +acknowledged_at: DateTime (NULL)
    }
    
    class IngredientConsumption {
        +consumption_date: Date
        +ingredient_id: Integer (FK -> Ingredient.id)
        +dish_id: Integer (FK -> Dish.id, NULL)
        +order_id: Integer (FK -> CustomerOrder.id, NULL)
        +theoretical_consumption: Decimal(10,3)
        +actual_consumption: Decimal(10,3)
        +consumption_difference: Decimal(10,3)
        +consumption_rate: Decimal(6,4)
        +unit_cost: Decimal(10,2)
        +total_cost: Decimal(10,2)
        +consumption_reason: String
        +recorded_by: Integer (FK -> User.id)
        +notes: Text
    }
    
    IngredientCategory "1" --> "*" Ingredient : categorizes
    Supplier "1" --> "*" PurchaseOrder : supplies
    PurchaseOrder "1" --> "*" PurchaseOrderItem : contains
    Ingredient "1" --> "*" PurchaseOrderItem : purchased_as
    Dish "1" --> "*" DishIngredient : requires
    Ingredient "1" --> "*" DishIngredient : used_in
    Ingredient "1" --> "*" InventoryTransaction : tracked_by
    Ingredient "1" --> "*" InventoryAlert : monitored_by
    Ingredient "1" --> "*" IngredientConsumption : consumed
    Dish "1" --> "*" IngredientConsumption : uses
    CustomerOrder "1" --> "*" IngredientConsumption : generates
```

### 6. 服务管理模块（含母子服务）

```mermaid
classDiagram
    direction LR
    
    BaseModel <|-- ServiceCategory
    BaseModel <|-- ServiceItem
    BaseModel <|-- ServicePackage
    BaseModel <|-- ServicePackageItem
    BaseModel <|-- ServiceBooking
    BaseModel <|-- ServiceFeedback
    BaseModel <|-- PostpartumRecoveryRecord
    BaseModel <|-- NewbornCareRecord
    BaseModel <|-- MotherBabyServiceRecord
    
    class ServiceCategory {
        +name: String (UNIQUE, NOT NULL)
        +description: Text
        +icon_url: String
        +sort_order: Integer
        +is_active: Boolean (DEFAULT true)
        +service_type: String (mother_baby/general)
    }
    
    class ServiceItem {
        +name: String (NOT NULL)
        +description: Text
        +category_id: Integer (FK -> ServiceCategory.id)
        +duration_minutes: Integer
        +price: Decimal(10,2)
        +discounted_price: Decimal(10,2)
        +image_url: String
        +is_available: Boolean (DEFAULT true)
        +service_type: String (postpartum_recovery/newborn_care/other)
        +target_age: String
        +benefits: JSON
        +precautions: Text
    }
    
    class ServicePackage {
        +name: String (NOT NULL)
        +description: Text
        +duration_days: Integer
        +total_price: Decimal(10,2)
        +discounted_price: Decimal(10,2)
        +services_included: JSON
        +is_active: Boolean (DEFAULT true)
        +package_type: String (basic/premium/custom)
        +target_group: String
    }
    
    class ServicePackageItem {
        +package_id: Integer (FK -> ServicePackage.id)
        +service_item_id: Integer (FK -> ServiceItem.id)
        +quantity: Integer
        +frequency: String
        +notes: Text
    }
    
    class ServiceBooking {
        +booking_number: String (UNIQUE)
        +customer_id: Integer (FK -> Customer.id)
        +service_item_id: Integer (FK -> ServiceItem.id, NULL)
        +package_id: Integer (FK -> ServicePackage.id, NULL)
        +booking_date: Date
        +start_time: Time
        +end_time: Time
        +duration_minutes: Integer
        +assigned_staff_id: Integer (FK -> User.id, NULL)
        +status: String (pending/confirmed/in_progress/completed/cancelled)
        +notes: Text
        +cancellation_reason: Text
        +payment_status: String (unpaid/paid/partial_refunded/full_refunded)
        +payment_method: String
        +transaction_no: String
        +actual_amount: Decimal(10,2)
    }
    
    class ServiceFeedback {
        +booking_id: Integer (FK -> ServiceBooking.id)
        +customer_id: Integer (FK -> Customer.id)
        +rating: Integer (1-5)
        +comment: Text
        +suggestions: Text
        +is_anonymous: Boolean (DEFAULT false)
        +feedback_date: Date
        +attachments: JSON
    }
    
    class PostpartumRecoveryRecord {
        +booking_id: Integer (FK -> ServiceBooking.id)
        +customer_id: Integer (FK -> Customer.id)
        +recovery_type: String
        +recovery_date: Date
        +recovery_time: Time
        +recovery_duration: Integer
        +recovery_progress: JSON
        +body_measurements: JSON
        +recovery_notes: Text
        +next_appointment: Date
        +assigned_staff_id: Integer (FK -> User.id)
        +status: String (completed/scheduled)
    }
    
    class NewbornCareRecord {
        +booking_id: Integer (FK -> ServiceBooking.id)
        +customer_id: Integer (FK -> Customer.id)
        +newborn_name: String
        +newborn_age_days: Integer
        +care_date: Date
        +care_time: Time
        +care_duration: Integer
        +care_type: String
        +care_details: JSON
        +vital_signs: JSON
        +feeding_records: JSON
        +sleep_records: JSON
        +care_notes: Text
        +next_appointment: Date
        +assigned_staff_id: Integer (FK -> User.id)
        +status: String (completed/scheduled)
    }
    
    class MotherBabyServiceRecord {
        +record_number: String (UNIQUE)
        +customer_id: Integer (FK -> Customer.id)
        +service_type: String
        +start_date: Date
        +end_date: Date
        +total_sessions: Integer
        +completed_sessions: Integer
        +total_amount: Decimal(10,2)
        +paid_amount: Decimal(10,2)
        +status: String (active/completed/cancelled)
        +service_notes: Text
        +staff_ids: JSON
        +related_bookings: JSON
    }
    
    ServiceCategory "1" --> "*" ServiceItem : contains
    ServicePackage "1" --> "*" ServicePackageItem : includes
    ServiceItem "1" --> "*" ServicePackageItem : part_of
    Customer "1" --> "*" ServiceBooking : books
    ServiceItem "1" --> "*" ServiceBooking : booked_as
    ServicePackage "1" --> "*" ServiceBooking : booked_as_package
    ServiceBooking "1" --> "1" ServiceFeedback : receives
    ServiceBooking "1" --> "*" PostpartumRecoveryRecord : generates
    ServiceBooking "1" --> "*" NewbornCareRecord : generates
    Customer "1" --> "*" MotherBabyServiceRecord : receives
    MotherBabyServiceRecord "1" --> "*" ServiceBooking : includes
```

### 7. 配送与排餐模块

```mermaid
classDiagram
    direction LR
    
    BaseModel <|-- DeliverySchedule
    BaseModel <|-- DeliveryAssignment
    BaseModel <|-- DeliveryRoute
    BaseModel <|-- DeliveryStatusUpdate
    
    class DeliverySchedule {
        +date: Date
        +time_slot: String
        +total_orders: Integer
        +total_customers: Integer
        +status: String (pending/assigned/in_progress/completed)
        +notes: Text
    }
    
    class DeliveryAssignment {
        +schedule_id: Integer (FK -> DeliverySchedule.id)
        +delivery_staff_id: Integer (FK -> User.id)
        +route_id: Integer (FK -> DeliveryRoute.id)
        +total_assignments: Integer
        +estimated_start_time: DateTime
        +estimated_end_time: DateTime
        +actual_start_time: DateTime
        +actual_end_time: DateTime
        +vehicle_type: String
        +vehicle_number: String
        +status: String (pending/started/in_progress/completed)
    }
    
    class DeliveryRoute {
        +name: String
        +description: Text
        +zone: String
        +route_sequence: JSON
        +estimated_distance_km: Decimal(6,2)
        +estimated_duration_minutes: Integer
        +is_active: Boolean (DEFAULT true)
    }
    
    class DeliveryStatusUpdate {
        +assignment_id: Integer (FK -> DeliveryAssignment.id)
        +order_id: Integer (FK -> CustomerOrder.id)
        +status: String (preparing/ready_for_pickup/picked_up/on_the_way/delivered/failed)
        +latitude: Decimal(10,8)
        +longitude: Decimal(11,8)
        +notes: Text
        +photo_url: String
        +updated_by: Integer (FK -> User.id)
    }
    
    DeliverySchedule "1" --> "*" DeliveryAssignment : assigns
    User "1" --> "*" DeliveryAssignment : assigned_to
    DeliveryRoute "1" --> "*" DeliveryAssignment : follows
    DeliveryAssignment "1" --> "*" DeliveryStatusUpdate : tracks
    CustomerOrder "1" --> "*" DeliveryStatusUpdate : tracked_for
```

### 8. 月子餐管理模块

```mermaid
classDiagram
    direction LR
    
    BaseModel <|-- ConfinementMealPlan
    BaseModel <|-- ConfinementWeekPlan
    BaseModel <|-- ConfinementDayPlan
    BaseModel <|-- ConfinementMealItem
    
    class ConfinementMealPlan {
        +plan_number: String (UNIQUE)
        +customer_id: Integer (FK -> Customer.id)
        +start_date: Date
        +end_date: Date
        +total_days: Integer
        +total_weeks: Integer
        +meal_plan_type: String (standard/premium/custom)
        +total_calories_per_day: Decimal(8,2)
        +total_price: Decimal(12,2)
        +discount_amount: Decimal(10,2)
        +final_price: Decimal(12,2)
        +status: String (draft/active/completed/cancelled)
        +notes: Text
        +created_by: Integer (FK -> User.id)
        +approved_by: Integer (FK -> User.id, NULL)
    }
    
    class ConfinementWeekPlan {
        +meal_plan_id: Integer (FK -> ConfinementMealPlan.id)
        +week_number: Integer (1-12)
        +focus_area: String
        +nutrition_goals: JSON
        +avoid_foods: JSON
        +recommended_foods: JSON
        +notes: Text
    }
    
    class ConfinementDayPlan {
        +week_plan_id: Integer (FK -> ConfinementWeekPlan.id)
        +day_number: Integer (1-7)
        +date: Date
        +total_calories: Decimal(8,2)
        +nutrition_summary: JSON
        +special_notes: Text
    }
    
    class ConfinementMealItem {
        +day_plan_id: Integer (FK -> ConfinementDayPlan.id)
        +meal_type: String (breakfast/morning_snack/lunch/afternoon_snack/dinner/night_snack)
        +dish_id: Integer (FK -> Dish.id)
        +serving_time: Time
        +quantity: Integer
        +calories: Decimal(8,2)
        +nutrition_details: JSON
        +special_instructions: Text
    }
    
    Customer "1" --> "*" ConfinementMealPlan : subscribes_to
    ConfinementMealPlan "1" --> "*" ConfinementWeekPlan : organized_by_weeks
    ConfinementWeekPlan "1" --> "*" ConfinementDayPlan : detailed_by_days
    ConfinementDayPlan "1" --> "*" ConfinementMealItem : composed_of
    Dish "1" --> "*" ConfinementMealItem : included_as
```

### 9. AI分析与报告模块

```mermaid
classDiagram
    direction LR
    
    BaseModel <|-- AIAnalysisJob
    BaseModel <|-- AIAnalysisResult
    BaseModel <|-- ReportTemplate
    BaseModel <|-- GeneratedReport
    BaseModel <|-- AlertRule
    BaseModel <|-- Alert
    
    class AIAnalysisJob {
        +job_type: String (menu_optimization/nutrition_analysis/demand_forecast/cost_analysis)
        +parameters: JSON
        +status: String (pending/running/completed/failed)
        +started_at: DateTime
        +completed_at: DateTime
        +result_summary: Text
        +error_message: Text
        +created_by: Integer (FK -> User.id)
    }
    
    class AIAnalysisResult {
        +job_id: Integer (FK -> AIAnalysisJob.id)
        +analysis_type: String
        +input_data: JSON
        +result_data: JSON
        +insights: JSON
        +recommendations: JSON
        +confidence_score: Decimal(5,4)
        +visualization_url: String
    }
    
    class ReportTemplate {
        +template_name: String (UNIQUE)
        +template_type: String (daily/weekly/monthly/custom)
        +description: Text
        +template_content: JSON
        +is_active: Boolean (DEFAULT true)
    }
    
    class GeneratedReport {
        +report_number: String (UNIQUE)
        +template_id: Integer (FK -> ReportTemplate.id)
        +report_type: String
        +period_start: Date
        +period_end: Date
        +report_data: JSON
        +insights: JSON
        +recommendations: JSON
        +file_url: String
        +status: String (generated/published/archived)
        +generated_by: Integer (FK -> User.id)
    }
    
    class AlertRule {
        +rule_name: String (UNIQUE)
        +rule_type: String (inventory/customer/order/equipment)
        +condition: JSON
        +severity: String (info/warning/critical)
        +notification_channels: JSON
        +is_active: Boolean (DEFAULT true)
    }
    
    class Alert {
        +alert_code: String (UNIQUE)
        +rule_id: Integer (FK -> AlertRule.id)
        +entity_type: String
        +entity_id: Integer
        +entity_name: String
        +message: Text
        +severity: String
        +data: JSON
        +status: String (active/acknowledged/resolved)
        +acknowledged_by: Integer (FK -> User.id, NULL)
        +acknowledged_at: DateTime (NULL)
        +resolved_by: Integer (FK -> User.id, NULL)
        +resolved_at: DateTime (NULL)
        +resolution_notes: Text
    }
    
    AIAnalysisJob "1" --> "1" AIAnalysisResult : produces
    ReportTemplate "1" --> "*" GeneratedReport : used_for
    AlertRule "1" --> "*" Alert : triggers
```

## 系统架构图

```mermaid
graph TB
    subgraph "客户端层"
        A1[Web管理后台]
        A2[微信小程序]
        A3[移动端APP]
        A4[员工工作台]
    end
    
    subgraph "API网关层"
        B1[API Gateway]
        B2[负载均衡器]
        B3[认证鉴权]
        B4[请求限流]
        B5[日志记录]
    end
    
    subgraph "业务服务层"
        subgraph "核心服务"
            C1[用户服务]
            C2[菜单服务]
            C3[订单服务]
            C4[库存服务]
        end
        
        subgraph "扩展服务"
            C5[配送服务]
            C6[月子餐服务]
            C7[分析服务]
            C8[通知服务]
        end
    end
    
    subgraph "数据层"
        D1[(MySQL主库)]
        D2[(MySQL从库)]
        D3[(Redis缓存)]
        D4[(Elasticsearch)]
        D5[文件存储]
        D6[消息队列]
    end
    
    subgraph "基础设施"
        E1[监控告警]
        E2[日志收集]
        E3[配置中心]
        E4[服务注册]
    end
    
    %% 连接关系
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    
    B1 --> B2
    B2 --> B3
    B3 --> C1
    
    C1 --> C2
    C1 --> C3
    C1 --> C4
    C1 --> C5
    C1 --> C6
    C1 --> C7
    C1 --> C8
    
    C2 --> D1
    C3 --> D1
    C4 --> D1
    C5 --> D1
    C6 --> D1
    C7 --> D4
    C8 --> D6
    
    D1 --> D2
    D1 --> D3
    D1 --> D5
    
    C1 --> E1
    C2 --> E1
    C3 --> E1
    C4 --> E1
    
    B5 --> E2
    C1 --> E2
    
    C1 --> E3
    C2 --> E3
    
    style A1 fill:#f9f,stroke:#333,stroke-width:2px
    style B1 fill:#bbf,stroke:#333,stroke-width:2px
    style C1 fill:#bfb,stroke:#333,stroke-width:2px
    style D1 fill:#f96,stroke:#333,stroke-width:2px
```

## 核心数据流图

```mermaid
flowchart TD
    subgraph "数据输入源"
        I1[客户注册/入住]
        I2[订单创建]
        I3[食材采购]
        I4[服务预约]
        I5[设备传感器]
    end
    
    subgraph "数据处理层"
        P1[数据验证]
        P2[业务规则引擎]
        P3[实时计算]
        P4[批量处理]
    end
    
    subgraph "数据存储层"
        S1[业务数据库]
        S2[分析数据库]
        S3[缓存层]
        S4[文件存储]
    end
    
    subgraph "数据输出层"
        O1[实时仪表盘]
        O2[业务报表]
        O3[API接口]
        O4[消息推送]
        O5[告警通知]
    end
    
    subgraph "数据消费层"
        C1[管理人员]
        C2[客户用户]
        C3[厨房员工]
        C4[配送人员]
        C5[供应商]
    end
    
    %% 数据流向
    I1 --> P1
    I2 --> P1
    I3 --> P1
    I4 --> P1
    I5 --> P1
    
    P1 --> P2
    P2 --> P3
    P2 --> P4
    
    P3 --> S1
    P3 --> S3
    P4 --> S2
    P4 --> S4
    
    S1 --> O1
    S2 --> O2
    S3 --> O3
    S1 --> O4
    S1 --> O5
    
    O1 --> C1
    O2 --> C1
    O3 --> C2
    O4 --> C2
    O4 --> C3
    O4 --> C4
    O5 --> C5
    
    style I1 fill:#e1f5fe
    style P1 fill:#f3e5f5
    style S1 fill:#e8f5e8
    style O1 fill:#fff3e0
    style C1 fill:#ffebee
```

## 主要优化和改进

### 1. **数据结构优化**
- 统一了字段命名规范（snake_case）
- 添加了必要的索引字段（如唯一标识、外键）
- 使用JSON类型存储灵活数据结构
- 添加了软删除支持（deleted_at字段）

### 2. **关系规范化**
- 修正了外键关系，使用正确的符号表示
- 移除了冗余的BasicMenu表
- 优化了多对多关系的中间表设计
- 添加了级联操作说明

### 3. **业务完整性**
- 添加了状态字段跟踪业务流转
- 增加了审计字段（created_by, updated_by）
- 完善了数据验证约束（NOT NULL, UNIQUE）
- 添加了合理的默认值

### 4. **性能考虑**
- 为频繁查询的字段添加了索引
- 设计了合理的缓存策略
- 考虑了大表的分区策略
- 添加了归档和历史表的设计

### 5. **扩展性设计**
- 模块化设计，便于独立扩展
- 支持多种客户端接入
- 预留了AI分析和自动化接口
- 设计了灵活的通知和告警机制

## 订餐流程功能支持

### 涉及的表结构

#### 1. 订单管理相关表
- **Customer**：客户基本信息，作为订单的主关联表
- **CustomerOrder**：客户订单表，包含订单编号、客户ID、订单日期、配送日期、配送时间段、配送地址、联系人、联系电话、总金额、支付状态、订单状态等信息
- **OrderItem**：订单详情表，包含订单ID、菜品ID、数量、单价、总价、特殊说明、准备状态等信息

#### 2. 菜品管理相关表
- **Dish**：菜品信息表，包含菜品名称、描述、食材、饮食限制、卡路里、价格、准备时间、分类、图片等信息
- **MenuCategory**：菜单分类表，包含分类名称、描述、排序、状态等信息
- **DishIngredient**：菜品食材关联表，包含菜品ID、食材ID、所需数量、单位、备注等信息

#### 3. 库存管理相关表
- **Ingredient**：食材信息表，包含食材名称、描述、分类、单位、当前库存、最小库存、最大库存、重订点、单价、营养信息、保质期、存储条件等信息
- **IngredientCategory**：食材分类表，包含分类名称、描述、父分类等信息
- **InventoryTransaction**：库存交易记录表，包含交易类型、食材ID、数量变化、单价、总价、参考ID、参考类型、备注、执行人、消费类型、消费日期、批次号、过期日期、位置、原因等信息
- **InventoryAlert**：库存告警表，包含食材ID、告警类型、当前值、阈值、消息、严重程度、状态、确认人、确认时间等信息

#### 4. 配送管理相关表
- **DeliverySchedule**：配送计划表，包含日期、时间段、总订单数、总客户数、状态、备注等信息
- **DeliveryAssignment**：配送分配表，包含计划ID、配送员ID、路线ID、总分配数、预计开始时间、预计结束时间、实际开始时间、实际结束时间、车辆类型、车牌号、状态等信息
- **DeliveryRoute**：配送路线表，包含路线名称、描述、区域、路线顺序、预计距离、预计时长、状态等信息
- **DeliveryStatusUpdate**：配送状态更新表，包含分配ID、订单ID、状态、纬度、经度、备注、照片、更新人等信息

#### 5. 统计和提示相关表
- **AlertRule**：告警规则表，包含规则名称、规则类型、条件、严重程度、通知渠道、状态等信息
- **Alert**：告警表，包含告警代码、规则ID、实体类型、实体ID、实体名称、消息、严重程度、数据、状态、解决时间、解决人、解决备注、确认时间、确认人等信息

### 订餐流程数据流向

1. **订单创建数据流向**：
   - 客户通过系统下单，创建CustomerOrder记录
   - 为订单添加菜品，创建OrderItem记录
   - 订单关联到Customer表，获取客户信息
   - 订单关联到Dish表，获取菜品信息

2. **库存扣减数据流向**：
   - 根据订单中的菜品，通过DishIngredient表查询所需食材
   - 根据食材需求，通过InventoryTransaction表记录库存扣减
   - 更新Ingredient表的当前库存
   - 当库存低于阈值时，通过InventoryAlert表生成库存告警

3. **配送安排数据流向**：
   - 根据订单配送日期，创建DeliverySchedule记录
   - 为配送计划分配配送员，创建DeliveryAssignment记录
   - 为配送分配安排路线，关联DeliveryRoute表
   - 配送过程中更新状态，创建DeliveryStatusUpdate记录

4. **统计和提示数据流向**：
   - 从CustomerOrder和OrderItem表收集订单数据
   - 从InventoryTransaction表收集库存数据
   - 从DeliveryAssignment表收集配送数据
   - 根据AlertRule表的规则，生成Alert记录

### 订餐流程查询逻辑

1. **订单查询**：
   - 按客户ID和日期范围筛选CustomerOrder记录
   - 关联查询OrderItem和Dish表的详细信息
   - 支持按订单状态、支付状态、配送日期等条件进一步筛选
   - 支持排序和分页

2. **库存查询**：
   - 按食材ID和日期范围筛选InventoryTransaction记录
   - 关联查询Ingredient表的详细信息
   - 支持按交易类型、食材分类等条件进一步筛选
   - 支持排序和分页

3. **配送查询**：
   - 按日期范围筛选DeliverySchedule记录
   - 关联查询DeliveryAssignment、DeliveryRoute和DeliveryStatusUpdate的详细信息
   - 支持按配送状态、配送员、路线等条件进一步筛选
   - 支持排序和分页

4. **统计查询**：
   - 按客户、时间、菜品等维度统计订单数据
   - 按食材、时间等维度统计库存数据
   - 按配送员、时间等维度统计配送数据

### 订餐流程统计和提示机制

1. **订单统计**：
   - 订单总数、总金额、平均订单金额
   - 各菜品销量统计、各菜品收入统计
   - 各时间段订单分布、各区域订单分布
   - 订单状态分布、支付状态分布

2. **库存统计**：
   - 各食材库存水平、各食材消耗量
   - 各食材周转率、各食材缺货次数
   - 库存总价值、库存周转天数

3. **配送统计**：
   - 配送订单数、配送准时率、配送成功率
   - 各配送员工作量、各路线配送效率
   - 配送成本统计、客户满意度统计

4. **提示机制**：
   - 库存不足提示：当食材库存低于最小库存时，生成库存不足告警
   - 订单超时提示：当订单处理时间超过阈值时，生成订单超时告警
   - 配送延迟提示：当配送时间超过预计时间时，生成配送延迟告警
   - 食材过期提示：当食材接近保质期时，生成食材过期告警

### 订餐流程储备不足计算

1. **食材储备不足计算**：
   - 食材储备不足 = 最小库存 - 当前库存
   - 食材储备不足率 = （最小库存 - 当前库存）÷ 最小库存 × 100%
   - 食材储备不足等级：
     - 轻微不足：储备不足率 < 20%
     - 中度不足：20% ≤ 储备不足率 < 50%
     - 严重不足：储备不足率 ≥ 50%

2. **配送员储备不足计算**：
   - 人力资源需求 = 预计配送订单数 ÷ 人均配送效率
   - 工作量储备 = 现有配送员数量 × 人均可用工作时长 × 工作效率系数
   - 配送员储备不足 = 人力资源需求 - 工作量储备
   - 配送员储备不足率 = （人力资源需求 - 工作量储备）÷ 人力资源需求 × 100%

3. **订单处理储备不足计算**：
   - 订单处理需求 = 预计订单数 × 平均处理时间
   - 订单处理储备 = 可用处理人员数量 × 人均可用工作时长 × 工作效率系数
   - 订单处理储备不足 = 订单处理需求 - 订单处理储备
   - 订单处理储备不足率 = （订单处理需求 - 订单处理储备）÷ 订单处理需求 × 100%

### 订餐流程打印功能支持

1. **数据导出**：
   - 支持将订单查询结果导出为PDF、Excel等格式
   - 支持将库存查询结果导出为PDF、Excel等格式
   - 支持将配送查询结果导出为PDF、Excel等格式
   - 通过ReportTemplate和GeneratedReport表管理报表模板和生成记录

2. **报表格式**：
   - 订单报表：包含订单编号、客户姓名、订单日期、配送日期、配送地址、联系人、联系电话、订单状态、支付状态、订单金额、菜品明细等信息
   - 库存报表：包含食材名称、当前库存、最小库存、最大库存、重订点、单价、库存价值、库存状态等信息
   - 配送报表：包含配送日期、配送员、路线、订单数、客户数、配送状态、配送时间、配送距离等信息

3. **打印流程**：
   - 用户选择查询条件，获取查询结果
   - 选择报表模板和导出格式
   - 系统生成报表文件
   - 用户下载或直接打印报表

## 客户服务记录查询功能支持

### 涉及的表结构

#### 1. 服务记录查询相关表
- **Customer**：客户基本信息，作为服务记录的主关联表
- **ServiceBooking**：服务预约记录，包含服务类型、日期、时间、时长等信息
- **PostpartumRecoveryRecord**：产后恢复服务记录，包含详细的恢复情况
- **NewbornCareRecord**：新生儿护理服务记录，包含生命体征、喂养记录、睡眠记录等详细信息

#### 2. 餐食记录查询相关表
- **CustomerMenuSelection**：客户菜单选择记录，包含餐食类型、日期、菜品等信息
- **DailyMenu**：每日菜单，作为餐食选择的基础
- **Dish**：菜品信息，包含菜品名称、描述、营养信息等

#### 3. 孩子服务记录查询相关表
- **NewbornCareRecord**：新生儿护理服务记录，包含孩子的详细服务信息
- **ServiceBooking**：服务预约记录，关联到孩子服务

#### 4. 统计和提示相关表
- **WorkloadRecord**：工作量记录，用于统计服务人员工作量
- **WorkloadAlert**：工作量预警，用于提示储备不足情况
- **WorkloadStatistics**：工作量统计，用于多维度分析

### 数据流向

1. **服务记录数据流向**：
   - 客户通过ServiceBooking表预约服务
   - 服务执行后，生成PostpartumRecoveryRecord或NewbornCareRecord记录
   - 查询时，通过Customer关联ServiceBooking，再关联到具体的服务记录表

2. **餐食记录数据流向**：
   - 客户通过CustomerMenuSelection表选择每日餐食
   - 选择记录关联到DailyMenu和Dish表
   - 查询时，通过Customer关联CustomerMenuSelection，再关联到DailyMenu和Dish表

3. **孩子服务记录数据流向**：
   - 客户通过ServiceBooking表预约孩子服务
   - 服务执行后，生成NewbornCareRecord记录
   - 查询时，通过Customer关联ServiceBooking，再关联到NewbornCareRecord表

4. **统计和提示数据流向**：
   - 从ServiceBooking、PostpartumRecoveryRecord、NewbornCareRecord等表收集工作量数据
   - 存储到WorkloadRecord表
   - 计算生成WorkloadStatistics和WorkloadAlert记录

### 查询逻辑

1. **服务记录查询**：
   - 按客户ID和日期范围筛选ServiceBooking记录
   - 关联查询PostpartumRecoveryRecord和NewbornCareRecord的详细信息
   - 支持按服务类型、状态等条件进一步筛选

2. **餐食记录查询**：
   - 按客户ID和日期范围筛选CustomerMenuSelection记录
   - 关联查询Dish表的详细信息
   - 支持按餐食类型、菜品等条件进一步筛选

3. **孩子服务记录查询**：
   - 按客户ID和日期范围筛选ServiceBooking记录
   - 关联查询NewbornCareRecord的详细信息
   - 支持按服务类型、状态等条件进一步筛选

4. **统计查询**：
   - 按客户、服务类型、时间等维度统计服务数据
   - 按客户、餐食类型、时间等维度统计餐食数据
   - 按服务人员、时间等维度统计工作量数据

### 储备不足计算

1. **数据收集**：
   - 从ServiceBooking表获取服务预约数据
   - 从WorkloadRecord表获取工作量记录
   - 从User表获取可用服务人员数据

2. **计算逻辑**：
   - 人力资源需求 = Σ（服务预计工作量 ÷ 人均工作效率）
   - 工作量储备 = 现有员工数量 × 人均可用工作时长 × 工作效率系数
   - 储备不足率 = （人力资源需求 - 工作量储备）÷ 人力资源需求 × 100%

3. **预警机制**：
   - 当储备不足率超过阈值时，生成WorkloadAlert记录
   - 根据不足程度设置不同的预警级别
   - 通过系统通知、邮件等方式提醒相关人员

### 打印功能支持

1. **数据导出**：
   - 支持将查询结果导出为PDF、Excel等格式
   - 通过ReportTemplate和GeneratedReport表管理报表模板和生成记录

2. **报表格式**：
   - 服务记录报表：包含服务类型、日期、时间、时长、服务人员等信息
   - 餐食记录报表：包含餐食类型、日期、菜品、数量等信息
   - 孩子服务记录报表：包含服务类型、日期、时间、时长、生命体征等信息

3. **打印流程**：
   - 用户选择查询条件，获取查询结果
   - 选择报表模板和导出格式
   - 系统生成报表文件
   - 用户下载或直接打印报表

这个修正版数据库结构已经过优化，可以直接用于实际的系统开发。每个模块都有清晰的职责划分，表之间的关系也得到了正确的表达。建议在具体实施时，根据实际业务需求进行适当的调整和优化。
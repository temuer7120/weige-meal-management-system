<template>
  <div class="ingredient-management">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <h2>食材管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="handleAddIngredient">添加食材</el-button>
        <el-button @click="handleImport">导入</el-button>
        <el-button @click="handleExport">导出</el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="食材名称">
          <el-input v-model="searchForm.name" placeholder="请输入食材名称" style="width: 200px"></el-input>
        </el-form-item>
        
        <el-form-item label="类别">
          <el-select v-model="searchForm.category" placeholder="请选择类别" style="width: 150px">
            <el-option label="蔬菜" value="蔬菜"></el-option>
            <el-option label="肉类" value="肉类"></el-option>
            <el-option label="海鲜" value="海鲜"></el-option>
            <el-option label="调料" value="调料"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="库存状态">
          <el-select v-model="searchForm.stockStatus" placeholder="请选择库存状态" style="width: 150px">
            <el-option label="正常" value="normal"></el-option>
            <el-option label="缺货" value="low"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 食材列表 -->
    <el-card class="list-card">
      <template #header>
        <div class="list-header">
          <span>食材列表</span>
          <span class="total-count">共 {{ ingredients.length }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="ingredients" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="食材名称"></el-table-column>
        <el-table-column prop="category" label="类别" width="100"></el-table-column>
        <el-table-column prop="unit" label="单位" width="80"></el-table-column>
        <el-table-column prop="current_stock" label="当前库存"></el-table-column>
        <el-table-column prop="minimum_stock" label="最低库存" width="100"></el-table-column>
        <el-table-column prop="price" label="单价" width="100">
          <template #default="scope">
            ¥{{ scope.row.price }}
          </template>
        </el-table-column>
        <el-table-column prop="supplier_name" label="供应商" width="150"></el-table-column>
        <el-table-column prop="expiry_date" label="保质期" width="120"></el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEditIngredient(scope.row)">编辑</el-button>
            <el-button type="success" size="small" @click="handleStockIn(scope.row)">入库</el-button>
            <el-button type="warning" size="small" @click="handleStockOut(scope.row)">出库</el-button>
            <el-button type="danger" size="small" @click="handleDeleteIngredient(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        />
      </div>
    </el-card>
    
    <!-- 添加/编辑食材对话框 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="食材名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入食材名称"></el-input>
        </el-form-item>
        
        <el-form-item label="类别" prop="category">
          <el-select v-model="formData.category" placeholder="请选择类别">
            <el-option label="蔬菜" value="蔬菜"></el-option>
            <el-option label="肉类" value="肉类"></el-option>
            <el-option label="海鲜" value="海鲜"></el-option>
            <el-option label="调料" value="调料"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="单位" prop="unit">
          <el-input v-model="formData.unit" placeholder="请输入单位"></el-input>
        </el-form-item>
        
        <el-form-item label="当前库存" prop="current_stock">
          <el-input v-model.number="formData.current_stock" placeholder="请输入当前库存" type="number"></el-input>
        </el-form-item>
        
        <el-form-item label="最低库存" prop="minimum_stock">
          <el-input v-model.number="formData.minimum_stock" placeholder="请输入最低库存" type="number"></el-input>
        </el-form-item>
        
        <el-form-item label="单价" prop="price">
          <el-input v-model.number="formData.price" placeholder="请输入单价" type="number"></el-input>
        </el-form-item>
        
        <el-form-item label="供应商" prop="supplier_id">
          <el-select v-model="formData.supplier_id" placeholder="请选择供应商">
            <el-option v-for="supplier in suppliers" :key="supplier.id" :label="supplier.name" :value="supplier.id"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="保质期">
          <el-date-picker v-model="formData.expiry_date" type="date" placeholder="请选择保质期" style="width: 100%"></el-date-picker>
        </el-form-item>
        
        <el-form-item label="营养成分">
          <el-input v-model="formData.nutrition_info" type="textarea" placeholder="请输入营养成分"></el-input>
        </el-form-item>
        
        <el-form-item label="热量">
          <el-input v-model.number="formData.calories" placeholder="请输入热量" type="number"></el-input>
        </el-form-item>
        
        <el-form-item label="禁忌">
          <el-input v-model="formData.restrictions" type="textarea" placeholder="请输入禁忌"></el-input>
        </el-form-item>
        
        <el-form-item label="购买人">
          <el-input v-model="formData.purchaser" placeholder="请输入购买人"></el-input>
        </el-form-item>
        
        <el-form-item label="食材溯源">
          <el-input v-model="formData.origin" type="textarea" placeholder="请输入食材溯源"></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 入库对话框 -->
    <el-dialog
      title="食材入库"
      :visible.sync="stockInDialogVisible"
      width="400px"
    >
      <el-form :model="stockInForm" :rules="stockInRules" ref="stockInFormRef" label-width="80px">
        <el-form-item label="食材名称">
          <el-input v-model="stockInForm.name" disabled></el-input>
        </el-form-item>
        
        <el-form-item label="当前库存">
          <el-input v-model="stockInForm.current_stock" disabled></el-input>
        </el-form-item>
        
        <el-form-item label="入库数量" prop="quantity">
          <el-input v-model.number="stockInForm.quantity" placeholder="请输入入库数量" type="number"></el-input>
        </el-form-item>
        
        <el-form-item label="入库单价" prop="price">
          <el-input v-model.number="stockInForm.price" placeholder="请输入入库单价" type="number"></el-input>
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input v-model="stockInForm.notes" type="textarea" placeholder="请输入备注"></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="stockInDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleStockInSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 出库对话框 -->
    <el-dialog
      title="食材出库"
      :visible.sync="stockOutDialogVisible"
      width="400px"
    >
      <el-form :model="stockOutForm" :rules="stockOutRules" ref="stockOutFormRef" label-width="80px">
        <el-form-item label="食材名称">
          <el-input v-model="stockOutForm.name" disabled></el-input>
        </el-form-item>
        
        <el-form-item label="当前库存">
          <el-input v-model="stockOutForm.current_stock" disabled></el-input>
        </el-form-item>
        
        <el-form-item label="出库数量" prop="quantity">
          <el-input v-model.number="stockOutForm.quantity" placeholder="请输入出库数量" type="number"></el-input>
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input v-model="stockOutForm.notes" type="textarea" placeholder="请输入备注"></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="stockOutDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleStockOutSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'IngredientManagement',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      name: '',
      category: '',
      stockStatus: ''
    })
    
    // 分页信息
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(100)
    
    // 食材数据
    const ingredients = ref([
      { id: 1, name: '西红柿', category: '蔬菜', unit: 'kg', current_stock: 50, minimum_stock: 10, price: 5.5, supplier_name: '绿色蔬菜供应商', expiry_date: '2026-02-20' },
      { id: 2, name: '鸡蛋', category: '其他', unit: '个', current_stock: 200, minimum_stock: 50, price: 0.8, supplier_name: '禽蛋供应商', expiry_date: '2026-02-15' },
      { id: 3, name: '猪肉', category: '肉类', unit: 'kg', current_stock: 15, minimum_stock: 5, price: 35, supplier_name: '肉类供应商', expiry_date: '2026-02-10' },
      { id: 4, name: '大米', category: '其他', unit: 'kg', current_stock: 100, minimum_stock: 20, price: 4.5, supplier_name: '粮油供应商', expiry_date: '2026-12-31' },
      { id: 5, name: '胡萝卜', category: '蔬菜', unit: 'kg', current_stock: 30, minimum_stock: 8, price: 3.5, supplier_name: '绿色蔬菜供应商', expiry_date: '2026-02-25' }
    ])
    
    // 供应商数据
    const suppliers = ref([
      { id: 1, name: '绿色蔬菜供应商' },
      { id: 2, name: '肉类供应商' },
      { id: 3, name: '海鲜供应商' },
      { id: 4, name: '粮油供应商' },
      { id: 5, name: '禽蛋供应商' }
    ])
    
    // 对话框相关
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加食材')
    const formData = reactive({})
    const formRef = ref(null)
    
    // 入库对话框
    const stockInDialogVisible = ref(false)
    const stockInForm = reactive({})
    const stockInFormRef = ref(null)
    
    // 出库对话框
    const stockOutDialogVisible = ref(false)
    const stockOutForm = reactive({})
    const stockOutFormRef = ref(null)
    
    // 表单验证规则
    const formRules = {
      name: [{ required: true, message: '请输入食材名称', trigger: 'blur' }],
      category: [{ required: true, message: '请选择类别', trigger: 'blur' }],
      unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
      current_stock: [{ required: true, message: '请输入当前库存', trigger: 'blur', type: 'number' }],
      minimum_stock: [{ required: true, message: '请输入最低库存', trigger: 'blur', type: 'number' }],
      price: [{ required: true, message: '请输入单价', trigger: 'blur', type: 'number' }],
      supplier_id: [{ required: true, message: '请选择供应商', trigger: 'blur' }]
    }
    
    const stockInRules = {
      quantity: [{ required: true, message: '请输入入库数量', trigger: 'blur', type: 'number', min: 1 }],
      price: [{ required: true, message: '请输入入库单价', trigger: 'blur', type: 'number', min: 0.01 }]
    }
    
    const stockOutRules = {
      quantity: [{ required: true, message: '请输入出库数量', trigger: 'blur', type: 'number', min: 1 }]
    }
    
    // 处理搜索
    const handleSearch = () => {
      console.log('搜索条件', searchForm)
      // 这里可以添加实际的搜索逻辑
    }
    
    // 重置搜索
    const resetSearch = () => {
      searchForm.name = ''
      searchForm.category = ''
      searchForm.stockStatus = ''
    }
    
    // 处理添加食材
    const handleAddIngredient = () => {
      dialogTitle.value = '添加食材'
      // 重置表单
      Object.assign(formData, {
        name: '',
        category: '',
        unit: '',
        current_stock: 0,
        minimum_stock: 0,
        price: 0,
        supplier_id: '',
        expiry_date: '',
        nutrition_info: '',
        calories: 0,
        restrictions: '',
        purchaser: '',
        origin: ''
      })
      dialogVisible.value = true
    }
    
    // 处理编辑食材
    const handleEditIngredient = (ingredient) => {
      dialogTitle.value = '编辑食材'
      // 填充表单数据
      Object.assign(formData, { ...ingredient })
      dialogVisible.value = true
    }
    
    // 处理提交
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        console.log('表单数据', formData)
        // 这里可以添加实际的提交逻辑
        dialogVisible.value = false
        // 刷新数据
        // fetchIngredients()
      } catch (error) {
        console.log('验证失败', error)
      }
    }
    
    // 处理入库
    const handleStockIn = (ingredient) => {
      Object.assign(stockInForm, {
        id: ingredient.id,
        name: ingredient.name,
        current_stock: ingredient.current_stock,
        quantity: 0,
        price: ingredient.price,
        notes: ''
      })
      stockInDialogVisible.value = true
    }
    
    // 处理入库提交
    const handleStockInSubmit = async () => {
      if (!stockInFormRef.value) return
      
      try {
        await stockInFormRef.value.validate()
        console.log('入库数据', stockInForm)
        // 这里可以添加实际的入库逻辑
        stockInDialogVisible.value = false
        // 刷新数据
        // fetchIngredients()
      } catch (error) {
        console.log('验证失败', error)
      }
    }
    
    // 处理出库
    const handleStockOut = (ingredient) => {
      Object.assign(stockOutForm, {
        id: ingredient.id,
        name: ingredient.name,
        current_stock: ingredient.current_stock,
        quantity: 0,
        notes: ''
      })
      stockOutDialogVisible.value = true
    }
    
    // 处理出库提交
    const handleStockOutSubmit = async () => {
      if (!stockOutFormRef.value) return
      
      try {
        await stockOutFormRef.value.validate()
        // 检查库存是否足够
        if (stockOutForm.quantity > stockOutForm.current_stock) {
          ElMessage.error('库存不足')
          return
        }
        console.log('出库数据', stockOutForm)
        // 这里可以添加实际的出库逻辑
        stockOutDialogVisible.value = false
        // 刷新数据
        // fetchIngredients()
      } catch (error) {
        console.log('验证失败', error)
      }
    }
    
    // 处理删除食材
    const handleDeleteIngredient = (id) => {
      ElMessageBox.confirm('确定要删除该食材吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log('删除食材', id)
        // 这里可以添加实际的删除逻辑
        // fetchIngredients()
      }).catch(() => {
        // 取消删除
      })
    }
    
    // 处理导入
    const handleImport = () => {
      console.log('导入食材')
      // 这里可以添加实际的导入逻辑
    }
    
    // 处理导出
    const handleExport = () => {
      console.log('导出食材')
      // 这里可以添加实际的导出逻辑
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      // 刷新数据
      // fetchIngredients()
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
      // 刷新数据
      // fetchIngredients()
    }
    
    // 获取食材数据
    const fetchIngredients = async () => {
      try {
        // 这里可以添加实际的数据获取逻辑
        // const response = await api.get('/ingredients')
        // ingredients.value = response.data
      } catch (error) {
        console.log('获取食材数据失败', error)
      }
    }
    
    // 获取供应商数据
    const fetchSuppliers = async () => {
      try {
        // 这里可以添加实际的数据获取逻辑
        // const response = await api.get('/suppliers')
        // suppliers.value = response.data
      } catch (error) {
        console.log('获取供应商数据失败', error)
      }
    }
    
    // 生命周期
    onMounted(() => {
      // 获取数据
      // fetchIngredients()
      // fetchSuppliers()
    })
    
    return {
      searchForm,
      ingredients,
      suppliers,
      currentPage,
      pageSize,
      total,
      dialogVisible,
      dialogTitle,
      formData,
      formRef,
      stockInDialogVisible,
      stockInForm,
      stockInFormRef,
      stockOutDialogVisible,
      stockOutForm,
      stockOutFormRef,
      formRules,
      stockInRules,
      stockOutRules,
      handleSearch,
      resetSearch,
      handleAddIngredient,
      handleEditIngredient,
      handleSubmit,
      handleStockIn,
      handleStockInSubmit,
      handleStockOut,
      handleStockOutSubmit,
      handleDeleteIngredient,
      handleImport,
      handleExport,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.ingredient-management {
  padding: 20px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.search-card {
  margin-bottom: 20px;
}

.list-card {
  margin-bottom: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-count {
  font-size: 14px;
  color: #606266;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .el-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .el-form-item {
    margin-bottom: 0;
  }
}
</style>

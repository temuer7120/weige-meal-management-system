<template>
  <div class="employee-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>员工管理</span>
          <el-button type="primary" @click="showAddEmployeeDialog">
            <el-icon><Plus /></el-icon>
            添加员工
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-input
          v-model="searchQuery"
          placeholder="搜索员工姓名或工号"
          prefix-icon="Search"
          style="width: 300px"
          @keyup.enter="handleSearch"
        />
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </div>

      <!-- 员工列表 -->
      <el-table
        v-loading="employeeStore.loading"
        :data="employeeStore.employees"
        style="width: 100%"
        border
      >
        <el-table-column prop="id" label="工号" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="gender" label="性别" width="80" />
        <el-table-column prop="position" label="职位" width="120" />
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '在职' : '离职' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewEmployee(row.id)">查看</el-button>
            <el-button size="small" type="primary" @click="editEmployee(row.id)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteEmployee(row.id)">删除</el-button>
            <el-button size="small" @click="viewWorkloadStats(row.id)">工作量</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="employeeStore.page"
          v-model:page-size="employeeStore.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="employeeStore.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEmployeeStore } from '../store/employee'
import { Plus } from '@element-plus/icons-vue'

const employeeStore = useEmployeeStore()
const searchQuery = ref('')

// 生命周期
onMounted(async () => {
  await employeeStore.getEmployees()
})

// 显示添加员工对话框
const showAddEmployeeDialog = () => {
  // 实现添加员工的逻辑
}

// 编辑员工
const editEmployee = async (id) => {
  // 实现编辑员工的逻辑
}

// 查看员工详情
const viewEmployee = async (id) => {
  // 实现查看员工详情的逻辑
}

// 删除员工
const deleteEmployee = async (id) => {
  await employeeStore.deleteEmployee(id)
  await employeeStore.getEmployees()
}

// 查看工作量统计
const viewWorkloadStats = (id) => {
  // 实现查看工作量统计的逻辑
}

// 搜索处理
const handleSearch = async () => {
  // 实现搜索逻辑
  await employeeStore.getEmployees()
}

// 重置搜索
const resetSearch = () => {
  searchQuery.value = ''
  employeeStore.setPage(1)
  employeeStore.getEmployees()
}

// 分页处理
const handleSizeChange = (size) => {
  employeeStore.setPageSize(size)
  employeeStore.getEmployees()
}

const handleCurrentChange = (current) => {
  employeeStore.setPage(current)
  employeeStore.getEmployees()
}
</script>

<style scoped>
.employee-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-filter {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>

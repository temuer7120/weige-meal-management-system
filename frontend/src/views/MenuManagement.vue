<template>
  <div class="menu-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>菜单管理</span>
          <el-button type="primary">
            <el-icon><Plus /></el-icon>
            添加菜单
          </el-button>
        </div>
      </template>
      <el-empty description="菜单管理功能开发中" />
    </el-card>
  </div>
</template>

<script setup>
import { Plus } from '@element-plus/icons-vue'
</script>

<style scoped>
.menu-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

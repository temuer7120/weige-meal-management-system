<template>
  <div class="financial-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>财务管理</span>
          <el-button type="primary">
            <el-icon><Refresh /></el-icon>
            刷新数据
          </el-button>
        </div>
      </template>
      <el-empty description="财务管理功能开发中" />
    </el-card>
  </div>
</template>

<script setup>
import { Refresh } from '@element-plus/icons-vue'
</script>

<style scoped>
.financial-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

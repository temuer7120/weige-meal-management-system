<template>
  <div class="mother-baby-service">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>母婴服务</span>
          <el-button type="primary">
            <el-icon><Plus /></el-icon>
            添加服务
          </el-button>
        </div>
      </template>
      <el-empty description="母婴服务功能开发中" />
    </el-card>
  </div>
</template>

<script setup>
import { Plus } from '@element-plus/icons-vue'
</script>

<style scoped>
.mother-baby-service {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

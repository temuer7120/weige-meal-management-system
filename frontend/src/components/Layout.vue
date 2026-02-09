<template>
  <el-container>
    <!-- 顶部导航 -->
    <el-header class="top-header">
      <div class="logo">
        <h1>公司管理系统</h1>
      </div>
      <div class="main-nav">
        <el-menu
          :default-active="activeMenu"
          class="el-menu-horizontal"
          mode="horizontal"
          @select="handleMenuSelect"
          background-color="#303133"
          text-color="#fff"
          active-text-color="#409eff"
          :router="true"
        >
          <el-menu-item index="/">
            <el-icon><House /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          
          <!-- 月子餐下拉菜单 -->
          <el-sub-menu index="月子餐">
            <template #title>
              <el-icon><MugCup /></el-icon>
              <span>月子餐</span>
            </template>
            <el-menu-item index="/ingredients">食材管理</el-menu-item>
            <el-menu-item index="/dishes">菜品管理</el-menu-item>
            <el-menu-item index="/menus">菜单管理</el-menu-item>
            <el-menu-item index="/mother-baby">母婴服务</el-menu-item>
            <el-menu-item index="/orders">订单管理</el-menu-item>
          </el-sub-menu>
          
          <!-- 公司管理下拉菜单 -->
          <el-sub-menu index="公司管理">
            <template #title>
              <el-icon><OfficeBuilding /></el-icon>
              <span>公司管理</span>
            </template>
            <el-menu-item index="/employees">员工管理</el-menu-item>
            <el-menu-item index="/financial">财务管理</el-menu-item>
            <el-menu-item index="/statistics">统计分析</el-menu-item>
            <el-menu-item index="/system" v-if="isAdmin">系统管理</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </div>
      <div class="user-info">
        <el-dropdown>
          <span class="user-dropdown">
            <el-avatar :size="32">{{ userName }}</el-avatar>
            <span>{{ userRole }}</span>
            <i class="el-icon-arrow-down"></i>
          </span>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleProfile">个人资料</el-dropdown-item>
            <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-header>
    
    <!-- 内容区域 -->
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { House, MugCup, OfficeBuilding } from '@element-plus/icons-vue'

export default {
  name: 'Layout',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    
    // 计算当前活跃菜单
    const activeMenu = computed(() => {
      return route.path
    })
    
    // 计算用户名和角色
    const userName = computed(() => {
      return authStore.user?.profile?.name || authStore.user?.username || '用户'
    })
    
    const userRole = computed(() => {
      return authStore.user?.role || ''
    })
    
    const isAdmin = computed(() => {
      return authStore.user?.role === 'admin'
    })
    
    // 处理菜单选择
    const handleMenuSelect = (key) => {
      router.push(key)
    }
    
    // 处理个人资料
    const handleProfile = () => {
      // 跳转到个人资料页面
      console.log('个人资料')
    }
    
    // 处理退出登录
    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    // 初始化
    onMounted(() => {
      // 检查用户是否已登录
      if (!authStore.isAuthenticated) {
        router.push('/login')
      }
    })
    
    return {
      activeMenu,
      userName,
      userRole,
      isAdmin,
      handleMenuSelect,
      handleProfile,
      handleLogout
    }
  }
}
</script>

<style scoped>
.top-header {
  display: flex;
  align-items: center;
  padding: 0 20px;
  background-color: #303133;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 60px;
}

.logo {
  margin-right: 30px;
  min-width: 180px;
  display: flex;
  align-items: center;
}

.logo h1 {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
  margin: 0;
  white-space: nowrap;
}

.main-nav {
  flex: 1;
}

.el-menu-horizontal {
  border-bottom: none;
}

.el-menu-horizontal .el-menu-item {
  height: 60px;
  line-height: 60px;
  margin: 0;
  padding: 0 20px;
}

.user-info {
  margin-left: 20px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  color: #fff;
}

.user-dropdown span {
  font-size: 14px;
}

.el-main {
  padding: 20px;
  min-height: calc(100vh - 60px);
  background-color: #f5f7fa;
}
</style>

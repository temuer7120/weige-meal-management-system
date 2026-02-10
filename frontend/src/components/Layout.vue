<template>
  <el-container>
    <!-- 顶部导航 -->
    <el-header class="top-header">
      <div class="logo">
        <h1>上海巍阁母婴护理中心</h1>
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
              <el-icon><Coffee /></el-icon>
              <span>月子餐</span>
            </template>
            <el-menu-item index="/ingredients" v-if="isAdmin || userRole === 'staff'">食材管理</el-menu-item>
            <el-menu-item index="/dishes" v-if="isAdmin || userRole === 'staff'">菜品管理</el-menu-item>
            <el-menu-item index="/menus" v-if="isAdmin || userRole === 'staff'">菜单管理</el-menu-item>
            <el-menu-item index="/mother-baby" v-if="isAdmin || userRole === 'staff' || userRole === 'customer'">母婴服务</el-menu-item>
            <el-menu-item index="/orders" v-if="isAdmin || userRole === 'manager' || userRole === 'staff'">订单管理</el-menu-item>
          </el-sub-menu>
          
          <!-- 公司管理下拉菜单 -->
          <el-sub-menu index="公司管理">
            <template #title>
              <el-icon><OfficeBuilding /></el-icon>
              <span>公司管理</span>
            </template>
            <el-menu-item index="/employees" v-if="isAdmin || userRole === 'manager'">员工管理</el-menu-item>
            <el-menu-item index="/financial" v-if="isAdmin || userRole === 'manager'">财务管理</el-menu-item>
            <el-menu-item index="/statistics" v-if="isAdmin || userRole === 'manager'">统计分析</el-menu-item>
            <el-menu-item index="/system" v-if="isAdmin">系统管理</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </div>
      <div class="user-info">
        <div class="user-details">
          <el-avatar :size="32">{{ userName }}</el-avatar>
          <span class="user-role">{{ userRole }}</span>
          <span class="user-name">{{ userName }}</span>
        </div>
        <el-button type="text" class="logout-button" @click="handleLogout">
          <span>退出</span>
        </el-button>
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
import { House, Coffee, OfficeBuilding } from '@element-plus/icons-vue'

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
      // 初始化认证信息
      authStore.initAuth()
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
  margin-right: 60px;
  min-width: 280px;
  display: flex;
  align-items: center;
}

.logo h1 {
  font-size: 18px;
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
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-details {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
}

.user-role {
  font-size: 14px;
  color: #409eff;
}

.user-name {
  font-size: 14px;
}

.logout-button {
  color: #fff;
  font-size: 14px;
  border-left: 1px solid #404244;
  padding-left: 20px;
}

.logout-button:hover {
  color: #409eff;
}

.el-main {
  padding: 20px;
  min-height: calc(100vh - 60px);
  background-color: #f5f7fa;
}
</style>

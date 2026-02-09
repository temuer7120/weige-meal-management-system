<template>
  <el-container>
    <!-- 侧边栏导航 -->
    <el-aside :class="{ collapsed: isCollapsed }">
      <div class="logo">
        <h1 v-if="!isCollapsed">餐食管理系统</h1>
        <h1 v-else>餐管</h1>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical-demo"
        @select="handleMenuSelect"
        :collapse="isCollapsed"
      >
        <el-menu-item index="/">
          <i class="el-icon-s-home"></i>
          <span slot="title">仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/ingredients">
          <i class="el-icon-s-grid"></i>
          <span slot="title">食材管理</span>
        </el-menu-item>
        <el-menu-item index="/dishes">
          <i class="el-icon-s-food"></i>
          <span slot="title">菜品管理</span>
        </el-menu-item>
        <el-menu-item index="/menus">
          <i class="el-icon-s-order"></i>
          <span slot="title">菜单管理</span>
        </el-menu-item>
        <el-menu-item index="/orders">
          <i class="el-icon-s-marketing"></i>
          <span slot="title">订单管理</span>
        </el-menu-item>
        <el-menu-item index="/employees">
          <i class="el-icon-user"></i>
          <span slot="title">员工管理</span>
        </el-menu-item>
        <el-menu-item index="/statistics">
          <i class="el-icon-data-analysis"></i>
          <span slot="title">统计分析</span>
        </el-menu-item>
        <el-menu-item index="/financial">
          <i class="el-icon-money"></i>
          <span slot="title">财务管理</span>
        </el-menu-item>
        <el-menu-item index="/mother-baby">
          <i class="el-icon-sugar"></i>
          <span slot="title">母婴服务</span>
        </el-menu-item>
        <el-menu-item index="/system" v-if="isAdmin">
          <i class="el-icon-setting"></i>
          <span slot="title">系统管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <!-- 主内容区域 -->
    <el-container>
      <!-- 顶部栏 -->
      <el-header>
        <div class="header-left">
          <el-button type="text" @click="toggleCollapse">
            <i :class="isCollapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'"></i>
          </el-button>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              <el-avatar :size="32">{{ userName }}</el-avatar>
              <span>{{ userRole }}</span>
              <i class="el-icon-arrow-down"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item @click="handleProfile">个人资料</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      
      <!-- 内容区域 -->
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../store/auth'

export default {
  name: 'Layout',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    
    const isCollapsed = ref(false)
    
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
    
    // 切换侧边栏折叠状态
    const toggleCollapse = () => {
      isCollapsed.value = !isCollapsed.value
    }
    
    // 处理菜单选择
    const handleMenuSelect = (key) => {
      router.push(key)
    }
    
    // 处理个人资料
    const handleProfile = () => {
      // 跳转到个人资料页面
      console.log('个人资料')
    }
    
    // 初始化
    onMounted(() => {
      // 检查用户是否已登录
      if (!authStore.isAuthenticated) {
        router.push('/login')
      }
    })
    
    return {
      isCollapsed,
      activeMenu,
      userName,
      userRole,
      isAdmin,
      toggleCollapse,
      handleMenuSelect,
      handleProfile
    }
  }
}
</script>

<style scoped>
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #303133;
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.user-info span {
  font-size: 14px;
}

.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.el-aside {
  background-color: #303133;
  color: #fff;
  transition: width 0.3s;
}

.el-aside.collapsed {
  width: 64px !important;
}

.el-menu-vertical-demo {
  height: 100%;
  border-right: none;
}

.el-menu-item {
  height: 60px;
  line-height: 60px;
  margin: 0;
  padding: 0 20px;
}

.el-menu-item:hover,
.el-menu-item.is-active {
  color: #fff;
  background-color: #409eff;
}

.el-menu-item i {
  font-size: 18px;
  margin-right: 10px;
}
</style>

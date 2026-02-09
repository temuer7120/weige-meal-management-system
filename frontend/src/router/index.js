import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import IngredientManagement from '../views/IngredientManagement.vue'
import DishManagement from '../views/DishManagement.vue'
import MenuManagement from '../views/MenuManagement.vue'
import OrderManagement from '../views/OrderManagement.vue'
import EmployeeManagement from '../views/EmployeeManagement.vue'
import FinancialManagement from '../views/FinancialManagement.vue'
import SystemManagement from '../views/SystemManagement.vue'
import MotherBabyService from '../views/MotherBabyService.vue'
import Statistics from '../views/Statistics.vue'
import { useAuthStore } from '../store/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/ingredients',
    name: 'IngredientManagement',
    component: IngredientManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/dishes',
    name: 'DishManagement',
    component: DishManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/menus',
    name: 'MenuManagement',
    component: MenuManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'OrderManagement',
    component: OrderManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/employees',
    name: 'EmployeeManagement',
    component: EmployeeManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/financial',
    name: 'FinancialManagement',
    component: FinancialManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/system',
    name: 'SystemManagement',
    component: SystemManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/mother-baby',
    name: 'MotherBabyService',
    component: MotherBabyService,
    meta: { requiresAuth: true }
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const isAdmin = authStore.user?.role === 'admin'
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && !isAdmin) {
    next('/')
  } else if (to.path === '/login' && isAuthenticated) {
    // 已登录用户不能访问登录页面
    next('/')
  } else {
    next()
  }
})

export default router

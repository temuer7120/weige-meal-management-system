import axios from 'axios'
import { useAuthStore } from '../store/auth'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()
    
    // 处理401错误（令牌过期）
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        // 尝试刷新令牌
        await authStore.refreshToken()
        // 重新发送原始请求
        originalRequest.headers.Authorization = `Bearer ${authStore.token}`
        return api(originalRequest)
      } catch (refreshError) {
        // 刷新令牌失败，跳转到登录页
        authStore.logout()
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

export default api

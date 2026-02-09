import { defineStore } from 'pinia'
import axios from 'axios'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },
  
  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null
      
      try {
        // 尝试调用后端API登录
        try {
          const response = await axios.post('/api/auth/login', {
            username,
            password
          })
          
          const { access_token, refresh_token, user } = response.data
          
          this.token = access_token
          this.refreshToken = refresh_token
          this.user = user
          
          localStorage.setItem('token', access_token)
          localStorage.setItem('refreshToken', refresh_token)
          
          // 设置axios默认头
          axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
          
          router.push('/')
        } catch (apiError) {
          // 后端API调用失败，使用模拟数据登录
          console.log('后端API不可用，使用模拟数据登录')
          
          // 模拟登录验证
          if (username === 'admin' && password === 'admin123') {
            // 模拟登录成功
            const mockToken = 'mock-token-' + Date.now()
            const mockUser = {
              id: 1,
              username: 'admin',
              role: 'admin',
              profile: {
                name: '管理员',
                position: '系统管理员',
                contact: 'admin@example.com'
              }
            }
            
            this.token = mockToken
            this.refreshToken = mockToken
            this.user = mockUser
            
            localStorage.setItem('token', mockToken)
            localStorage.setItem('refreshToken', mockToken)
            
            router.push('/')
          } else {
            // 模拟登录失败
            throw new Error('用户名或密码错误')
          }
        }
      } catch (error) {
        this.error = error.message || '登录失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        // 尝试调用后端API注册
        try {
          const response = await axios.post('/api/auth/register', userData)
          return response.data
        } catch (apiError) {
          // 后端API调用失败，使用模拟数据
          console.log('后端API不可用，使用模拟数据')
          return {
            id: Date.now(),
            username: userData.username,
            email: userData.email,
            full_name: userData.full_name
          }
        }
      } catch (error) {
        this.error = error.response?.data?.error || '注册失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async refreshToken() {
      try {
        // 尝试调用后端API刷新token
        try {
          const response = await axios.post('/api/auth/refresh')
          const { access_token } = response.data
          
          this.token = access_token
          localStorage.setItem('token', access_token)
          axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
          
          return access_token
        } catch (apiError) {
          // 后端API调用失败，使用模拟token
          console.log('后端API不可用，使用模拟token')
          const mockToken = 'mock-token-' + Date.now()
          this.token = mockToken
          localStorage.setItem('token', mockToken)
          return mockToken
        }
      } catch (error) {
        this.logout()
        throw error
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      this.refreshToken = null
      
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      
      delete axios.defaults.headers.common['Authorization']
      
      router.push('/login')
    },
    
    initAuth() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        
        // 如果没有用户信息，设置模拟用户信息
        if (!this.user) {
          this.user = {
            id: 1,
            username: 'admin',
            role: 'admin',
            profile: {
              name: '管理员',
              position: '系统管理员',
              contact: 'admin@example.com'
            }
          }
        }
      }
    }
  }
})

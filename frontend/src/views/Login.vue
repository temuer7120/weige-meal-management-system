<template>
  <div class="login-container">
    <!-- 公司网站头部 -->
    <div class="company-header">
      <div class="company-logo">
        <h1>WeigeCo</h1>
      </div>
      <div class="company-nav">
        <a href="#" class="nav-link">首页</a>
        <a href="#" class="nav-link">关于我们</a>
        <a href="#" class="nav-link">服务项目</a>
        <a href="#" class="nav-link">联系我们</a>
      </div>
    </div>

    <!-- 登录注册区域 -->
    <div class="login-register-section">
      <div class="login-register-container">
        <!-- 左侧：系统介绍 -->
        <div class="system-intro">
          <h2>餐食管理系统</h2>
          <p>专业的企业级餐食管理解决方案，为您提供高效、便捷的餐饮服务管理体验。</p>
          <div class="features">
            <div class="feature-item">
              <el-icon class="feature-icon"><Suitcase /></el-icon>
              <span>食材管理</span>
            </div>
            <div class="feature-item">
              <el-icon class="feature-icon"><MugCup /></el-icon>
              <span>菜品管理</span>
            </div>
            <div class="feature-item">
              <el-icon class="feature-icon"><Notebook /></el-icon>
              <span>订单管理</span>
            </div>
            <div class="feature-item">
              <el-icon class="feature-icon"><UserFilled /></el-icon>
              <span>员工管理</span>
            </div>
          </div>
        </div>

        <!-- 右侧：登录注册表单 -->
        <el-card class="auth-card">
          <!-- 标签切换 -->
          <div class="auth-tabs">
            <div 
              class="auth-tab" 
              :class="{ active: activeTab === 'login' }"
              @click="activeTab = 'login'"
            >
              登录
            </div>
            <div 
              class="auth-tab" 
              :class="{ active: activeTab === 'register' }"
              @click="activeTab = 'register'"
            >
              注册
            </div>
          </div>

          <!-- 登录表单 -->
          <el-form 
            v-if="activeTab === 'login'" 
            :model="loginForm" 
            :rules="loginRules" 
            ref="loginFormRef" 
            label-width="80px"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="loginForm.username" placeholder="请输入用户名" prefix-icon="UserFilled"></el-input>
            </el-form-item>
            
            <el-form-item label="密码" prop="password">
              <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" prefix-icon="Lock"></el-input>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" class="auth-button" @click="handleLogin" :loading="loading">登录</el-button>
            </el-form-item>
            
            <el-form-item v-if="error" class="error-message">
              <el-alert
                :title="error"
                type="error"
                show-icon
                :closable="false"
              />
            </el-form-item>
          </el-form>

          <!-- 注册表单 -->
          <el-form 
            v-else 
            :model="registerForm" 
            :rules="registerRules" 
            ref="registerFormRef" 
            label-width="80px"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="registerForm.username" placeholder="请输入用户名" prefix-icon="UserFilled"></el-input>
            </el-form-item>
            
            <el-form-item label="密码" prop="password">
              <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" prefix-icon="Lock"></el-input>
            </el-form-item>
            
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请确认密码" prefix-icon="Check"></el-input>
            </el-form-item>
            
            <el-form-item label="姓名" prop="name">
              <el-input v-model="registerForm.name" placeholder="请输入姓名" prefix-icon="Avatar"></el-input>
            </el-form-item>
            
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="registerForm.phone" placeholder="请输入联系电话" prefix-icon="Phone"></el-input>
            </el-form-item>
            
            <el-form-item label="角色" prop="role">
              <el-select v-model="registerForm.role" placeholder="请选择角色">
                <el-option label="管理员" value="admin"></el-option>
                <el-option label="员工" value="employee"></el-option>
                <el-option label="客户" value="customer"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" class="auth-button" @click="handleRegister" :loading="loading">注册</el-button>
            </el-form-item>
            
            <el-form-item v-if="error" class="error-message">
              <el-alert
                :title="error"
                type="error"
                show-icon
                :closable="false"
              />
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>

    <!-- 页脚 -->
    <div class="footer">
      <p>&copy; {{ new Date().getFullYear() }} WeigeCo. 保留所有权利。</p>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const loginFormRef = ref(null)
    const registerFormRef = ref(null)
    const loading = ref(false)
    const error = ref('')
    const activeTab = ref('login')
    
    const loginForm = reactive({
      username: '',
      password: ''
    })
    
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少为 6 个字符', trigger: 'blur' }
      ]
    }
    
    const registerForm = reactive({
      username: '',
      password: '',
      confirmPassword: '',
      name: '',
      phone: '',
      role: ''
    })
    
    const registerRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少为 6 个字符', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        { validator: (rule, value, callback) => {
            if (value !== registerForm.password) {
              callback(new Error('两次输入的密码不一致'))
            } else {
              callback()
            }
          }, trigger: 'blur' }
      ],
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入联系电话', trigger: 'blur' }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ]
    }
    
    const handleLogin = async () => {
      // 表单验证
      if (!loginFormRef.value) return
      
      try {
        await loginFormRef.value.validate()
        loading.value = true
        error.value = ''
        
        // 调用登录方法
        await authStore.login(loginForm.username, loginForm.password)
        
        // 登录成功，跳转到首页
        router.push('/')
      } catch (err) {
        // 处理验证错误和登录错误
        if (err.name === 'ValidationError') {
          // 表单验证错误，由 Element Plus 自动处理
        } else {
          // 登录错误
          error.value = err.response?.data?.error || '登录失败，请检查用户名和密码'
        }
      } finally {
        loading.value = false
      }
    }
    
    const handleRegister = async () => {
      // 表单验证
      if (!registerFormRef.value) return
      
      try {
        await registerFormRef.value.validate()
        loading.value = true
        error.value = ''
        
        // 调用注册方法
        await authStore.register(registerForm)
        
        // 注册成功，切换到登录标签
        activeTab.value = 'login'
        error.value = '注册成功，请登录'
      } catch (err) {
        // 处理验证错误和注册错误
        if (err.name === 'ValidationError') {
          // 表单验证错误，由 Element Plus 自动处理
        } else {
          // 注册错误
          error.value = err.response?.data?.error || '注册失败，请稍后重试'
        }
      } finally {
        loading.value = false
      }
    }
    
    return {
      activeTab,
      loginForm,
      loginRules,
      loginFormRef,
      registerForm,
      registerRules,
      registerFormRef,
      loading,
      error,
      handleLogin,
      handleRegister
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f7fa;
}

/* 公司网站头部 */
.company-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 50px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.company-logo h1 {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin: 0;
}

.company-nav {
  display: flex;
  gap: 30px;
}

.nav-link {
  text-decoration: none;
  color: #606266;
  font-size: 16px;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #409EFF;
}

/* 登录注册区域 */
.login-register-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 50px 20px;
}

.login-register-container {
  display: flex;
  max-width: 900px;
  width: 100%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 左侧：系统介绍 */
.system-intro {
  flex: 1;
  padding: 60px 40px;
  background: linear-gradient(135deg, #409EFF 0%, #667EEA 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.system-intro h2 {
  font-size: 32px;
  margin-bottom: 20px;
  font-weight: bold;
}

.system-intro p {
  font-size: 16px;
  margin-bottom: 40px;
  line-height: 1.5;
  opacity: 0.9;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.feature-icon {
  font-size: 24px;
  opacity: 0.9;
}

.feature-item span {
  font-size: 16px;
}

/* 右侧：登录注册表单 */
.auth-card {
  flex: 1;
  padding: 40px;
  border: none;
  box-shadow: none;
}

.auth-tabs {
  display: flex;
  margin-bottom: 30px;
  border-bottom: 1px solid #e4e7ed;
}

.auth-tab {
  padding: 10px 20px;
  font-size: 18px;
  cursor: pointer;
  color: #606266;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
}

.auth-tab:hover {
  color: #409EFF;
}

.auth-tab.active {
  color: #409EFF;
  border-bottom-color: #409EFF;
}

.auth-button {
  width: 100%;
  height: 40px;
  font-size: 16px;
}

.error-message {
  margin-top: 15px;
}

/* 页脚 */
.footer {
  background-color: #fff;
  padding: 20px;
  text-align: center;
  border-top: 1px solid #e4e7ed;
  color: #909399;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .company-header {
    flex-direction: column;
    gap: 15px;
    padding: 15px;
  }
  
  .login-register-container {
    flex-direction: column;
  }
  
  .system-intro {
    padding: 30px 20px;
    text-align: center;
  }
  
  .system-intro h2 {
    font-size: 24px;
  }
  
  .auth-card {
    padding: 30px 20px;
  }
}
</style>

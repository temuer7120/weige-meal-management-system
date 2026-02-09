import { defineStore } from 'pinia'
import api from '../services/api'

export const useEmployeeStore = defineStore('employee', {
  state: () => ({
    employees: [],
    currentEmployee: null,
    loading: false,
    error: null,
    page: 1,
    pageSize: 10,
    total: 0,
    workloadStats: [],
    salaryStats: []
  }),
  
  getters: {
    allEmployees: (state) => state.employees
  },
  
  actions: {
    async getEmployees() {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get('/employees', {
          params: {
            page: this.page,
            page_size: this.pageSize
          }
        })
        
        this.employees = response.data.employees
        this.total = response.data.total
      } catch (error) {
        this.error = error.response?.data?.error || '获取员工列表失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async getEmployeeById(employeeId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get(`/employees/${employeeId}`)
        this.currentEmployee = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || '获取员工详情失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createEmployee(employeeData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.post('/employees', employeeData)
        this.employees.unshift(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || '创建员工失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateEmployee(employeeId, employeeData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.put(`/employees/${employeeId}`, employeeData)
        const index = this.employees.findIndex(emp => emp.id === employeeId)
        if (index !== -1) {
          this.employees[index] = response.data
        }
        if (this.currentEmployee && this.currentEmployee.id === employeeId) {
          this.currentEmployee = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || '更新员工失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteEmployee(employeeId) {
      this.loading = true
      this.error = null
      
      try {
        await api.delete(`/employees/${employeeId}`)
        this.employees = this.employees.filter(emp => emp.id !== employeeId)
      } catch (error) {
        this.error = error.response?.data?.error || '删除员工失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async getWorkloadStats(employeeId, startDate, endDate) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get('/employees/workload-stats', {
          params: {
            employee_id: employeeId,
            start_date: startDate,
            end_date: endDate
          }
        })
        this.workloadStats = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || '获取工作量统计失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async getSalaryStats(employeeId, startDate, endDate) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get('/employees/salary-stats', {
          params: {
            employee_id: employeeId,
            start_date: startDate,
            end_date: endDate
          }
        })
        this.salaryStats = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || '获取薪资统计失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    setPage(page) {
      this.page = page
    },
    
    setPageSize(pageSize) {
      this.pageSize = pageSize
      this.page = 1
    }
  }
})

import { defineStore } from 'pinia'
import api from '../services/api'

export const useOrderStore = defineStore('order', {
  state: () => ({
    orders: [],
    currentOrder: null,
    loading: false,
    error: null,
    page: 1,
    pageSize: 10,
    total: 0,
    filters: {
      orderType: '',
      status: '',
      customerName: '',
      serviceStaff: ''
    }
  }),
  
  getters: {
    filteredOrders: (state) => {
      return state.orders.filter(order => {
        return (
          (state.filters.orderType === '' || order.order_type === state.filters.orderType) &&
          (state.filters.status === '' || order.status === state.filters.status) &&
          (state.filters.customerName === '' || order.customer_name.includes(state.filters.customerName)) &&
          (state.filters.serviceStaff === '' || order.service_staff_name.includes(state.filters.serviceStaff))
        )
      })
    }
  },
  
  actions: {
    async getOrders() {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get('/orders', {
          params: {
            page: this.page,
            page_size: this.pageSize,
            ...this.filters
          }
        })
        
        this.orders = response.data.orders
        this.total = response.data.total
      } catch (error) {
        this.error = error.response?.data?.error || '获取订单列表失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async getOrderById(orderId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get(`/orders/${orderId}`)
        this.currentOrder = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || '获取订单详情失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createOrder(orderData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.post('/orders', orderData)
        this.orders.unshift(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || '创建订单失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateOrder(orderId, orderData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.put(`/orders/${orderId}`, orderData)
        const index = this.orders.findIndex(order => order.id === orderId)
        if (index !== -1) {
          this.orders[index] = response.data
        }
        if (this.currentOrder && this.currentOrder.id === orderId) {
          this.currentOrder = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || '更新订单失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteOrder(orderId) {
      this.loading = true
      this.error = null
      
      try {
        await api.delete(`/orders/${orderId}`)
        this.orders = this.orders.filter(order => order.id !== orderId)
      } catch (error) {
        this.error = error.response?.data?.error || '删除订单失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async confirmOrder(orderId) {
      return this.updateOrder(orderId, { status: 'confirmed' })
    },
    
    async cancelOrder(orderId) {
      return this.updateOrder(orderId, { status: 'cancelled' })
    },
    
    async payOrder(orderId, paymentData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.post(`/orders/${orderId}/pay`, paymentData)
        const index = this.orders.findIndex(order => order.id === orderId)
        if (index !== -1) {
          this.orders[index].status = 'paid'
          this.orders[index].payment_info = response.data.payment_info
        }
        if (this.currentOrder && this.currentOrder.id === orderId) {
          this.currentOrder.status = 'paid'
          this.currentOrder.payment_info = response.data.payment_info
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || '支付失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.page = 1
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

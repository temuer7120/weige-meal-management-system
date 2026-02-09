<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <div class="dashboard-stats">
      <el-card class="stat-card">
        <template #header>
          <div class="stat-header">
            <span>今日订单</span>
            <i class="el-icon-s-order"></i>
          </div>
        </template>
        <div class="stat-content">
          <div class="stat-value">{{ todayOrders }}</div>
          <div class="stat-label">单</div>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <template #header>
          <div class="stat-header">
            <span>今日销售</span>
            <i class="el-icon-money"></i>
          </div>
        </template>
        <div class="stat-content">
          <div class="stat-value">¥{{ todaySales }}</div>
          <div class="stat-label">元</div>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <template #header>
          <div class="stat-header">
            <span>食材库存</span>
            <i class="el-icon-s-grid"></i>
          </div>
        </template>
        <div class="stat-content">
          <div class="stat-value">{{ ingredientCount }}</div>
          <div class="stat-label">种</div>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <template #header>
          <div class="stat-header">
            <span>缺货提醒</span>
            <i class="el-icon-warning"></i>
          </div>
        </template>
        <div class="stat-content">
          <div class="stat-value">{{ lowStockCount }}</div>
          <div class="stat-label">种</div>
        </div>
      </el-card>
    </div>
    
    <!-- 图表区域 -->
    <div class="dashboard-charts">
      <el-card class="chart-card">
        <template #header>
          <div class="chart-header">
            <span>销售趋势</span>
            <el-select v-model="chartPeriod" size="small">
              <el-option label="近7天" value="7d"></el-option>
              <el-option label="近30天" value="30d"></el-option>
              <el-option label="近90天" value="90d"></el-option>
            </el-select>
          </div>
        </template>
        <div class="chart-content">
          <el-empty v-if="!salesData.length" description="暂无销售数据" />
          <div v-else ref="salesChartRef" class="chart"></div>
        </div>
      </el-card>
      
      <el-card class="chart-card">
        <template #header>
          <div class="chart-header">
            <span>订单类型分布</span>
          </div>
        </template>
        <div class="chart-content">
          <el-empty v-if="!orderTypeData.length" description="暂无订单数据" />
          <div v-else ref="orderTypeChartRef" class="chart"></div>
        </div>
      </el-card>
    </div>
    
    <!-- 最近订单 -->
    <el-card class="recent-orders">
      <template #header>
        <div class="orders-header">
          <span>最近订单</span>
          <el-button type="primary" size="small" @click="navigateToOrders">查看全部</el-button>
        </div>
      </template>
      
      <el-table :data="recentOrders" style="width: 100%">
        <el-table-column prop="id" label="订单ID" width="100"></el-table-column>
        <el-table-column prop="order_type" label="订单类型"></el-table-column>
        <el-table-column prop="total_amount" label="金额" width="120">
          <template #default="scope">
            ¥{{ scope.row.total_amount }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100"></el-table-column>
        <el-table-column prop="order_date" label="下单时间"></el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewOrder(scope.row.id)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import api from '../services/api'

export default {
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    
    // 统计数据
    const todayOrders = ref(12)
    const todaySales = ref(3580)
    const ingredientCount = ref(86)
    const lowStockCount = ref(5)
    
    // 图表数据
    const chartPeriod = ref('7d')
    const salesData = ref([1200, 1900, 3000, 2500, 3200, 2800, 3500])
    const orderTypeData = ref([
      { name: '餐食订单', value: 65 },
      { name: '服务订单', value: 35 }
    ])
    
    // 最近订单数据
    const recentOrders = ref([
      { id: 1001, order_type: '餐食订单', total_amount: 128, status: '已完成', order_date: '2026-02-09 10:30' },
      { id: 1002, order_type: '服务订单', total_amount: 298, status: '进行中', order_date: '2026-02-09 09:15' },
      { id: 1003, order_type: '餐食订单', total_amount: 88, status: '已完成', order_date: '2026-02-09 08:45' },
      { id: 1004, order_type: '餐食订单', total_amount: 158, status: '已完成', order_date: '2026-02-08 18:30' },
      { id: 1005, order_type: '服务订单', total_amount: 398, status: '已完成', order_date: '2026-02-08 15:20' }
    ])
    
    // 图表引用
    const salesChartRef = ref(null)
    const orderTypeChartRef = ref(null)
    let salesChart = null
    let orderTypeChart = null
    
    // 初始化图表
    const initSalesChart = () => {
      if (salesChartRef.value) {
        salesChart = echarts.init(salesChartRef.value)
        const option = {
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: ['2/3', '2/4', '2/5', '2/6', '2/7', '2/8', '2/9']
          },
          yAxis: {
            type: 'value',
            axisLabel: {
              formatter: '¥{value}'
            }
          },
          series: [
            {
              data: salesData.value,
              type: 'line',
              smooth: true,
              lineStyle: {
                color: '#409eff'
              },
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: 'rgba(64, 158, 255, 0.5)' },
                  { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
                ])
              }
            }
          ]
        }
        salesChart.setOption(option)
      }
    }
    
    const initOrderTypeChart = () => {
      if (orderTypeChartRef.value) {
        orderTypeChart = echarts.init(orderTypeChartRef.value)
        const option = {
          tooltip: {
            trigger: 'item'
          },
          legend: {
            top: '5%',
            left: 'center'
          },
          series: [
            {
              name: '订单类型',
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: false,
                position: 'center'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: '18',
                  fontWeight: 'bold'
                }
              },
              labelLine: {
                show: false
              },
              data: orderTypeData.value
            }
          ]
        }
        orderTypeChart.setOption(option)
      }
    }
    
    // 导航到订单管理
    const navigateToOrders = () => {
      router.push('/orders')
    }
    
    // 查看订单详情
    const viewOrder = (orderId) => {
      // 导航到订单详情页
      console.log('查看订单', orderId)
    }
    
    // 监听窗口大小变化
    const handleResize = () => {
      salesChart?.resize()
      orderTypeChart?.resize()
    }
    
    // 生命周期
    onMounted(() => {
      initSalesChart()
      initOrderTypeChart()
      window.addEventListener('resize', handleResize)
      
      // 这里可以添加实际的数据获取逻辑
      // fetchDashboardData()
    })
    
    // 监听图表周期变化
    watch(chartPeriod, (newPeriod) => {
      // 根据选择的周期更新图表数据
      console.log('图表周期变化', newPeriod)
      // 这里可以添加实际的数据获取逻辑
    })
    
    return {
      todayOrders,
      todaySales,
      ingredientCount,
      lowStockCount,
      chartPeriod,
      salesData,
      orderTypeData,
      recentOrders,
      salesChartRef,
      orderTypeChartRef,
      navigateToOrders,
      viewOrder
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px 0;
}

.dashboard-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  flex: 1;
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #606266;
}

.stat-header i {
  font-size: 16px;
  color: #409eff;
}

.stat-content {
  margin-top: 20px;
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.dashboard-charts {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  flex: 1;
  min-height: 300px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-content {
  margin-top: 20px;
}

.chart {
  height: 250px;
  width: 100%;
}

.recent-orders {
  margin-top: 20px;
}

.orders-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 768px) {
  .dashboard-stats {
    flex-direction: column;
  }
  
  .dashboard-charts {
    flex-direction: column;
  }
  
  .chart-card {
    min-height: 250px;
  }
  
  .chart {
    height: 200px;
  }
}
</style>

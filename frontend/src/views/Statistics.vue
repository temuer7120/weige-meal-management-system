<template>
  <div class="statistics">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>统计分析</span>
          <el-form :inline="true" :model="dateRange">
            <el-form-item label="时间范围">
              <el-date-picker
                v-model="dateRange.value"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                @change="handleDateRangeChange"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadStatistics">
                <el-icon><Refresh /></el-icon>
                刷新数据
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </template>

      <!-- 概览卡片 -->
      <div class="overview-cards">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ statistics.totalOrders }}</div>
            <div class="stat-label">总订单数</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">¥{{ statistics.totalRevenue }}</div>
            <div class="stat-label">总收入</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ statistics.totalWorkload }}</div>
            <div class="stat-label">总工作量</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ statistics.totalIngredients }}</div>
            <div class="stat-label">食材种类</div>
          </div>
        </el-card>
      </div>

      <!-- 销售趋势图 -->
      <el-card class="chart-card">
        <template #header>
          <span>销售趋势</span>
        </template>
        <div ref="salesChartRef" class="chart-container"></div>
      </el-card>

      <!-- 订单类型分布 -->
      <el-card class="chart-card">
        <template #header>
          <span>订单类型分布</span>
        </template>
        <div ref="orderTypeChartRef" class="chart-container"></div>
      </el-card>

      <!-- 工作量统计 -->
      <el-card class="chart-card">
        <template #header>
          <span>员工工作量统计</span>
        </template>
        <div ref="workloadChartRef" class="chart-container"></div>
      </el-card>

      <!-- 库存状态 -->
      <el-card class="chart-card">
        <template #header>
          <span>库存状态</span>
        </template>
        <div class="inventory-status">
          <el-table :data="inventoryData" border>
            <el-table-column prop="name" label="食材名称" />
            <el-table-column prop="category" label="类别" />
            <el-table-column prop="current_stock" label="当前库存" />
            <el-table-column prop="min_stock" label="最低库存" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStockStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const dateRange = ref({
  value: []
})

const statistics = ref({
  totalOrders: 0,
  totalRevenue: 0,
  totalWorkload: 0,
  totalIngredients: 0
})

const inventoryData = ref([
  { name: '大米', category: '主食', current_stock: 100, min_stock: 50, status: '正常' },
  { name: '面粉', category: '主食', current_stock: 80, min_stock: 40, status: '正常' },
  { name: '鸡蛋', category: '蛋类', current_stock: 20, min_stock: 30, status: '不足' },
  { name: '西红柿', category: '蔬菜', current_stock: 15, min_stock: 25, status: '不足' },
  { name: '黄瓜', category: '蔬菜', current_stock: 30, min_stock: 20, status: '正常' },
  { name: '猪肉', category: '肉类', current_stock: 40, min_stock: 25, status: '正常' },
  { name: '鸡肉', category: '肉类', current_stock: 25, min_stock: 20, status: '正常' },
  { name: '鱼', category: '海鲜', current_stock: 10, min_stock: 15, status: '不足' }
])

// 图表引用
const salesChartRef = ref(null)
const orderTypeChartRef = ref(null)
const workloadChartRef = ref(null)

// 图表实例
let salesChart = null
let orderTypeChart = null
let workloadChart = null

// 生命周期
onMounted(() => {
  // 初始化日期范围为最近30天
  const endDate = new Date()
  const startDate = new Date()
  startDate.setDate(startDate.getDate() - 30)
  dateRange.value = [startDate, endDate]
  
  loadStatistics()
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  disposeCharts()
})

// 加载统计数据
const loadStatistics = () => {
  // 模拟数据加载
  statistics.value = {
    totalOrders: 1250,
    totalRevenue: 89500,
    totalWorkload: 3200,
    totalIngredients: 150
  }
  
  // 渲染图表
  renderSalesChart()
  renderOrderTypeChart()
  renderWorkloadChart()
}

// 初始化图表
const initCharts = () => {
  if (salesChartRef.value) {
    salesChart = echarts.init(salesChartRef.value)
  }
  if (orderTypeChartRef.value) {
    orderTypeChart = echarts.init(orderTypeChartRef.value)
  }
  if (workloadChartRef.value) {
    workloadChart = echarts.init(workloadChartRef.value)
  }
}

// 渲染销售趋势图
const renderSalesChart = () => {
  if (!salesChart) return
  
  const dates = Array.from({ length: 30 }, (_, i) => {
    const date = new Date()
    date.setDate(date.getDate() - 29 + i)
    return `${date.getMonth() + 1}/${date.getDate()}`
  })
  
  const salesData = Array.from({ length: 30 }, () => Math.floor(Math.random() * 5000) + 1000)
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: salesData,
      type: 'line',
      smooth: true,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgba(129, 182, 234, 0.6)'
          },
          {
            offset: 1,
            color: 'rgba(129, 182, 234, 0.1)'
          }
        ])
      }
    }]
  }
  
  salesChart.setOption(option)
}

// 渲染订单类型分布图
const renderOrderTypeChart = () => {
  if (!orderTypeChart) return
  
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [{
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
          fontSize: 20,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 650, name: '餐食订单' },
        { value: 400, name: '服务订单' },
        { value: 200, name: '其他订单' }
      ]
    }]
  }
  
  orderTypeChart.setOption(option)
}

// 渲染工作量统计图
const renderWorkloadChart = () => {
  if (!workloadChart) return
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: ['张三', '李四', '王五', '赵六', '钱七']
    },
    series: [{
      name: '工作量',
      type: 'bar',
      data: [850, 720, 900, 650, 800]
    }]
  }
  
  workloadChart.setOption(option)
}

// 处理日期范围变化
const handleDateRangeChange = () => {
  loadStatistics()
}

// 处理窗口大小变化
const handleResize = () => {
  salesChart?.resize()
  orderTypeChart?.resize()
  workloadChart?.resize()
}

// 销毁图表
const disposeCharts = () => {
  salesChart?.dispose()
  orderTypeChart?.dispose()
  workloadChart?.dispose()
}

// 获取库存状态类型
const getStockStatusType = (status) => {
  switch (status) {
    case '正常':
      return 'success'
    case '不足':
      return 'warning'
    case '缺货':
      return 'danger'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.statistics {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.overview-cards {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  flex: 1;
  min-width: 200px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-top: 8px;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-container {
  width: 100%;
  height: 400px;
}

.inventory-status {
  margin-top: 10px;
}
</style>

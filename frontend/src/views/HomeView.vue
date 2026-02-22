<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const router = useRouter()

// 1. 假数据：核心统计数字
const stats = ref({
  total: 156,
  today: 12,
  hotTemplate: '小红书种草模板'
})

// 2. 页面跳转
const go = (path) => {
  router.push(path)
}

// 3. ECharts 图表渲染逻辑
const chartRef = ref(null)

onMounted(() => {
  // 确保 DOM 挂载完成后再初始化图表
  if (chartRef.value) {
    const myChart = echarts.init(chartRef.value)
    
    // 配置图表 (近7天生成量柱状图)
    const option = {
      title: { text: '近7天AI生成量趋势', left: 'center' },
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      },
      yAxis: { type: 'value' },
      series: [
        {
          data: [12, 19, 15, 22, 18, 28, 12],
          type: 'bar',
          itemStyle: { color: '#409EFF', borderRadius: [4, 4, 0, 0] },
          barWidth: '40%'
        }
      ]
    }
    myChart.setOption(option)

    // 监听窗口大小改变，让图表自适应
    window.addEventListener('resize', () => {
      myChart.resize()
    })
  }
})
</script>

<template>
  <div class="home-container">
    <div class="top-section">
      <h1 class="hero-title">AI 营销文案一键生成</h1>
      <p class="hero-subtitle">选模板 · 输关键词 · 生成适配抖音/小红书的营销文案</p>
      
      <div class="action-section">
        <el-button type="primary" plain class="action-btn" size="large" @click="go('/material')">进入素材库</el-button>
        <el-button type="primary" class="action-btn highlight-btn" size="large" @click="go('/generate')">开始创作</el-button>
        <el-button type="info" plain class="action-btn" size="large" @click="go('/history')">查看创作记录</el-button>
      </div>
    </div>

    <el-divider />

    <div class="dashboard-section">
      <el-row :gutter="20" class="stats-row">
        <el-col :span="8">
          <el-card shadow="hover" class="stats-card">
            <div class="card-label">累计生成文案数</div>
            <div class="card-num">{{ stats.total }} <span class="unit">条</span></div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="stats-card">
            <div class="card-label">今日生成数</div>
            <div class="card-num">{{ stats.today }} <span class="unit">条</span></div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="stats-card">
            <div class="card-label">最热模板</div>
            <div class="card-val">{{ stats.hotTemplate }}</div>
          </el-card>
        </el-col>
      </el-row>

      <div class="chart-container">
        <div ref="chartRef" style="width: 100%; height: 300px;"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 上半区样式 */
.top-section {
  text-align: center;
  padding: 20px 0;
}
.hero-title {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 16px;
}
.hero-subtitle {
  font-size: 16px;
  color: #606266;
  margin-bottom: 30px;
}
.action-section {
  display: flex;
  justify-content: center;
  gap: 30px;
}
.action-btn {
  width: 160px;
  height: 50px;
  font-size: 16px;
}
.highlight-btn {
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

/* 下半区数据看板样式 */
.dashboard-section {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
}
.stats-row {
  margin-bottom: 30px;
}
.stats-card {
  text-align: center;
  padding: 10px 0;
}
.card-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}
.card-num {
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
}
.card-val {
  font-size: 20px;
  font-weight: bold;
  color: #E6A23C;
  line-height: 40px;
}
.unit {
  font-size: 14px;
  color: #606266;
  font-weight: normal;
}
.chart-container {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  border: 1px solid #EBEEF5;
}
</style>
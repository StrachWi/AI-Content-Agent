<script setup>
import { ref } from 'vue'

const searchKeyword = ref('')
const dateRange = ref('')

const historyList = ref([
  { id: 1, topic: '开学季笔记本', time: '2023-10-12 10:00', platform: '抖音 + 小红书' },
  { id: 2, topic: '新款口红测评', time: '2023-10-11 14:30', platform: '小红书' },
  { id: 3, topic: '运动鞋推广', time: '2023-10-10 09:15', platform: '抖音' },
])
</script>

<template>
  <div class="history-container">
    
    <!-- 顶部筛选区 -->
    <div class="filter-bar">
      <span class="page-title">创作记录中心</span>
      <div class="filters">
        <el-date-picker 
          v-model="dateRange" 
          type="daterange" 
          range-separator="至" 
          start-placeholder="开始日期" 
          end-placeholder="结束日期"
          style="width: 240px; margin-right: 10px;"
        />
        <el-input 
          v-model="searchKeyword" 
          placeholder="输入文案关键词搜索" 
          style="width: 200px; margin-right: 10px;"
        />
        <el-button type="primary">查询</el-button>
      </div>
    </div>

    <div class="main-body">
      <!-- 左侧：记录列表 (70%) -->
      <div class="list-section">
        <el-table :data="historyList" stripe border style="width: 100%">
          <el-table-column prop="topic" label="创作主题" min-width="180" />
          <el-table-column prop="time" label="生成时间" width="180" />
          <el-table-column prop="platform" label="涉及平台" width="150" />
          <el-table-column label="操作" width="220" fixed="right">
            <template #default>
              <el-button link type="primary">查看/复制</el-button>
              <el-button link type="success">导出</el-button>
              <el-button link type="danger">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 右侧：基础统计卡片 (30%) -->
      <div class="stats-section">
        <div class="stats-title">数据统计</div>
        
        <div class="stats-card">
          <div class="card-label">累计生成文案数</div>
          <div class="card-num">12 <span class="unit">条</span></div>
        </div>

        <div class="stats-card">
          <div class="card-label">本周生成数</div>
          <div class="card-num">8 <span class="unit">条</span></div>
        </div>

        <div class="stats-card">
          <div class="card-label">高频使用模板</div>
          <div class="card-val">抖音产品推广</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.history-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-title {
  font-size: 18px;
  font-weight: bold;
}
.filters {
  display: flex;
}

.main-body {
  flex: 1;
  display: flex;
  gap: 20px;
}

/* 左侧 */
.list-section {
  flex: 0 0 70%;
}

/* 右侧 */
.stats-section {
  flex: 1;
  background: #f9fafc;
  border: 1px solid #e4e7ed;
  padding: 20px;
  border-radius: 4px;
}
.stats-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #303133;
}
.stats-card {
  background: #fff;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.card-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}
.card-num {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}
.card-val {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}
.unit {
  font-size: 12px;
  color: #303133;
  font-weight: normal;
}
</style>
<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

// ================= 1. 状态 =================
const historyList = ref([])
const loading = ref(false)
const stats = ref({ total: 0, today: 0, hotTemplate: '暂无数据' })

// 筛选与分页状态
const searchKeyword = ref('')
const dateRange = ref('') 
const currentPage = ref(1)
const pageSize = ref(4)
const totalRecords = ref(0)

// 弹窗状态
const dialogVisible = ref(false)
const currentContent = ref('')

// ================= 2. 核心逻辑 (对接后端版) =================

// 当搜索条件改变时，重置回第一页并重新请求
const handleSearch = () => {
  currentPage.value = 1
  fetchHistoryList()
}

// 分页页码改变触发
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchHistoryList()
}

// 核心：加载历史记录列表
const fetchHistoryList = async () => {
  loading.value = true
  try {
    // 解析时间参数传给后端
    let startDate = ''
    let endDate = ''
    if (dateRange.value && dateRange.value.length === 2) {
      startDate = dateRange.value[0]
      endDate = dateRange.value[1]
    }

    const response = await axios.get('/api/history', {
      params: {
        keyword: searchKeyword.value, // 把关键词传给后端
        startDate: startDate,         // 把时间传给后端
        endDate: endDate,
        page: currentPage.value,
        limit: pageSize.value
      }
    })

    if (response.data.code === 200) {
      const data = response.data.data
      const rawList = data.list || []
      
      // 映射后端字段，顺手做个“防守”过滤掉测试数据
      historyList.value = rawList
        .filter(item => item.user_input !== '好物推荐' && item.topic !== '好物推荐') 
        .map(item => ({
          id: item.id,
          // 兼容后端乱七八糟的命名（他传什么我们就接什么）
          keyword: item.user_input || item.topic || item.keyword || '无', 
          template: item.template_name || item.template || '',
          time: item.time || '暂无时间',
          platform: item.platform,
          content: item.ai_result || item.content || ''
        }))
        
      totalRecords.value = data.total
    } else {
      ElMessage.error(response.data.msg || '获取历史记录失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请检查后端服务是否启动')
    console.error('Error fetching history:', error)
  } finally {
    loading.value = false
  }
}

// 加载统计数据
const fetchStats = async () => {
  try {
    const response = await axios.get('/api/stats')
    if (response.data.code === 200) {
      stats.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching stats:', error)
  }
}

onMounted(() => {
  fetchHistoryList()
  fetchStats()
})

// ================= 3. 操作事件 =================
const viewContent = (row) => {
  currentContent.value = row.content
  dialogVisible.value = true
}

const copyText = async () => {
  try {
    await navigator.clipboard.writeText(currentContent.value)
    ElMessage.success('文案已成功复制到剪贴板！')
    dialogVisible.value = false
  } catch (err) {
    ElMessage.error('复制失败，请手动选中复制')
  }
}

const exportToTxt = (row) => {
  // ✅ 已修改：导出文件中的抬头改为“核心话题”
  const textContent = `【核心话题】${row.keyword}\n【平台】${row.platform}\n【生成时间】${row.time}\n\n【文案正文】\n${row.content}`
  const blob = new Blob([textContent], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${row.keyword}_文案.txt`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
  ElMessage.success('导出成功！')
}

const deleteItem = async (id) => {
  try {
    const response = await axios.delete(`/api/history/${id}`)
    if (response.data.code === 200) {
      ElMessage.success('删除成功！')
      fetchHistoryList()
      fetchStats()
    } else {
      ElMessage.error('删除失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请检查后端服务是否启动')
  }
}
</script>

<template>
  <div class="history-container">
    
    <div class="filter-bar">
      <span class="page-title">创作记录中心</span>
      <div class="filters">
        <el-date-picker 
          v-model="dateRange" 
          type="daterange" 
          range-separator="至" 
          start-placeholder="开始日期" 
          end-placeholder="结束日期"
          style="width: 260px; margin-right: 15px;"
          value-format="YYYY-MM-DD"
          @change="handleSearch"
        />
        <el-input 
          v-model="searchKeyword" 
          placeholder="输入关键词并回车" 
          style="width: 200px; margin-right: 15px;"
          clearable
          @keyup.enter="handleSearch"
          @clear="handleSearch"
        />
      </div>
    </div>

    <div class="main-body">
      <div class="list-section">
        <el-table :data="historyList" stripe border style="width: 100%; height: 450px;" :loading="loading">
          <el-table-column prop="keyword" label="核心话题" min-width="120" show-overflow-tooltip />
          <el-table-column prop="template" label="模板" width="120" />
          <el-table-column prop="platform" label="平台" width="90" />
          <el-table-column prop="time" label="生成时间" width="160" />
          <el-table-column label="操作" width="220" fixed="right">
            <template #default="scope">
              <el-button link type="primary" @click="viewContent(scope.row)">查看/复制</el-button>
              <el-button link type="success" @click="exportToTxt(scope.row)">导出</el-button>
              <el-button link type="danger" @click="deleteItem(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-wrapper">
          <el-pagination 
            background 
            layout="total, prev, pager, next" 
            :total="totalRecords" 
            :page-size="pageSize"
            :current-page="currentPage"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>

      <div class="stats-section">
        <div class="stats-title">数据统计看板</div>
        
        <div class="stats-card">
          <div class="card-label">累计生成文案数</div>
          <div class="card-num">{{ stats.total }} <span class="unit">条</span></div>
        </div>

        <div class="stats-card">
          <div class="card-label">本周/今日生成数</div>
          <div class="card-num">{{ stats.today }} <span class="unit">条</span></div>
        </div>

        <div class="stats-card">
          <div class="card-label">高频使用模板</div>
          <div class="card-val">{{ stats.hotTemplate }}</div>
        </div>
      </div>
    </div>

    <el-dialog v-model="dialogVisible" title="文案内容" width="50%">
      <el-input
        v-model="currentContent"
        type="textarea"
        :rows="8"
        readonly
      />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="copyText">
            一键复制文案
          </el-button>
        </span>
      </template>
    </el-dialog>

  </div>
</template>

<style scoped>
.history-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-sizing: border-box;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-title {
  font-size: 20px;
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

/* 左侧列表区 */
.list-section {
  flex: 0 0 70%;
  display: flex;
  flex-direction: column;
}
.pagination-wrapper {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

/* 右侧统计区 */
.stats-section {
  flex: 1;
  background: #f9fafc;
  border: 1px solid #e4e7ed;
  padding: 20px;
  border-radius: 8px;
}
.stats-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
  border-bottom: 2px solid #409EFF;
  padding-bottom: 10px;
  display: inline-block;
}
.stats-card {
  background: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
}
.card-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}
.card-num {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
}
.card-val {
  font-size: 18px;
  font-weight: bold;
  color: #E6A23C;
}
.unit {
  font-size: 14px;
  color: #606266;
  font-weight: normal;
}
</style>
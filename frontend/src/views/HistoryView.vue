<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

// ================= 1. 假数据与状态 =================
const historyList = ref([
  { id: 1, keyword: '开学季笔记本', template: '小红书种草', time: '2023-10-12', platform: '小红书', content: '✨开学季必备！这款笔记本颜值太高了吧...\n超级流畅不卡顿，绝绝子！' },
  { id: 2, keyword: '新款口红测评', template: '抖音短视频', time: '2023-10-11', platform: '抖音', content: 'OMG！家人们，今天测的这支口红太显白了！\n黄皮闭眼入，点赞收藏防走丢！' },
  { id: 3, keyword: '运动鞋推广', template: '朋友圈文案', time: '2023-10-10', platform: '微信', content: '跑起来，风都在帮你！新款缓震运动鞋上新，快来带走你的秋季第一双跑鞋。' },
  { id: 4, keyword: '双十一预售', template: '小红书种草', time: '2023-10-09', platform: '小红书', content: '双十一攻略来啦！抄作业必看...' },
  { id: 5, keyword: '护肤品推荐', template: '通用文案', time: '2023-10-08', platform: '通用', content: '熬夜党救星，这套水乳真的绝。' },
])

// 右侧统计假数据
const stats = ref({
  total: 156,
  today: 12,
  hotTemplate: '小红书种草'
})

// 筛选与分页状态
const searchKeyword = ref('')
const dateRange = ref('') // 格式为 [Date, Date]
const currentPage = ref(1)
const pageSize = ref(4)

// 查看/复制弹窗状态
const dialogVisible = ref(false)
const currentContent = ref('')

// ================= 2. 核心逻辑 (纯前端实现) =================

// 综合过滤：同时处理【关键词搜索】和【时间范围筛选】
const filteredList = computed(() => {
  let result = historyList.value

  // 1. 关键词过滤
  if (searchKeyword.value) {
    result = result.filter(item => 
      item.keyword.includes(searchKeyword.value) || item.template.includes(searchKeyword.value)
    )
  }

  // 2. 时间范围过滤
  if (dateRange.value && dateRange.value.length === 2) {
    // 将选中的日期转为时间戳方便比较
    const start = new Date(dateRange.value[0]).getTime()
    const end = new Date(dateRange.value[1]).getTime()
    
    result = result.filter(item => {
      const itemTime = new Date(item.time).getTime()
      return itemTime >= start && itemTime <= end
    })
  }
  
  return result
})

// 分页截取：从过滤后的数据中，根据当前页码截取对应的数据
const pagedList = computed(() => {
  const startIdx = (currentPage.value - 1) * pageSize.value
  const endIdx = startIdx + pageSize.value
  return filteredList.value.slice(startIdx, endIdx)
})

// 分页页码改变触发
const handleCurrentChange = (val) => {
  currentPage.value = val
}

// ================= 3. 操作事件 =================

// 查看并打开弹窗
const viewContent = (row) => {
  currentContent.value = row.content
  dialogVisible.value = true
}

// 复制文案到剪贴板
const copyText = async () => {
  try {
    await navigator.clipboard.writeText(currentContent.value)
    ElMessage.success('文案已成功复制到剪贴板！')
    dialogVisible.value = false
  } catch (err) {
    ElMessage.error('复制失败，请手动选中复制')
  }
}

// 导出 TXT
const exportToTxt = (row) => {
  const textContent = `【关键词】${row.keyword}\n【平台】${row.platform}\n【生成时间】${row.time}\n\n【文案正文】\n${row.content}`
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

// 删除
const deleteItem = (id) => {
  historyList.value = historyList.value.filter(item => item.id !== id)
  ElMessage.success('删除成功！')
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
        />
        <el-input 
          v-model="searchKeyword" 
          placeholder="输入关键词或模板搜索" 
          style="width: 200px; margin-right: 15px;"
          clearable
        />
      </div>
    </div>

    <div class="main-body">
      <div class="list-section">
        <el-table :data="pagedList" stripe border style="width: 100%; height: 450px;">
          <el-table-column prop="keyword" label="关键词" min-width="120" show-overflow-tooltip />
          <el-table-column prop="template" label="模板" width="120" />
          <el-table-column prop="platform" label="平台" width="90" />
          <el-table-column prop="time" label="生成时间" width="120" />
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
            :total="filteredList.length" 
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
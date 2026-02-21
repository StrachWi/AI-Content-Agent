<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
// 后端 API 地址
const API_BASE = 'http://127.0.0.1:8000/api/templates'

// --- 数据区 ---
const tableData = ref([])
const loading = ref(false)
const showEditor = ref(false)
const isEditMode = ref(false)
const editingId = ref(null)

const formData = ref({
  name: '',
  platform: '',
  content: ''
})

// --- 拉取列表 ---
const fetchList = async () => {
  loading.value = true
  try {
    const res = await axios.get(API_BASE)
    if (res.data.code !== 200) throw new Error(res.data.msg)
    tableData.value = res.data.data || []
  } catch (e) {
    ElMessage.error('无法连接后端，请确认后端已启动: ' + e.message)
  } finally {
    loading.value = false
  }
}

// --- 操作逻辑 ---
const handleAdd = () => {
  isEditMode.value = false
  editingId.value = null
  formData.value = { name: '', platform: '', content: '' }
  showEditor.value = true
}

const handleEdit = (row) => {
  isEditMode.value = true
  editingId.value = row.id
  formData.value = { name: row.name, platform: row.platform, content: row.content }
  showEditor.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该模板吗？', '提示', { type: 'warning' })
    const res = await axios.delete(`${API_BASE}/${row.id}`)
    if (res.data.code === 200) {
      ElMessage.success('删除成功')
      fetchList()
    }
  } catch (e) {}
}

const handleSelect = (row) => {
  // 存储选中的模板，供生成页面使用
  localStorage.setItem('selectedTemplate', JSON.stringify(row))
  ElMessage.success(`已选用：${row.name}`)
  router.push('/generate')
}

const handleSave = async () => {
  // 1. 基础非空校验
  if (!formData.value.name.trim()) return ElMessage.warning('模板名称必填')
  if (!formData.value.platform.trim()) return ElMessage.warning('适用平台必填')
  if (!formData.value.content.trim()) return ElMessage.warning('模板内容必填')

  // 2. 核心占位符校验 (确保包含所有"钉子")
  const requiredTags = [
    '{identity}', '{genre}', '{time}', '{platform}', 
    '{topic}', '{keyword}', '{style}', '{emotion}', '{length}'
  ]
  
  const missingTags = requiredTags.filter(tag => !formData.value.content.includes(tag))
  
  if (missingTags.length > 0) {
    return ElMessage.error(`模板内容缺少以下必要占位符：\n${missingTags.join(', ')}`)
  }

  // 3. 发送请求
  try {
    if (isEditMode.value) {
      await axios.put(`${API_BASE}/${editingId.value}`, formData.value)
    } else {
      await axios.post(API_BASE, formData.value)
    }
    ElMessage.success('保存成功')
    showEditor.value = false
    fetchList()
  } catch (e) {
    ElMessage.error('保存失败: ' + e.message)
  }
}

// 页面加载时拉取数据
onMounted(fetchList)
</script>

<template>
  <div class="material-container">
    <!-- 左侧列表区 -->
    <div class="left-panel" :class="{ 'shrink': showEditor }">
      <div class="top-bar">
        <span class="page-title">素材库管理</span>
        <div class="btn-group">
          <el-button type="primary" @click="handleAdd">新增模板</el-button>
          <el-button @click="fetchList">刷新列表</el-button>
        </div>
      </div>

      <el-table :data="tableData" style="width: 100%" stripe border v-loading="loading">
        <el-table-column prop="name" label="模板名称" />
        <el-table-column prop="platform" label="适用平台" width="120">
          <template #default="scope">
            <el-tag>{{ scope.row.platform }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(scope.row)">删除</el-button>
            <el-button link type="success" @click="handleSelect(scope.row)">选用</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 右侧：编辑/新增抽屉 (占 30%) -->
    <!-- 使用 transition 增加滑出动画 -->
    <transition name="slide-fade">
      <div class="right-panel" v-if="showEditor">
        <div class="panel-header">
          <h3>{{ isEditMode ? '编辑模板' : '新增模板' }}</h3>
        </div>
        
        <el-form label-position="top" class="panel-form">
          <el-form-item label="模板名称 (必填)">
            <el-input v-model="formData.name" placeholder="如：开学季笔记本推广" />
          </el-form-item>

          <el-form-item label="模型类型">
            <el-select v-model="formData.platform" placeholder="请选择平台">
              <el-option label="抖音" value="抖音" />
              <el-option label="小红书" value="小红书" />
              <el-option label="通用" value="通用" />
            </el-select>
          </el-form-item>

          <el-form-item label="模板框架内容">
            <el-input 
              v-model="formData.content" 
              type="textarea" 
              :rows="10" 
              placeholder="输入模板框架，用 [场景]、[卖点] 等标注可变方向..." 
            />
          </el-form-item>
        </el-form>

        <div class="panel-footer">
          <el-button @click="showEditor = false">取消</el-button>
          <el-button type="primary" @click="handleSave">保存</el-button>
        </div>
      </div>
    </transition>

  </div>
</template>

<style scoped>
.material-container {
  display: flex;
  height: calc(100vh - 60px); /* 让容器有稳定高度（header 60px） */
  gap: 20px;
  overflow: visible;          /* ✅ 不裁剪右侧面板动画 */
}


.left-panel {
  flex: 1;
  min-width: 0;           /* ✅ 防止 el-table 宽度撑破 flex 布局 */
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.left-panel.shrink {
  flex: 0 0 70%; /* 当右侧出现时，强制变 70% */
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-title {
  font-size: 18px;
  font-weight: bold;
}

/* 右侧面板 */
.right-panel {
  flex: 0 0 30%;
  min-width: 360px;        /* ✅ 保底宽度，防止看不到 */
  background: #fff;
  border-left: 1px solid #e4e7ed;
  padding: 20px;
  display: flex;
  flex-direction: column;
  box-shadow: -2px 0 10px rgba(0,0,0,0.05);
  overflow: auto;          /* ✅ 自己滚动，不靠父容器裁剪 */
}

.panel-header {
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}
.panel-form {
  flex: 1;
  overflow-y: auto; /* 内容过长可滚动 */
}
.panel-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 动画效果 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease-out;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>
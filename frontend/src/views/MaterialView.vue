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

    <!-- 右侧编辑区 -->
    <div class="right-panel" v-if="showEditor">
      <h3>{{ isEditMode ? '编辑模板' : '新增模板' }}</h3>
      <el-form label-position="top">
        <el-form-item label="模板名称">
          <el-input v-model="formData.name" placeholder="例如：小红书爆款种草" />
        </el-form-item>

        <el-form-item label="适用平台">
          <el-select v-model="formData.platform" placeholder="请选择平台">
            <el-option value="抖音" label="抖音" />
            <el-option value="小红书" label="小红书" />
            <el-option value="通用" label="通用" />
          </el-select>
        </el-form-item>

        <el-form-item label="Prompt 框架内容">
          <div class="tip">
            请务必包含以下所有占位符：<br>
            {identity}, {genre}, {time}, {platform}, {topic}, {keyword}, {style}, {emotion}, {length}
          </div>
          <el-input 
            type="textarea" 
            :rows="12" 
            v-model="formData.content" 
            placeholder="示例：你是一个{identity}，请以{emotion}的语气..." 
          />
        </el-form-item>

        <div class="panel-footer">
          <el-button type="primary" @click="handleSave">保存</el-button>
          <el-button @click="showEditor = false">取消</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.material-container {
  display: flex;
  height: calc(100vh - 60px);
  gap: 20px;
  overflow: hidden;
}
.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
}
.left-panel.shrink {
  flex: 0 0 60%;
}
.right-panel {
  flex: 1;
  background: #fff;
  border-left: 1px solid #eee;
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  box-shadow: -5px 0 10px rgba(0,0,0,0.05);
}
.top-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.tip {
  font-size: 12px;
  color: #E6A23C;
  margin-bottom: 5px;
  line-height: 1.5;
}
.panel-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
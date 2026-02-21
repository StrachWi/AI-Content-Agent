<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

import { useRouter } from 'vue-router'

const router = useRouter()

const handleSelect = (row) => {
  // 1️⃣ 存储选中的模板
  localStorage.setItem('selectedTemplate', JSON.stringify(row))

  // 2️⃣ 提示
  ElMessage.success(`已选用模板：${row.name}`)

  // 3️⃣ 跳转到生成页面
  router.push('/generate')
}


// ====== 后端 API 基地址（你的后端 main.py + CORS 已允许 5173）======
const API_BASE = 'http://127.0.0.1:8000/api/templates'

// --- 数据区 ---
const tableData = ref([])      // 从后端读
const loading = ref(false)

// 控制右侧编辑框显示
const showEditor = ref(false)
const isEditMode = ref(false)  // true编辑，false新增
const editingId = ref(null)    // 正在编辑的模板 id

// 表单数据（字段对齐后端：name/platform/content）
const formData = ref({
  name: '',
  platform: '',
  content: ''
})

// --- 工具：拉取列表 ---
const fetchList = async () => {
  loading.value = true
  try {
    const res = await axios.get(API_BASE)
    if (res.data.code !== 200) throw new Error(res.data.msg)
    tableData.value = res.data.data || []
  } catch (e) {
    ElMessage.error(e.message || '拉取模板列表失败')
  } finally {
    loading.value = false
  }
}

// --- 1. 点击新增 ---
const handleAdd = () => {
  isEditMode.value = false
  editingId.value = null
  formData.value = { name: '', platform: '', content: '' }
  showEditor.value = true
}


// --- 2. 点击编辑 ---
const handleEdit = (row) => {
  isEditMode.value = true
  editingId.value = row.id
  formData.value = {
    name: row.name,
    platform: row.platform,
    content: row.content
  }
  showEditor.value = true
}

// --- 3. 点击删除 ---
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该模板吗？', '提示', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })

    const res = await axios.delete(`${API_BASE}/${row.id}`)
    if (res.data.code !== 200) throw new Error(res.data.msg)

    ElMessage.success('删除成功')
    // 如果正在编辑被删的那条，顺便关掉编辑面板
    if (editingId.value === row.id) showEditor.value = false

    await fetchList()
  } catch (e) {
    // 用户点取消也会走 catch，不提示错误
  }
}

// --- 4. 保存（新增 or 编辑）---
const handleSave = async () => {
  // 基本校验（你们组要求：必须包含 {keyword}）
  //"{identity}","{genre}","{time}","{platform}","{topic}","{keyword}","{style}","{emotion}","{length}"
  if (!formData.value.name.trim()) return ElMessage.warning('模板名称必填')
  if (!formData.value.platform.trim()) return ElMessage.warning('适用平台必填')
  if (!formData.value.content.trim()) return ElMessage.warning('模板内容必填')
  if (!formData.value.content.includes('{identity}')) {
    return ElMessage.warning('模板内容必须包含{identity}占位符')
  }
  if (!formData.value.content.includes('{genre}')) {
    return ElMessage.warning('模板内容必须包含{genre}占位符')
  }  
  if (!formData.value.content.includes('{time}')) {
    return ElMessage.warning('模板内容必须包含{time}占位符')
  }
  if (!formData.value.content.includes('{platform}')) {
    return ElMessage.warning('模板内容必须包含{platform}占位符')
  }
  if (!formData.value.content.includes('{topic}')) {
    return ElMessage.warning('模板内容必须包含{topic}占位符')
  }
  if (!formData.value.content.includes('{keyword}')) {
    return ElMessage.warning('模板内容必须包含 {keyword} 占位符')
  }
  if (!formData.value.content.includes('{style}')) {
    return ElMessage.warning('模板内容必须包含{style}占位符')
  }
  if (!formData.value.content.includes('{emotion}')) {
    return ElMessage.warning('模板内容必须包含{emotion}占位符')
  }
  if (!formData.value.content.includes('{length}')) {
    return ElMessage.warning('模板内容必须包含{length}占位符')
  }

const handleSelect = (row) => {
  // TODO: 选中模板用于“文案生成”页面，可存 pinia / localStorage / 跳转并带参数
  ElMessage.success(`已选用模板：${row.name}`)
}


  try {
    if (isEditMode.value && editingId.value != null) {
      const res = await axios.put(`${API_BASE}/${editingId.value}`, formData.value)
      if (res.data.code !== 200) throw new Error(res.data.msg)
      ElMessage.success('修改成功')
    } else {
      const res = await axios.post(API_BASE, formData.value)
      if (res.data.code !== 200) throw new Error(res.data.msg)
      ElMessage.success('新增成功')
    }

    showEditor.value = false
    await fetchList()
  } catch (e) {
    ElMessage.error(e.message || '保存失败')
  }
}

// 页面加载自动拉取
onMounted(fetchList)
</script>


<template>
  <div class="material-container">
    
    <!-- 左侧：列表区 (根据 showEditor 动态调整宽度，或者始终占满由 flex 控制) -->
    <div class="left-panel" :class="{ 'shrink': showEditor }">
      
      <!-- 顶部操作区 -->
      <div class="top-bar">
        <span class="page-title">素材库管理</span>
        <div class="btn-group">
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon> 新增模板
          </el-button>
          <el-button type="primary" plain @click="fetchList">
            <el-icon><Refresh /></el-icon> 刷新列表
          </el-button>

        </div>
      </div>

      <!-- 表格列表 -->
      <el-table :data="tableData" style="width: 100%" stripe border>
        <el-table-column prop="name" label="模板名称" min-width="150" />
        <el-table-column prop="platform" label="适用平台" width="120">
          <template #default="scope">
            <el-tag>{{ scope.row.platform }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="create_time" label="创建时间" width="180" />

        <el-table-column label="操作" width="180" fixed="right">
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
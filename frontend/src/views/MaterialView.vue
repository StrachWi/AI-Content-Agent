<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox, ElDialog } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
// 🚀 核心修改：改为相对路径，让请求走 Vite 代理！
const API_BASE = '/api/templates'

// --- 数据区 ---
const tableData = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEditMode = ref(false)
const editingId = ref(null)

// 多选功能
const multipleSelection = ref([])
const selectable = (row, index) => {
  return true
}

const formData = ref({
  name: '',
  platform: '',
  content: ''
})

// 占位符列表
const placeholders = [
  { key: '{identity}', label: '身份', desc: '如：资深文案专家' },
  { key: '{genre}', label: '体裁', desc: '如：社交媒体文案' },
  { key: '{time}', label: '时间', desc: '如：近期' },
  { key: '{platform}', label: '平台', desc: '如：小红书' },
  { key: '{topic}', label: '主题', desc: '如：产品推广' },
  { key: '{keyword}', label: '关键词', desc: '如：新品上市' },
  { key: '{style}', label: '风格', desc: '如：吸引人' },
  { key: '{emotion}', label: '情感', desc: '如：积极' },
  { key: '{length}', label: '长度', desc: '如：200字左右' }
]

// --- 拉取列表 ---
const fetchList = async () => {
  loading.value = true
  try {
    const res = await axios.get(API_BASE)
    if (res.data.code !== 200) throw new Error(res.data.msg)
    tableData.value = res.data.data || []
    
    // 如果没有模板，添加默认模板
    if (tableData.value.length === 0) {
      await addDefaultTemplates()
    }
  } catch (e) {
    ElMessage.error('无法连接后端，请确认后端已启动: ' + e.message)
  } finally {
    loading.value = false
  }
}

// 添加默认模板
const addDefaultTemplates = async () => {
  // 先获取现有模板列表，用于去重
  let existingTemplates = []
  try {
    const res = await axios.get(API_BASE)
    if (res.data.code === 200) {
      existingTemplates = res.data.data || []
    }
  } catch (e) {
    console.error('获取现有模板失败:', e)
  }
  
  // 现有模板名称集合
  const existingTemplateNames = new Set(existingTemplates.map(t => t.name))
  
  const defaultTemplates = [
    {
      name: '小红书沉浸式种草',
      platform: '小红书',
      content: `# Role
你现在的身份是一名在【{platform}】拥有百万粉丝的【{identity}】。你的粉丝喜欢看真实、有生活感、像闺蜜聊天一样的分享。

# Context
现在的时间背景是【{time}】，当下的热门话题是【{topic}】。
请你创作一篇【{genre}】，篇幅控制在【{length}】。

# Product Info
核心推广的产品关键词/卖点如下：
【{keyword}】

# Requirements
1. 标题：必须包含“绝绝子”、“谁懂啊”、“救命”等抓眼球的词，且要带有数字或痛点。
2. 正文结构：
   - 痛点引入（用【{emotion}】的情绪开场）
   - 沉浸式体验/产品亮点介绍
   - 结尾强力安利
3. 风格要求：语言风格要【{style}】，每一段都要大量使用 Emoji 表情符号，增加视觉吸引力。
4. 标签：文末自动生成 5 个相关的 Hashtag。`
    },
    {
      name: '短视频剧情脚本',
      platform: '抖音',
      content: `# Role
你是一名专业的短视频编剧/导演，擅长通过镜头语言和反转剧情吸引观众。你的身份设定是【{identity}】。

# Task
请为【{platform}】平台写一个【{genre}】。
核心主题是【{topic}】，针对的时间节点是【{time}】。

# Key Elements
视频的核心卖点/植入信息：
【{keyword}】

# Constraints
1. 整体基调：【{emotion}】且【{style}】。
2. 视频时长预估：【{length}】。
3. 输出格式：请严格按照“分镜头脚本”格式输出，包含以下列：
   - 镜号
   - 景别（全景/近景/特写）
   - 画面描述（详细动作）
   - 台词/旁白
   - 背景音乐建议
请确保开头前 3 秒有黄金 3 秒的吸睛点。`
    },
    {
      name: '高转化痛点营销',
      platform: '通用/朋友圈',
      content: `# Role 你是一名资深的【{identity}】，也是一名心理学营销专家。你非常擅长挖掘用户痛点并提供解决方案。

# Goal
请撰写一篇【{genre}】，发布在【{platform}】。
主题围绕【{topic}】，结合【{time}】的季节/节日特性。

# Input
产品核心卖点：
【{keyword}】

# Writing Strategy (PAS Model)
请严格按照 PAS (Problem-Agitation-Solution) 模型写作：
1. P (提出问题)：用【{emotion}】的语气指出用户当前面临的烦恼。
2. A (放大痛苦)：描述如果不解决这个问题会有什么后果。
3. S (提出方案)：自然地引出产品，用【{style}】的语言描述产品如何完美解决上述问题。

篇幅要求：【{length}】。`
    },
    {
      name: '专业深度测评/科普',
      platform: '知乎/公众号',
      content: `# Role 你是一名行业内的权威【{identity}】，你的说话风格【{style}】，讲究数据和逻辑，拒绝情绪化表达。

# Task
请针对话题【{topic}】，写一篇深度的【{genre}】发布于【{platform}】。
文章需要结合【{time}】的最新趋势。

# Keywords
核心分析对象/关键词：
【{keyword}】

# Requirements
1. 结构清晰：使用 Markdown 格式，包含一级标题、二级标题。
2. 内容深度：不要流于表面，需要分析背后的原理、成分或市场逻辑。
3. 情感控制：保持【{emotion}】（建议为客观冷静），用事实说话。
4. 篇幅：【{length}】。
5. 在文章最后，给出一个简短的“太长不看版(TL;DR)”总结。`
    }
  ]
  
  for (const template of defaultTemplates) {
    // 检查是否已存在相同名称的模板
    if (!existingTemplateNames.has(template.name)) {
      try {
        await axios.post(API_BASE, template)
      } catch (e) {
        console.error('添加默认模板失败:', e)
      }
    }
  }
  
  // 重新拉取列表
  await fetchList()
}

// 重置默认模板
const resetDefaultTemplates = async () => {
  try {
    await ElMessageBox.confirm('确定要重置默认模板吗？这将会添加所有默认模板（不会删除现有模板）', '提示', { 
      type: 'warning',
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    
    await addDefaultTemplates()
    ElMessage.success('默认模板重置成功')
  } catch (e) {
    // 用户取消操作
  }
}

// --- 操作逻辑 ---
const handleAdd = () => {
  isEditMode.value = false
  editingId.value = null
  formData.value = { name: '', platform: '', content: '' }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEditMode.value = true
  editingId.value = row.id
  formData.value = { name: row.name, platform: row.platform, content: row.content }
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该模板吗？', '提示', { type: 'warning' })
    const res = await axios.delete(`${API_BASE}/${row.id}`)
    if (res.data.code === 200) {
      ElMessage.success('删除成功')
      
      // 检查并清除本地存储中的模板信息
      const selectedTemplateStr = localStorage.getItem('selectedTemplate')
      if (selectedTemplateStr) {
        const selectedTemplate = JSON.parse(selectedTemplateStr)
        if (selectedTemplate.id === row.id) {
          localStorage.removeItem('selectedTemplate')
        }
      }
      
      fetchList()
    }
  } catch (e) {}
}

// 多选删除
const handleBatchDelete = async () => {
  if (multipleSelection.value.length === 0) {
    return ElMessage.warning('请先选择要删除的模板')
  }

  try {
    await ElMessageBox.confirm(`确认删除选中的 ${multipleSelection.value.length} 个模板吗？`, '提示', { type: 'warning' })
    
    // 批量删除
    const deletePromises = multipleSelection.value.map(row => 
      axios.delete(`${API_BASE}/${row.id}`)
    )
    
    await Promise.all(deletePromises)
    ElMessage.success('批量删除成功')
    
    // 检查并清除本地存储中的模板信息
    const selectedTemplateStr = localStorage.getItem('selectedTemplate')
    if (selectedTemplateStr) {
      const selectedTemplate = JSON.parse(selectedTemplateStr)
      const isSelectedDeleted = multipleSelection.value.some(row => row.id === selectedTemplate.id)
      if (isSelectedDeleted) {
        localStorage.removeItem('selectedTemplate')
      }
    }
    
    multipleSelection.value = []
    fetchList()
  } catch (e) {}
}

// 处理多选变化
const handleSelectionChange = (val) => {
  multipleSelection.value = val
}

const handleSelect = (row) => {
  // 存储选中的模板，供生成页面使用
  localStorage.setItem('selectedTemplate', JSON.stringify(row))
  ElMessage.success(`已选用：${row.name}`)
  router.push('/generate')
}

// 插入占位符
const insertPlaceholder = (placeholder) => {
  formData.value.content += placeholder
}

const handleSave = async () => {
  // 1. 基础非空校验
  if (!formData.value.name.trim()) return ElMessage.warning('模板名称必填')
  if (!formData.value.platform.trim()) return ElMessage.warning('适用平台必填')
  if (!formData.value.content.trim()) return ElMessage.warning('模板内容必填')
  
  // 2. 名称唯一性校验
  try {
    const res = await axios.get(API_BASE)
    if (res.data.code === 200) {
      const existingTemplates = res.data.data || []
      const isNameExists = existingTemplates.some(t => 
        t.name === formData.value.name && t.id !== editingId.value
      )
      if (isNameExists) {
        return ElMessage.warning('模板名称已存在，请使用其他名称')
      }
    }
  } catch (e) {
    console.error('检查模板名称失败:', e)
  }

  // 3. 占位符校验：至少包含一个
  const requiredTags = [
    '{identity}', '{genre}', '{time}', '{platform}', 
    '{topic}', '{keyword}', '{style}', '{emotion}', '{length}'
  ]
  
  const hasAnyTag = requiredTags.some(tag => formData.value.content.includes(tag))
  
  if (!hasAnyTag) {
    return ElMessage.error('模板内容必须至少包含一个占位符（如 {identity}、{topic} 等）')
  }

  // 3. 发送请求
  try {
    if (isEditMode.value) {
      await axios.put(`${API_BASE}/${editingId.value}`, formData.value)
    } else {
      await axios.post(API_BASE, formData.value)
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
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
    <div class="left-panel" :class="{ 'shrink': showEditor }">
      <div class="top-bar">
        <span class="page-title">素材库管理</span>
        <div class="btn-group">
          <el-button type="primary" @click="handleAdd">新增模板</el-button>
          <el-button type="danger" @click="handleBatchDelete" :disabled="multipleSelection.length === 0">批量删除</el-button>
          <el-button type="warning" @click="resetDefaultTemplates">重置默认模板</el-button>
          <el-button @click="fetchList">刷新列表</el-button>
        </div>
      </div>

      <el-table 
        :data="tableData" 
        style="width: 100%" 
        stripe 
        border 
        v-loading="loading"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" :selectable="selectable" />
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

    <el-dialog
      v-model="dialogVisible"
      :title="isEditMode ? '编辑模板' : '新增模板'"
      width="80%"
      center
      draggable
    >
      <div class="editor-container">
        <div class="editor-form">
          <el-form label-position="top" class="panel-form">
            <el-form-item label="模板名称 (必填)">
              <el-input v-model="formData.name" placeholder="如：开学季笔记本推广" />
            </el-form-item>

            <el-form-item label="适用平台">
              <el-select v-model="formData.platform" placeholder="请选择平台">
                <el-option label="抖音" value="抖音" />
                <el-option label="小红书" value="小红书" />
                <el-option label="知乎" value="知乎" />
                <el-option label="朋友圈" value="朋友圈" />
                <el-option label="公众号" value="公众号" />
                <el-option label="通用" value="通用" />
              </el-select>
            </el-form-item>

            <el-form-item label="模板框架内容">
              <el-input 
                v-model="formData.content" 
                type="textarea" 
                :rows="12" 
                placeholder="请在这里输入模板框架，至少要包含一个关键词（关键词由“{}”包含）。示例：“你是一名{platform}的博主，要发布一则主题为{topic}的帖子，请写出一篇合适的文案，情感要求为{emotion}，字数要求为{length}。”" 
              />
            </el-form-item>
          </el-form>
        </div>
        
        <div class="placeholder-sidebar">
          <h4>可选关键词</h4>
          <div class="placeholder-list">
            <el-button 
              v-for="placeholder in placeholders" 
              :key="placeholder.key"
              type="primary"
              size="small"
              plain
              @click="insertPlaceholder(placeholder.key)"
              class="placeholder-btn"
            >
              {{ placeholder.key }}
            </el-button>
          </div>
          <div class="placeholder-hints">
            <ul>
              <li v-for="placeholder in placeholders" :key="placeholder.key">
                {{ placeholder.key }}：{{ placeholder.label }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSave">保存</el-button>
        </div>
      </template>
    </el-dialog>

  </div>
</template>

<style scoped>
.material-container {
  display: flex;
  height: calc(100vh - 60px); /* 让容器有稳定高度（header 60px） */
  gap: 20px;
  overflow: visible;         /* ✅ 不裁剪右侧面板动画 */
}


.left-panel {
  flex: 1;
  min-width: 0;           /* ✅ 防止 el-table 宽度撑破 flex 布局 */
  display: flex;
  flex-direction: column;
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
/* 右侧面板样式已移除，改为使用对话框 */

.editor-container {
  display: flex;
  gap: 20px;
  flex: 1;
  overflow: hidden;
}

.editor-form {
  flex: 1;
  overflow-y: auto;
}

.placeholder-sidebar {
  width: 200px;
  background-color: #f9f9f9;
  padding: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  overflow-y: auto;
}

.placeholder-sidebar h4 {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 15px;
  color: #303133;
}

.placeholder-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
  align-items: flex-start;
  padding-left: 8px;
}

.placeholder-btn {
  text-align: center;
  font-size: 12px;
  /* 调整内边距，让按钮更美观 */
  padding: 10px 15px;
  border-radius: 6px; /* 圆角更柔和 */
  /* 统一宽度：适配父容器（减去内边距），所有按钮宽度一致 */
  width: calc(100% - 16px);
  box-sizing: border-box;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  border: 1px solid #dcdfe6;
  transition: all 0.3s ease;
  /* 移除居中相关属性，确保左对齐 */
  margin: 0;
}

.placeholder-btn:hover {
  border-color: #409eff;
  color: #409eff;
}

.placeholder-hints {
  margin-top: 15px;
}

.placeholder-hints ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.placeholder-hints li {
  font-size: 12px;
  line-height: 1.5;
  margin-bottom: 4px;
  color: #606266;
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

/* 动画效果已移除，改为使用对话框的默认动画 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.custom-label {
  line-height: 1.5;
  font-weight: 500;
}
.keywords-hint {
  font-size: 12px;
  font-weight: normal;
  color: #606266;
  display: inline-block;
  margin-top: 4px;
  line-height: 1.4;
}
</style>
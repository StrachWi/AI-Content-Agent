<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'


// --- 状态 ---
const isLoading = ref(false)
const hasResult = ref(false)
const isEdit = ref(false)

// 【修改点1】扩充 inputData，加入新增的 8 个维度，给个默认值方便演示
const inputData = ref({
  template: '', // 保持不变：只存模板名称用于展示
  keywords: '', // 保持不变：核心需求
  
  // --- 新增的 8 个“钉子”参数 ---
  identity: '资深博主',
  genre: '种草文案',
  time: '当下',
  platform: '小红书',
  topic: '好物推荐',
  style: '真诚',
  emotion: '激动',
  length: '200字左右'
})

const STORAGE_KEY = 'generate_page_data'

// 新增：保存所有数据到 localStorage
const saveAllData = () => {
  const dataToSave = {
    inputData: { ...inputData.value },
    resultData: { ...resultData.value },
    hasResult: hasResult.value,
    isEdit: isEdit.value
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(dataToSave))
  console.log('数据已保存到 localStorage')
}

// 新增：从 localStorage 恢复数据
const restoreData = () => {
  const savedStr = localStorage.getItem(STORAGE_KEY)
  if (savedStr) {
    try {
      const savedData = JSON.parse(savedStr)
      
      // 恢复输入参数（避免覆盖模板名）
      if (savedData.inputData) {
        const currentTemplate = inputData.value.template
        inputData.value = { ...savedData.inputData }
        // 保持模板名不被覆盖
        if (currentTemplate) {
          inputData.value.template = currentTemplate
        }
      }
      
      // 恢复结果数据
      if (savedData.resultData) {
        resultData.value = { ...savedData.resultData }
      }
      
      // 恢复状态
      if (savedData.hasResult !== undefined) {
        hasResult.value = savedData.hasResult
      }
      if (savedData.isEdit !== undefined) {
        isEdit.value = savedData.isEdit
      }
      
      console.log('数据已从 localStorage 恢复')
    } catch (error) {
      console.error('恢复数据失败:', error)
      localStorage.removeItem(STORAGE_KEY) // 清理损坏的数据
    }
  }
}

const resultData = ref({
  douyin: '',
  redbook: ''
})

// --- 初始化 ---
onMounted(() => {
  const templateStr = localStorage.getItem('selectedTemplate')
  if (templateStr) {
    const template = JSON.parse(templateStr)
    // 自动回填模板名称
    inputData.value.template = template.name
    
    // 如果模板里自带了平台属性，自动填入 platform 字段
    if (template.platform) inputData.value.platform = template.platform
    
    ElMessage.success(`已自动加载模板：${template.name}`)
  }
  
  // 新增：恢复保存的数据
  restoreData()
})
import { watch } from 'vue'

// 监听 inputData 的变化（深度监听）
watch(
  () => ({ ...inputData.value }), // 使用展开操作符创建新对象触发监听
  (newVal, oldVal) => {
    // 延迟保存，避免频繁操作
    setTimeout(() => {
      saveAllData()
    }, 500)
  },
  { deep: true }
)

// 监听 resultData 的变化
watch(
  () => ({ ...resultData.value }),
  () => {
    setTimeout(() => {
      saveAllData()
    }, 500)
  },
  { deep: true }
)

// 监听状态变化
watch([hasResult, isEdit], () => {
  setTimeout(() => {
    saveAllData()
  }, 500)
})

// --- 逻辑 ---
const handleGenerate = async () => {
  if (!inputData.value.template) {
    ElMessage.warning('请先去素材库选用一个模板')
    return
  }
  
  if (!inputData.value.keywords || inputData.value.keywords.trim() === '') {
    ElMessage.warning('请填写核心关键词/需求')
    return
  }
  inputData.value.topic = inputData.value.keywords;
  isLoading.value = true
  hasResult.value = false
  
  try {
    // 从 localStorage 获取模板ID
    const templateStr = localStorage.getItem('selectedTemplate')
    const template = templateStr ? JSON.parse(templateStr) : {}
    
    if (!template.id) {
      ElMessage.error('模板信息不完整，请重新选择模板')
      isLoading.value = false
      return
    }
    
    // 准备请求数据
    const requestData = {
      template_id: template.id,
      keyword: inputData.value.keywords,  // 注意：后端是 keyword，不是 keywords
      identity: inputData.value.identity,
      genre: inputData.value.genre,
      time: inputData.value.time,
      platform: inputData.value.platform,
      topic: inputData.value.topic,
      style: inputData.value.style,
      emotion: inputData.value.emotion,
      length: inputData.value.length
    }
    
    console.log('发送给后端的数据:', JSON.stringify(requestData, null, 2))
    
    // 使用 fetch 调用后端API
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 70000)  // 70秒超时
    
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
      signal: controller.signal
    })
    
    clearTimeout(timeoutId)
    
    console.log('响应状态:', response.status, response.statusText)
    
    // 检查响应状态
    if (!response.ok) {
      let errorMsg = `HTTP ${response.status}: ${response.statusText}`
      try {
        const errorData = await response.json()
        errorMsg = errorData.msg || errorData.message || errorMsg
      } catch (e) {
        // 无法解析JSON错误信息
      }
      throw new Error(errorMsg)
    }
    
    // 解析响应数据
    const responseData = await response.json()
    console.log('后端响应:', responseData)
    
    // 处理响应
    if (responseData && responseData.code === 200) {
  const data = responseData.data
  
  // 后端只返回一个 result，先显示相同的内容
  resultData.value.douyin = data.result
  resultData.value.redbook = data.result  // 暂时显示相同内容
  
  hasResult.value = true
  ElMessage.success('文案生成成功！')
  
  // 新增：立即保存数据
  saveAllData()
  
  // 可选：保存历史记录ID
  if (data.history_id) {
    console.log('历史记录ID:', data.history_id)
  }
}else {
      // 处理业务错误
      const errorMsg = responseData?.msg || '生成失败，请稍后重试'
      ElMessage.error(errorMsg)
    }
    
  } catch (error) {
    // 处理错误
    console.error('API调用失败:', error)
    
    // 判断错误类型
    if (error.name === 'AbortError') {
      ElMessage.error('请求超时，请稍后重试')
    } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      ElMessage.error('网络连接失败，请检查: 1. 后端服务是否启动 2. 网络连接')
    } else if (error.message.includes('HTTP')) {
      // 之前抛出的HTTP错误
      ElMessage.error(error.message)
    } else {
      ElMessage.error('请求错误: ' + error.message)
    }
  }finally {
    // 无论成功或失败，都结束加载状态
    isLoading.value = false
    }
}
const clearSavedData = () => {
  localStorage.removeItem(STORAGE_KEY)
  // 重置表单（但保留模板）
  const currentTemplate = inputData.value.template
  inputData.value = {
    template: currentTemplate,
    keywords: '',
    identity: '资深博主',
    genre: '种草文案',
    time: '当下',
    platform: '小红书',
    topic: '',
    style: '真诚',
    emotion: '激动',
    length: '200字左右'
  }
  resultData.value = { douyin: '', redbook: '' }
  hasResult.value = false
  isEdit.value = false
  ElMessage.success('已清空所有输入和结果')
}
const copyText = (text) => {
  navigator.clipboard.writeText(text)
  ElMessage.success('已复制到剪贴板')
}

// 保存文案到历史记录
const saveContent = async () => {
  if (!resultData.value.redbook) {
    ElMessage.warning('没有可保存的文案')
    return
  }
  
  try {
    const templateStr = localStorage.getItem('selectedTemplate')
    const template = templateStr ? JSON.parse(templateStr) : {}
    
    const response = await axios.post('/api/history', {
      topic: inputData.value.keywords,
      platform: inputData.value.platform,
      content: resultData.value.redbook,
      template_name: template.name || '未知模板'
    })
    
    if (response.data.code === 200) {
      ElMessage.success('文案已保存到历史记录')
    } else {
      ElMessage.error('保存失败，请稍后重试')
    }
  } catch (error) {
    ElMessage.error('网络错误，请检查后端服务是否启动')
    console.error('Error saving content:', error)
  }
}
</script>

<template>
  <div class="generate-container">
    
    <!-- 1. 顶部模板信息 (保持不变) -->
    <div class="section-card">
      <div class="section-title">Step 1: 确认模板</div>
      <div class="form-row">
        <span class="label">当前使用模板：</span>
        <el-input 
          v-model="inputData.template" 
          disabled 
          placeholder="请前往素材库选用模板" 
          style="width: 300px" 
        />
        <el-link type="primary" class="ml-20" href="/material">去素材库更换模板</el-link>
      </div>
    </div>

    <!-- 2. 中部输入区 (【修改点2】布局升级) -->
    <div class="section-card mt-20">
      <div class="section-title">Step 2: 定义参数 (AI 指令)</div>
      
      <!-- 新增：8个参数的网格布局 -->
      <div class="params-grid">
        <el-form-item label="身份设定">
          <el-input v-model="inputData.identity" placeholder="如：美妆博主" />
        </el-form-item>
        <el-form-item label="发布平台">
          <el-select v-model="inputData.platform" style="width: 100%">
            <el-option value="小红书" label="小红书" />
            <el-option value="抖音" label="抖音" />
            <el-option value="知乎" label="知乎" />
          </el-select>
        </el-form-item>
        <el-form-item label="文案体裁">
          <el-input v-model="inputData.genre" placeholder="如：脚本/笔记" />
        </el-form-item>
        <el-form-item label="核心话题">
          <el-input v-model="inputData.topic" placeholder="如：好物分享" />
        </el-form-item>
        <el-form-item label="语言风格">
          <el-input v-model="inputData.style" placeholder="如：幽默/专业" />
        </el-form-item>
        <el-form-item label="情感基调">
          <el-input v-model="inputData.emotion" placeholder="如：激动/客观" />
        </el-form-item>
        <el-form-item label="篇幅长度">
          <el-input v-model="inputData.length" placeholder="如：200字" />
        </el-form-item>
        <el-form-item label="时间背景">
          <el-input v-model="inputData.time" placeholder="如：当下/开学季" />
        </el-form-item>
      </div>

      <!-- 原有的大输入框 (保持不变，加了点间距) -->
      <div class="big-input-area">
        <div class="label-text">核心关键词 / 需求 (Keywords):</div>
        <el-input
          v-model="inputData.keywords"
          type="textarea"
          :rows="4"
          placeholder="输入产品的具体卖点、参数、要求，如：开学季、笔记本电脑、轻薄..."
        />
      </div>

      <div class="btn-area">
        <el-button type="primary" size="large" :loading="isLoading" @click="handleGenerate">
          {{ isLoading ? 'AI 正在思考中...' : '一键生成文案' }}
        </el-button>
      </div>
    </div>

    <!-- 3. 结果展示区 (保持不变) -->
<div class="section-card mt-20" v-if="hasResult">
  
  <!-- 直接显示内容，不用标签页 -->
  <div class="result-header">
    <h3>AI生成文案</h3>
    <div class="btn-group">
      <el-button size="small" @click="isEdit = !isEdit">{{ isEdit ? '保存修改' : '编辑' }}</el-button>
    </div>
  </div>
  <el-input type="textarea" v-model="resultData.redbook" :readonly="!isEdit" :rows="8" />

      <!-- 底部操作栏 -->
      <div class="result-actions">
        <el-button type="primary" @click="saveContent">保存文案</el-button>
        <el-button type="success" @click="copyText(resultData.douyin)">复制抖音文案</el-button>
        <el-button type="success" @click="copyText(resultData.redbook)">复制小红书文案</el-button>
        <el-button plain @click="handleGenerate">重新生成</el-button>
      </div>
      <div class="btn-area">
    <el-button type="primary" size="large" :loading="isLoading" @click="handleGenerate">
      {{ isLoading ? 'AI 正在思考中...' : '一键生成文案' }}
    </el-button>
    <el-button type="default" size="large" @click="clearSavedData" style="margin-left: 10px;">
      清空重填
    </el-button>
  </div>
    </div>

  </div>
</template>

<style scoped>
.generate-container {
  max-width: 900px;
  margin: 0 auto;
  padding-bottom: 50px; /* 底部留白 */
}
.section-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05); /*稍微加点阴影好看*/
}
.mt-20 { margin-top: 20px; }
.ml-20 { margin-left: 20px; }
.section-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 20px;
  border-left: 4px solid #409EFF; /* 加个蓝条装饰 */
  padding-left: 10px;
}
.section-title.small { font-size: 14px; }
.form-row { display: flex; align-items: center; }
.label { margin-right: 12px; font-weight: bold; }
.btn-area { margin-top: 30px; text-align: center; } /* 增加间距 */
.result-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
.result-actions { margin-top: 20px; display: flex; justify-content: flex-end; gap: 10px; }

/* 【修改点3】新增网格布局样式 */
.params-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 一行4个 */
  gap: 20px;
  margin-bottom: 20px;
}
.big-input-area {
  margin-top: 20px;
  border-top: 1px dashed #eee; /* 加个虚线分隔 */
  padding-top: 20px;
}
.label-text {
  font-weight: bold;
  margin-bottom: 8px;
  font-size: 14px;
}
</style>
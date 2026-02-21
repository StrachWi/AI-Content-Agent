<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

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

const resultData = ref({
  douyin: '',
  redbook: ''
})

// --- 初始化：逻辑保持不变 ---
onMounted(() => {
  const templateStr = localStorage.getItem('selectedTemplate')
  if (templateStr) {
    const template = JSON.parse(templateStr)
    // 自动回填模板名称
    inputData.value.template = template.name
    
    // (可选优化) 如果模板里自带了平台属性，自动填入 platform 字段
    if (template.platform) inputData.value.platform = template.platform
    
    ElMessage.success(`已自动加载模板：${template.name}`)
  }
})

// --- 逻辑 ---
const handleGenerate = () => {
  if (!inputData.value.template) return ElMessage.warning('请先去素材库选用一个模板')
  
  isLoading.value = true
  
  // TODO: 3组同学请注意！
  // 你们接入 API 时，发送给后端的参数应该是 inputData.value 的全部内容
  // 包含：template_id, keywords, identity, genre, time... 等等
  
  // 模拟效果 (保持你的逻辑不变，只是让结果更丰富一点，证明参数生效了)
  setTimeout(() => {
    isLoading.value = false
    hasResult.value = true
    
    // 模拟结果
    resultData.value.douyin = `【抖音脚本】\n身份设定：${inputData.value.identity}\n场景：${inputData.value.keywords}\n风格：${inputData.value.style}\n(这是模拟结果)...`
    resultData.value.redbook = `【小红书文案】\n发布平台：${inputData.value.platform}\n标题：${inputData.value.keywords} 绝绝子！\n情感基调：${inputData.value.emotion}\n(这是模拟结果)...`
  }, 2000)
}

const copyText = (text) => {
  navigator.clipboard.writeText(text)
  ElMessage.success('已复制到剪贴板')
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
      <el-tabs type="border-card">
        <el-tab-pane label="抖音版">
          <div class="result-header">
            <h3>抖音适配文案</h3>
            <el-button size="small" @click="isEdit = !isEdit">{{ isEdit ? '保存修改' : '编辑' }}</el-button>
          </div>
          <el-input type="textarea" v-model="resultData.douyin" :readonly="!isEdit" :rows="8" />
        </el-tab-pane>

        <el-tab-pane label="小红书版">
          <div class="result-header">
            <h3>小红书适配文案</h3>
            <div class="btn-group">
               <el-button size="small" @click="isEdit = !isEdit">{{ isEdit ? '保存修改' : '编辑' }}</el-button>
            </div>
          </div>
          <el-input type="textarea" v-model="resultData.redbook" :readonly="!isEdit" :rows="8" />
        </el-tab-pane>
      </el-tabs>

      <!-- 底部操作栏 -->
      <div class="result-actions">
        <el-button type="primary">保存文案</el-button>
        <el-button type="success" @click="copyText(resultData.douyin)">复制抖音文案</el-button>
        <el-button type="success" @click="copyText(resultData.redbook)">复制小红书文案</el-button>
        <el-button plain @click="handleGenerate">重新生成</el-button>
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
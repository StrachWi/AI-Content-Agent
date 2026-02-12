<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

// --- 状态 ---
const isLoading = ref(false)
const hasResult = ref(false) // 是否生成了结果

const inputData = ref({
  template: '',
  keywords: ''
})

const resultData = ref({
  douyin: '',
  redbook: ''
})

// --- 逻辑 ---
const handleGenerate = () => {
  if (!inputData.value.template) return ElMessage.warning('请先选择模板')
  
  isLoading.value = true
  
  // 模拟 AI 生成过程 (2秒延迟)
  setTimeout(() => {
    isLoading.value = false
    hasResult.value = true
    
    // 模拟结果
    resultData.value.douyin = `【抖音脚本】\n场景：${inputData.value.keywords}\n1. 镜头切入...\n2. 主角展示...`
    resultData.value.redbook = `【小红书文案】\n标题：${inputData.value.keywords} 绝绝子！\n正文：家人们谁懂啊... #好物分享`
  }, 2000)
}

const copyText = (text) => {
  navigator.clipboard.writeText(text)
  ElMessage.success('已复制到剪贴板')
}
</script>

<template>
  <div class="generate-container">
    
    <!-- 1. 顶部模板选择区 -->
    <div class="section-card">
      <div class="section-title">内容智能生成</div>
      <div class="form-row">
        <span class="label">选择模板：</span>
        <el-select v-model="inputData.template" placeholder="请选择创作模板" style="width: 300px">
          <el-option label="抖音产品推广" value="douyin" />
          <el-option label="小红书种草" value="redbook" />
        </el-select>
        <el-link type="primary" class="ml-20" href="/material">去素材库创建模板</el-link>
      </div>
    </div>

    <!-- 2. 中部输入区 -->
    <div class="section-card mt-20">
      <div class="section-title small">创作需求输入</div>
      <el-input
        v-model="inputData.keywords"
        type="textarea"
        :rows="5"
        placeholder="输入核心关键词 / 需求，如：开学季、笔记本电脑、轻薄、长续航、学生党..."
      />
      <div class="btn-area">
        <el-button type="primary" size="large" :loading="isLoading" @click="handleGenerate">
          {{ isLoading ? 'AI 正在思考中...' : '一键生成文案' }}
        </el-button>
      </div>
    </div>

    <!-- 3. 底部生成结果展示区 (默认隐藏，生成后显示) -->
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
            <el-button size="small">编辑</el-button>
          </div>
          <el-input type="textarea" v-model="resultData.redbook" readonly :rows="8" />
        </el-tab-pane>
      </el-tabs>

      <!-- 底部操作栏 -->
      <div class="result-actions">
        <el-button type="primary">保存文案</el-button>
        <el-button type="success" @click="copyText(resultData.douyin)">导出/复制文案</el-button>
        <el-button plain @click="handleGenerate">重新生成</el-button>
      </div>
    </div>

  </div>
</template>

<style scoped>
.generate-container {
  max-width: 900px;
  margin: 0 auto; /* 居中显示 */
}

.section-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  /* box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05); */
}
.mt-20 { margin-top: 20px; }
.ml-20 { margin-left: 20px; }

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
}
.section-title.small {
  font-size: 14px;
}

.form-row {
  display: flex;
  align-items: center;
}
.label {
  margin-right: 12px;
  font-weight: bold;
}

.btn-area {
  margin-top: 20px;
  text-align: center;
}

.result-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}
.result-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
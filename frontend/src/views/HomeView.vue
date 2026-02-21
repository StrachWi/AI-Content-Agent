<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

// 快捷跳转
const go = (path) => {
  router.push(path)
}
</script>

<template>
  <div class="home-container">
    <!-- 上半区：工具价值说明 -->
    <div class="hero-section">
      <h1 class="hero-title">AI 营销文案一键生成</h1>
      <p class="hero-subtitle">选模板 · 输关键词 · 生成适配抖音/小红书的营销文案</p>
      <span class="hero-desc">无需从零创作，提升营销内容产出效率</span>
    </div>

    <!-- 下半区：3个快捷功能按钮 -->
    <div class="action-section">
      <!-- 按钮1：进入素材库 -->
      <div class="action-card" @click="go('/material')">
        <el-button type="primary" plain class="action-btn" size="large">
          进入素材库
        </el-button>
      </div>

      <!-- 按钮2：开始创作 (高亮) -->
      <div class="action-card" @click="go('/generate')">
        <el-button type="primary" class="action-btn highlight-btn" size="large">
          开始创作
        </el-button>
      </div>

      <!-- 按钮3：查看创作记录 -->
      <div class="action-card" @click="go('/history')">
        <el-button type="info" plain class="action-btn" size="large">
          查看创作记录
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 60px; /* 上下间距 */
}

/* 上半区文字 */
.hero-section {
  text-align: center;
}
.hero-title {
  font-size: 32px; /* 稍微大一点更好看，文档说20px可能太小，可调整 */
  font-weight: bold;
  color: #303133;
  margin-bottom: 16px;
}
.hero-subtitle {
  font-size: 16px;
  color: #606266;
  margin-bottom: 12px;
}
.hero-desc {
  font-size: 12px;
  color: #909399;
}

/* 下半区按钮 */
.action-section {
  display: flex;
  gap: 40px;
}
.action-btn {
  width: 160px;
  height: 50px;
  font-size: 16px;
}
.highlight-btn {
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4); /* 增加一点高亮阴影 */
}
</style>
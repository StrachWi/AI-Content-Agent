<script setup>
import { RouterView, useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <div class="app-layout">
    <el-container class="full-height">
      
      <!-- 1. 侧边栏 (200px, 浅灰色) -->
      <el-aside width="200px" class="app-aside">
        <div class="logo-area">
          <el-icon size="24" color="#409EFF"><ChromeFilled /></el-icon>
          <span style="margin-left: 8px; font-weight: bold;">AI 营销助手</span>
        </div>

        <el-menu
          :default-active="route.path"
          router
          class="el-menu-vertical"
          background-color="#f5f7fa"
        >
          <!-- 首页 -->
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>工作台</span>
          </el-menu-item>
          
          <!-- 素材库 -->
          <el-menu-item index="/material">
            <el-icon><Folder /></el-icon>
            <span>素材库管理</span>
          </el-menu-item>
          
          <!-- 智能生成 -->
          <el-menu-item index="/generate">
            <el-icon><EditPen /></el-icon>
            <span>内容智能生成</span>
          </el-menu-item>
          
          <!-- 创作记录 -->
          <el-menu-item index="/history">
            <el-icon><Document /></el-icon>
            <span>创作记录中心</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 2. 右侧主体 -->
      <el-container>
        <!-- 顶部 Header -->
        <el-header class="app-header">
          <h2 class="header-title">AI 营销内容创作助手</h2>
        </el-header>

        <!-- 内容区域 -->
        <el-main class="app-main">
          <RouterView />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.app-layout {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
.full-height {
  height: 100%;
}

/* 侧边栏样式 */
.app-aside {
  background-color: #f5f7fa; /* 浅灰色背景 */
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.logo-area {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e4e7ed;
  color: #303133;
}

.el-menu-vertical {
  border-right: none;
  background-color: transparent;
}

/* 顶部 Header 样式 */
.app-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: center; /* 字体居中 */
  height: 60px;
}
.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  letter-spacing: 1px;
}

/* 主内容区 */
.app-main {
  background-color: #ffffff;
  padding: 24px;
}
</style>
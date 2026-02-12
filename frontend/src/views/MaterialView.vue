<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// --- 数据区 ---
const tableData = ref([
  { id: 1, name: '抖音产品推广模板', type: '抖音', time: '2023-10-01' },
  { id: 2, name: '小红书种草模板', type: '小红书', time: '2023-10-05' },
  { id: 3, name: '活动宣传通用', type: '通用', time: '2023-10-10' },
])

// 控制右侧编辑框显示
const showEditor = ref(false)
const isEditMode = ref(false) // true为编辑，false为新增

// 表单数据
const formData = ref({
  name: '',
  type: '',
  content: ''
})

// --- 交互逻辑 ---
// 1. 点击新增
const handleAdd = () => {
  isEditMode.value = false
  formData.value = { name: '', type: '', content: '' } // 重置表单
  showEditor.value = true
}

// 2. 点击编辑
const handleEdit = (row) => {
  isEditMode.value = true
  // 模拟回填数据
  formData.value = { 
    name: row.name, 
    type: row.type, 
    content: '这是模拟的模板内容框架...' 
  } 
  showEditor.value = true
}

// 3. 点击删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该模板吗？', '提示', {
    confirmButtonText: '删除',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    ElMessage.success('删除成功')
    // 这里写删除逻辑...
  })
}

// 4. 保存
const handleSave = () => {
  ElMessage.success(isEditMode.value ? '修改成功' : '新增成功')
  showEditor.value = false
}
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
          <el-button type="danger" plain>
            <el-icon><Delete /></el-icon> 刷新列表
          </el-button>
        </div>
      </div>

      <!-- 表格列表 -->
      <el-table :data="tableData" style="width: 100%" stripe border>
        <el-table-column prop="name" label="模板名称" min-width="150" />
        <el-table-column prop="type" label="模型类型" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.type === '抖音' ? '' : 'warning'">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="time" label="创建时间" width="150" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(scope.row)">删除</el-button>
            <el-button link type="success">选用</el-button>
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
            <el-select v-model="formData.type" placeholder="请选择平台">
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
  height: 100%;
  gap: 20px;
  overflow: hidden; /* 防止溢出 */
}

/* 左侧面板 */
.left-panel {
  flex: 1; /* 默认占满 */
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
  flex: 0 0 30%; /* 固定 30% */
  background: #fff;
  border-left: 1px solid #e4e7ed;
  padding: 20px;
  display: flex;
  flex-direction: column;
  box-shadow: -2px 0 10px rgba(0,0,0,0.05);
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
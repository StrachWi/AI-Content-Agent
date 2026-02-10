<script setup>
import { ref } from 'vue'
import axios from 'axios'

const message = ref('等待服务器响应...')

const checkConnection = async () => {
  try {
    // 请求后端的测试接口
    const res = await axios.get('http://127.0.0.1:8000/api/test')
    message.value = res.data.data // 应该显示“这是从后端获取的数据”
  } catch (error) {
    message.value = '连接失败，请检查后端是否启动'
    console.error(error)
  }
}
</script>

<template>
  <div style="padding: 50px; text-align: center;">
    <h1>项目初始化测试</h1>
    <p>后端状态: {{ message }}</p>
    <button @click="checkConnection" style="padding: 10px 20px; cursor: pointer;">
      测试前后端连接
    </button>
  </div>
</template>
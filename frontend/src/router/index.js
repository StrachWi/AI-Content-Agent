import { createRouter, createWebHistory } from 'vue-router'

// 懒加载模式引入页面（更规范）
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'), // 工作台（首页）
      meta: { title: '工作台' }
    },
    {
      path: '/material',
      name: 'material',
      component: () => import('../views/MaterialView.vue'), // 素材库
      meta: { title: '素材库管理' }
    },
    {
      path: '/generate',
      name: 'generate',
      component: () => import('../views/GenerateView.vue'), // 内容智能生成
      meta: { title: '内容智能生成' }
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('../views/HistoryView.vue'), // 创作记录中心
      meta: { title: '创作记录中心' }
    }
  ]
})

export default router
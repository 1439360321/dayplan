// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../components/Dashboard.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Profile from '../components/Profile.vue'
import Calendar from '../components/Calendar.vue'
import { getToken } from '../utils/auth'
const routes = [
     {
    path: '/',
    redirect: '/index' // 默认跳转到 dashboard
  },
  { path: '/index', name: 'Dashboard', component: Dashboard,meta: { requiresAuth: true }},
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/calendar', name: 'Calendar', component: Calendar },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


/// 路由守卫：检查登录状态
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!getToken()
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login') // 未登录跳转登录页
  } else {
    next() // 其他情况正常放行
  }
})
export default router

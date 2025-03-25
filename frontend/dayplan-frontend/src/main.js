// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from './utils/axios'

// 让 Axios 自动发送 cookies（包括 sessionid 和 CSRF 令牌）
axios.defaults.withCredentials = true;


async function fetchCsrfToken() {
    try {
        const res = await axios.get('http://localhost:9000/api/csrf/', { withCredentials: true });
        const csrfToken = res.data.csrfToken;  // 这里应该是 res.data.csrfToken
        axios.defaults.headers.common['X-CSRFToken'] = csrfToken;  // 设置到默认请求头
        console.log("获取到的 CSRF 令牌:", csrfToken);
    } catch (error) {
        console.error("获取 CSRF 令牌失败", error);
    }
}

// 在应用启动时获取 CSRF 令牌
fetchCsrfToken();
const app = createApp(App)
app.config.globalProperties.$axios = axios  // 使 axios 在组件中通过 this.$axios 调用
app.use(router)
app.mount('#app')





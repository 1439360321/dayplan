<!-- src/components/Login.vue -->
<template>
  <div class="login">
    <h2>用户登录</h2>
    <form @submit.prevent="login">
      <div>
        <label>用户名或邮箱：</label>
        <input v-model="username" required />
      </div>
      <div>
        <label>密码：</label>
        <input type="password" v-model="password" required />
      </div>
      <div>
        <input type="checkbox" v-model="rememberMe" /> 记住我
      </div>
      <button type="submit">登录</button>
    </form>
    <p>没有账号？ <router-link to="/register">注册</router-link></p>
  </div>
</template>
<style scoped>
.login {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.login h2 {
  text-align: center;
  color: #333;
}

.login form div {
  margin-bottom: 15px;
}

.login label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.login input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.login button {
  width: 100%;
  padding: 10px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.2s;
}

.login button:hover {
  background: #0056b3;
}

.login p {
  text-align: center;
  margin-top: 10px;
}

.login a {
  color: #007bff;
  text-decoration: none;
}

.login a:hover {
  text-decoration: underline;
}

.login input[type="checkbox"] {
  margin-right: 5px;
}

</style>
<script>
import axios from "../utils/axios.js";
import { setToken } from '../utils/auth';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async fetchCsrfToken() {
    try {
        const res = await axios.get('http://localhost:9000/api/csrf/', { withCredentials: true });
        const csrfToken = res.data.csrfToken;  // 这里应该是 res.data.csrfToken
        axios.defaults.headers.common['X-CSRFToken'] = csrfToken;  // 设置到默认请求头
        console.log("获取到的 CSRF 令牌:", csrfToken);
    } catch (error) {
        console.error("获取 CSRF 令牌失败", error);
    }
},
    async login() {
      try {
        const res = await this.$axios.post('/api/login/', {
          username: this.username,
          password: this.password
        })
        setToken(res.data.token) // 保存 Token

        await this.fetchCsrfToken()
        this.$router.push('/')
      } catch (error) {
        alert('登录失败：' + (error.response.data.error || '未知错误'))
      }
    },

  }
}
</script>

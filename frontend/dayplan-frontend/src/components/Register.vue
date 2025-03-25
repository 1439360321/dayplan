<!-- src/components/Register.vue -->
<template>
  <div class="register">
    <h2>用户注册</h2>
    <form @submit.prevent="register">
      <div>
        <label>用户名：</label>
        <input v-model="username" required />
      </div>
      <div>
        <label>邮箱：</label>
        <input v-model="email" type="email" required />
      </div>
      <div>
        <label>手机号：</label>
        <input v-model="phone" />
      </div>
      <div>
        <label>性别：</label>
        <select v-model="gender">
          <option value="">请选择</option>
          <option value="M">男</option>
          <option value="F">女</option>
        </select>
      </div>
      <div>
        <label>年龄：</label>
        <input type="password" v-model="age" required />
      </div>
      <div>
        <label>密码：</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">注册</button>
    </form>
    <p>已有账号？ <router-link to="/login">登录</router-link></p>
  </div>
</template>
<style scoped>
.register {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.register h2 {
  text-align: center;
  color: #333;
}

.register form div {
  margin-bottom: 15px;
}

.register label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.register input, .register select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.register button {
  width: 100%;
  padding: 10px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.2s;
}

.register button:hover {
  background: #218838;
}

.register p {
  text-align: center;
  margin-top: 10px;
}

.register a {
  color: #007bff;
  text-decoration: none;
}

.register a:hover {
  text-decoration: underline;
}

</style>
<script>
export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      phone: '',
      gender: '',
      password: '',
      age: ''
    }
  },
  methods: {
    async register() {
      try {
        await this.$axios.post('/api/register/', {
          username: this.username,
          email: this.email,
          phone: this.phone,
          gender: this.gender,
          password: this.password,
          age: this.age
        })
        alert('注册成功，请前往邮箱验证账号！')
        this.$router.push('/login')
      } catch (error) {
        alert('注册失败：' + JSON.stringify(error.response.data))
      }
    },

  }
}
</script>

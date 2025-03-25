<!-- src/components/Profile.vue -->
<template>
  <div class="profile-edit">
    <h2>个人信息</h2>
    <form @submit.prevent="updateProfile">
      <div>
        <label>用户名：</label>
        <input v-model="profile.username" disabled />
      </div>
      <div>
        <label>邮箱：</label>
        <input v-model="profile.email" type="email" required />
      </div>
      <div>
        <label>手机号：</label>
        <input v-model="profile.phone" />
      </div>
      <div>
        <label>年龄：</label>
        <input v-model="profile.age" />
      </div>
      <div>
        <label>性别：</label>
        <select v-model="profile.gender">
          <option value="">请选择</option>
          <option value="M">男</option>
          <option value="F">女</option>
        </select>
      </div>
      <button type="submit">更新信息</button>
    </form>
    <hr/>
    <h3>修改密码</h3>
    <form @submit.prevent="changePassword">
      <div>
        <label>旧密码：</label>
        <input type="password" v-model="passwordData.old_password" required />
      </div>
      <div>
        <label>新密码：</label>
        <input type="password" v-model="passwordData.new_password" required />
      </div>
      <button type="submit">修改密码</button>
    </form>
  </div>
</template>
<style scoped>
.profile-edit {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.profile-edit h2, .profile-edit h3 {
  text-align: center;
  color: #333;
}

.profile-edit form div {
  margin-bottom: 15px;
}

.profile-edit label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.profile-edit input, .profile-edit select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.profile-edit button {
  width: 100%;
  padding: 10px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.2s;
}

.profile-edit button:hover {
  background: #0056b3;
}

hr {
  margin: 20px 0;
  border: 0;
  height: 1px;
  background: #ddd;
}

</style>
<script>
export default {
  name: 'Profile',
  data() {
    return {
      profile: {},
      passwordData: {
        old_password: '',
        new_password: ''
      }
    }
  },
  mounted() {
    this.fetchProfile()
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await this.$axios.get('/api/profile/')
        this.profile = res.data
      } catch (error) {
        console.error(error)
      }
    },
    async updateProfile() {
      try {
        const res = await this.$axios.put('/api/profile/', this.profile)
        this.profile = res.data
        alert('更新成功')
      } catch (error) {
        alert('更新失败：' + JSON.stringify(error.response.data))
      }
    },
    async changePassword() {
      try {
        await this.$axios.post('/api/change-password/', this.passwordData)
        alert('密码修改成功，请重新登录')
        localStorage.removeItem('user')
        sessionStorage.removeItem('user')
        this.$router.push('/login')
      } catch (error) {
        alert('修改失败：' + JSON.stringify(error.response.data))
      }
    },

  }
}
</script>

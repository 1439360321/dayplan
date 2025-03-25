<!-- src/components/Dashboard.vue -->
<template>
  <div class="dashboard">
    <h2>欢迎，{{ user.username }}</h2>
    <button @click="logout">退出登录</button>
    <div class="profile">
      <p>邮箱：{{ user.email }}</p>
      <p>手机号：{{ user.phone }}</p>
      <router-link to="/profile">修改个人信息</router-link>
    </div>
    <div>
    <h2>任务日历</h2>
    <Calendar :tasks="tasks" @date-selected="onDateSelected" />
  </div>
    <div class="tasks">
      <h3>今日任务</h3>
      <!-- 使用 vuedraggable 实现任务拖拽排序 -->
      <draggable v-model="tasks" item-key="id" @end="updateTaskOrder">
  <template #item="{ element }">
    <div class="task-item">
      <strong>{{ element.title }}</strong> - 优先级：{{ element.priority }}
      <span v-if="element.completed">(已完成)</span>
      <button @click="toggleTask(element)">切换状态</button>
    </div>
  </template>
</draggable>

      <div class="add-task">
        <h4>新增任务</h4>
        <input v-model="newTask.title" placeholder="任务标题" />
        <textarea v-model="newTask.description" placeholder="任务描述"></textarea>
        <select v-model="newTask.priority">
          <option value="high">高</option>
          <option value="medium" selected>中</option>
          <option value="low">低</option>
        </select>
        <input type="datetime-local" v-model="newTask.due_date" />
        <button @click="createTask">添加任务</button>
      </div>
      <div>
        <button @click="exportPDF">导出任务为 PDF</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.dashboard {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2, h3, h4 {
  color: #333;
}

.profile {
  padding: 15px;
  background: #fff;
  border-radius: 5px;
  margin-bottom: 20px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
}

.profile p {
  margin: 5px 0;
}

.tasks {
  padding: 15px;
  background: #fff;
  border-radius: 5px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  margin: 5px 0;
  background: #f4f4f4;
  border-radius: 5px;
  cursor: grab;
  transition: background 0.2s;
}

.task-item:hover {
  background: #e0e0e0;
}

.task-item button {
  padding: 5px 10px;
  border: none;
  background: #007bff;
  color: white;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.2s;
}

.task-item button:hover {
  background: #0056b3;
}

.add-task {
  margin-top: 20px;
  padding: 15px;
  background: #fff;
  border-radius: 5px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
}

.add-task input, .add-task textarea, .add-task select {
  width: 100%;
  padding: 8px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.add-task button {
  width: 100%;
  padding: 10px;
  border: none;
  background: #28a745;
  color: white;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.2s;
}

.add-task button:hover {
  background: #218838;
}

button.export {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.2s;
}

button.export:hover {
  background: #c82333;
}

</style>
<script>

import draggable from 'vuedraggable'
import Calendar from './Calendar.vue'
import { getToken, removeToken } from '../utils/auth'
export default {
  name: 'Dashboard',
  components: { draggable , Calendar},
  data() {
    return {
      user: [],
      tasks: [],
      newTask: {
        title: '',
        description: '',
        priority: 'medium',
        due_date: ''
      }
    }
  },

  async mounted() {
    await this.fetchTasks()
    const token = getToken()
    if (token) {
      await this.fetchUser()
    } else {
      this.$router.push('/login')
    }
  },
  methods: {
     async fetchUser() {
       try {
         const res = await this.$axios.get('/api/profile/')
         this.user = res.data
       } catch (error) {
         alert('身份验证失效，请重新登录')
         this.$router.push('/login')
       }
     },
    async fetchTasks() {
      try {
        const res = await this.$axios.get('/api/tasks/')
        this.tasks = res.data
      } catch (error) {
        console.error(error)
      }
    },
    async createTask() {
      try {
        const res = await this.$axios.post("/api/tasks/", this.newTask
        );
        this.tasks.push(res.data);
    } catch (error) {
        console.error("任务创建失败", error);
    }
    },
    async toggleTask(task) {
      try {
        const res = await this.$axios.put(`/api/tasks/${task.id}/`, { completed: !task.completed, title: task.title})
        task.completed = res.data.completed
      } catch (error) {
        console.error(error)
      }
    },
    async updateTaskOrder() {
      // 可在此调用 API 保存新的任务顺序
      console.log('任务排序更新：', this.tasks)
    },
    async exportPDF() {
      try {
        window.open('http://localhost:9000/api/export-pdf/', '_blank')
      } catch (error) {
        console.error('PDF 导出失败', error)
      }
    },
     onDateSelected(date) {
      console.log('选中的日期:', date);
    },
    // 退出登录
    async logout() {
      try {
        await this.axios.post('/api/logout/') // 调用 Django 后端的退出接口
      } catch (error) {
        console.error('退出失败', error)
      }
      removeToken() // 清除前端 Cookie
      this.$router.push('/login') // 跳转到登录页
    }
  }
}
</script>

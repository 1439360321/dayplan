// src/utils/axios.js
import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:9000',  // 后端 Django 服务器地址
  withCredentials: true,             // 保证跨域请求时携带 cookie
})

instance.interceptors.response.use(
  response => response,
  error => {
    return Promise.reject(error)
  }
)

export default instance

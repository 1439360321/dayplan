// 保存 Token 到 Cookie
export function setToken(token) {
  document.cookie = `auth_token=${token}; path=/; max-age=604800` // 7天有效期
}

// 获取 Token
export function getToken() {
  const cookies = document.cookie.split('; ')
  const tokenCookie = cookies.find(cookie => cookie.startsWith('auth_token='))
  return tokenCookie ? tokenCookie.split('=')[1] : null
}

// 删除 Token
export function removeToken() {
  document.cookie = 'auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC'
}

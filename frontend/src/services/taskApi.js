import axios from 'axios'
import { useUserStore } from '../store/userStore'

// Eğer Pinia store erişilemezse localStorage fallback
function getAccessToken() {
  try {
    return useUserStore().accessToken
  } catch {
    return localStorage.getItem('accessToken')
  }
}

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export function fetchTasks(params) {
  return axios.get(`${BASE_URL}/tasks/`, {
    params,
    headers: {
      Authorization: `Bearer ${getAccessToken()}`
    }
  })
}

export function fetchTaskDetail(taskId) {
  return axios.get(`${BASE_URL}/tasks/${taskId}/`, {
    headers: {
      Authorization: `Bearer ${getAccessToken()}`
    }
  })
}

export async function createTask(data) {
  return await axios.post(`${BASE_URL}/tasks/`, data, {
    headers: {Authorization: `Bearer ${getAccessToken()}`}
  })
}


export function updateTask(taskId, taskData) {
  return axios.patch(`${BASE_URL}/tasks/${taskId}/`, taskData, {
    headers: {
      Authorization: `Bearer ${getAccessToken()}`
    }
  })
}

export function deleteTask(taskId) {
  return axios.delete(`${BASE_URL}/tasks/${taskId}/`, {
    headers: {
      Authorization: `Bearer ${getAccessToken()}`
    }
  })
}

export function fetchUserTasks() {
  return axios.get(`${BASE_URL}/tasks/?my=1`, {
    headers: {
      Authorization: `Bearer ${getAccessToken()}`
    }
  })
}

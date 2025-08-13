import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const endpoints = {
  auth: { login: '/users/login', register: '/users/register', me: '/users/me' },
  departments: { list: '/departments', services: (id: number) => `/departments/${id}/services` },
  services: { list: '/services', byDepartment: (id: number) => `/services/department/${id}` },
  appointments: {
    mine: '/appointments/me', create: '/appointments/',
    timeSlotsAvailable: (sid: number) => `/appointments/time-slots/${sid}/available`
  },
  documents: { upload: '/documents/upload', mine: '/documents/me' },
  notifications: { mine: '/notifications/me', unread: '/notifications/unread/count' },
  feedback: { create: '/feedback', mine: '/feedback/me' },
  analytics: { overview: '/analytics/dashboard/overview' },
}



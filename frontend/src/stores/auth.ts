import { defineStore } from 'pinia'
import { api, endpoints } from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as any,
    token: localStorage.getItem('access_token') as string | null,
  }),
  actions: {
    async login(username: string, password: string) {
      const { data } = await api.post(endpoints.auth.login, { username, password })
      localStorage.setItem('access_token', data.access_token)
      this.token = data.access_token
      this.user = data.user
    },
    async register(payload: any) {
      await api.post(endpoints.auth.register, payload)
    },
    async me() {
      const { data } = await api.get(endpoints.auth.me)
      this.user = data
    },
    logout() {
      localStorage.removeItem('access_token')
      this.token = null
      this.user = null
    },
  },
})



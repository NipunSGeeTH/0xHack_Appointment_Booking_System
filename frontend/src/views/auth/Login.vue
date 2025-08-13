<template>
  <div class="auth-card">
    <h2>Login</h2>
    <form @submit.prevent="onSubmit">
      <label>Username</label>
      <input v-model="username" />
      <label>Password</label>
      <input type="password" v-model="password" />
      <div v-if="error" class="error">{{ error }}</div>
      <button type="submit">Login</button>
    </form>
  </div>
  
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref<string | null>(null)
const auth = useAuthStore()
const router = useRouter()

async function onSubmit() {
  error.value = null
  try {
    await auth.login(username.value, password.value)
    router.push('/dashboard')
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Login failed'
  }
}
</script>



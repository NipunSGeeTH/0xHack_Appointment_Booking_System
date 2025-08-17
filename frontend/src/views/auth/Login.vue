<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h2>Welcome Back</h2>
        <p>Sign in to access your government services account</p>
      </div>
      
      <form @submit.prevent="onSubmit" class="auth-form">
        <div class="form-group">
          <label class="form-label">Username</label>
          <input 
            v-model="username" 
            type="text"
            class="form-input"
            placeholder="Enter your username"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Password</label>
          <input 
            v-model="password" 
            type="password"
            class="form-input"
            placeholder="Enter your password"
            required
          />
        </div>
        
        <div v-if="error" class="alert alert-error">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
          <span v-if="loading" class="loading"></span>
          <span v-else>Sign In</span>
        </button>
      </form>
      
      <div class="auth-footer">
        <p>Don't have an account? 
          <router-link to="/register" class="text-primary">Register here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref<string | null>(null)
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

async function onSubmit() {
  error.value = null
  loading.value = true
  
  try {
    await auth.login(username.value, password.value)
    router.push('/dashboard')
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Login failed. Please check your credentials and try again.'
  } finally {
    loading.value = false
  }
}
</script>



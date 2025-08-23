<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h2>Create Account</h2>
        <p>Join the Sri Lankan Government Services Portal</p>
      </div>
      
      <form @submit.prevent="onSubmit" class="auth-form">
        <div class="form-group">
          <label class="form-label">Username</label>
          <input 
            v-model="form.username" 
            type="text"
            class="form-input"
            placeholder="Choose a username"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Email</label>
          <input 
            v-model="form.email" 
            type="email"
            class="form-input"
            placeholder="Enter your email"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Password</label>
          <input 
            v-model="form.password" 
            type="password"
            class="form-input"
            placeholder="Create a strong password"
            required
          />
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div class="form-group">
            <label class="form-label">First Name</label>
            <input 
              v-model="form.first_name" 
              type="text"
              class="form-input"
              placeholder="First name"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Last Name</label>
            <input 
              v-model="form.last_name" 
              type="text"
              class="form-input"
              placeholder="Last name"
              required
            />
          </div>
        </div>
        
        <div class="form-group">
          <label class="form-label">National ID</label>
          <input 
            v-model="form.national_id" 
            type="text"
            class="form-input"
            placeholder="Enter your National ID"
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
          <span v-else>Create Account</span>
        </button>
      </form>
      
      <div class="auth-footer">
        <p>Already have an account? 
          <router-link to="/login" class="text-primary">Sign in here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const form = reactive<any>({ username:'', email:'', password:'', first_name:'', last_name:'', national_id:'' })
const error = ref<string | null>(null)
const loading = ref(false)
const router = useRouter()
const auth = useAuthStore()

async function onSubmit() {
  error.value = null
  loading.value = true
  
  try {
    await auth.register(form)
    router.push('/login')
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Registration failed. Please check your information and try again.'
  } finally {
    loading.value = false
  }
}
</script>



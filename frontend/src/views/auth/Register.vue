<template>
  <div class="auth-card">
    <h2>Register</h2>
    <form @submit.prevent="onSubmit">
      <label>Username</label>
      <input v-model="form.username" />
      <label>Email</label>
      <input v-model="form.email" />
      <label>Password</label>
      <input type="password" v-model="form.password" />
      <label>First Name</label>
      <input v-model="form.first_name" />
      <label>Last Name</label>
      <input v-model="form.last_name" />
      <label>National ID</label>
      <input v-model="form.national_id" />
      <div v-if="error" class="error">{{ error }}</div>
      <button type="submit">Create Account</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const form = reactive<any>({ username:'', email:'', password:'', first_name:'', last_name:'', national_id:'' })
const error = ref<string | null>(null)
const router = useRouter()
const auth = useAuthStore()

async function onSubmit() {
  error.value = null
  try {
    await auth.register(form)
    router.push('/login')
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Registration failed'
  }
}
</script>



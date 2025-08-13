<template>
  <div class="app-container">
    <nav class="topnav">
      <div class="brand"><router-link to="/">Gov Portal</router-link></div>
      <div class="links">
        <router-link to="/departments">Departments</router-link>
        <router-link to="/services">Services</router-link>
        <template v-if="(auth.user?.role || '').toLowerCase() === 'citizen'">
          <router-link to="/book">Book</router-link>
        </template>
        <template v-if="auth.user">
          <router-link to="/dashboard">Dashboard</router-link>
          <button @click="onLogout">Logout</button>
        </template>
        <template v-else>
          <router-link to="/login">Login</router-link>
          <router-link to="/register">Register</router-link>
        </template>
      </div>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
  
</template>

<script setup lang="ts">
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function onLogout() {
  auth.logout()
  router.push('/login')
}
</script>



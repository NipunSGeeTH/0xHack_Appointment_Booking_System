<template>
  <div id="app">
    <!-- Navigation -->
    <nav class="navbar">
      <div class="navbar-container">
        <router-link to="/" class="navbar-brand">
          <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path>
          </svg>
          Sri Lanka Gov Portal
        </router-link>
        
        <ul class="navbar-nav">
          <li><router-link to="/departments" class="nav-link">Departments</router-link></li>
          <li><router-link to="/services" class="nav-link">Services</router-link></li>
          
          <template v-if="(auth.user?.role || '').toLowerCase() === 'citizen'">
            <li><router-link to="/book" class="nav-link">Book Appointment</router-link></li>
          </template>
          
          <template v-if="auth.user">
            <li><router-link to="/dashboard" class="nav-link">Dashboard</router-link></li>
            <li>
              <button @click="onLogout" class="btn btn-ghost">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                </svg>
                Logout
              </button>
            </li>
          </template>
          
          <template v-else>
            <li><router-link to="/login" class="nav-link">Login</router-link></li>
            <li><router-link to="/register" class="btn btn-primary">Register</router-link></li>
          </template>
        </ul>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 class="text-lg font-semibold mb-4">Sri Lanka Government Portal</h3>
            <p class="text-gray-600">Providing efficient and accessible government services to all citizens.</p>
          </div>
          <div>
            <h4 class="font-semibold mb-4">Quick Links</h4>
            <ul class="space-y-2">
              <li><router-link to="/departments" class="text-gray-600 hover:text-primary">Departments</router-link></li>
              <li><router-link to="/services" class="text-gray-600 hover:text-primary">Services</router-link></li>
              <li><router-link to="/book" class="text-gray-600 hover:text-primary">Book Appointment</router-link></li>
            </ul>
          </div>
          <div>
            <h4 class="font-semibold mb-4">Contact</h4>
            <p class="text-gray-600">Email: info@gov.lk</p>
            <p class="text-gray-600">Phone: +94 11 123 4567</p>
          </div>
        </div>
        <div class="border-t border-gray-200 mt-8 pt-8 text-center text-gray-600">
          <p>&copy; 2024 Sri Lanka Government. All rights reserved.</p>
        </div>
      </div>
    </footer>
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



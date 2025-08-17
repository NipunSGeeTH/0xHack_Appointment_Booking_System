<template>
  <div class="dashboard-container">
    <!-- Dashboard Header -->
    <div class="dashboard-header">
      <div class="welcome-section">
        <h1>Welcome back, {{ user?.first_name || 'User' }}!</h1>
        <p>Manage your government services and appointments</p>
      </div>
      
      <div class="quick-stats">
        <div class="stat-card">
          <div class="stat-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <h3>{{ stats.appointments || 0 }}</h3>
            <p>Total Appointments</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <h3>{{ stats.documents || 0 }}</h3>
            <p>Documents Uploaded</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM4 19h6v-2H4v2zM4 15h6v-2H4v2zM4 11h6V9H4v2zM4 7h6V5H4v2z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <h3>{{ stats.notifications || 0 }}</h3>
            <p>Unread Notifications</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <h2>Quick Actions</h2>
      <div class="actions-grid">
        <router-link to="/book" class="action-card primary">
          <div class="action-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </div>
          <div class="action-content">
            <h3>Book Appointment</h3>
            <p>Schedule a new government service appointment</p>
          </div>
        </router-link>
        
        <router-link to="/dashboard/user/appointments" class="action-card">
          <div class="action-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
            </svg>
          </div>
          <div class="action-content">
            <h3>My Appointments</h3>
            <p>View and manage your scheduled appointments</p>
          </div>
        </router-link>
        
        <router-link to="/dashboard/user/documents" class="action-card">
          <div class="action-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <div class="action-content">
            <h3>My Documents</h3>
            <p>Upload and manage your documents</p>
          </div>
        </router-link>
        
        <router-link to="/dashboard/user/notifications" class="action-card">
          <div class="action-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM4 19h6v-2H4v2zM4 15h6v-2H4v2zM4 11h6V9H4v2zM4 7h6V5H4v2z"></path>
            </svg>
          </div>
          <div class="action-content">
            <h3>Notifications</h3>
            <p>View your notifications and updates</p>
          </div>
        </router-link>
        
        <router-link to="/dashboard/user/feedback" class="action-card">
          <div class="action-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
          </div>
          <div class="action-content">
            <h3>Feedback</h3>
            <p>Share your feedback and suggestions</p>
          </div>
        </router-link>
        
        <router-link to="/services" class="action-card">
          <div class="action-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <div class="action-content">
            <h3>Browse Services</h3>
            <p>Explore available government services</p>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="recent-activity" v-if="recentAppointments.length > 0">
      <h2>Recent Appointments</h2>
      <div class="activity-list">
        <div 
          v-for="appointment in recentAppointments" 
          :key="appointment.id" 
          class="activity-item"
        >
          <div class="activity-icon">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </div>
          <div class="activity-content">
            <h4>{{ appointment.service?.name || 'Unknown Service' }}</h4>
            <p>{{ formatDate(appointment.appointment_date) }} at {{ formatTime(appointment.appointment_date) }}</p>
            <span class="status-badge" :class="appointment.status.toLowerCase()">
              {{ appointment.status }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Router View for nested routes -->
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { api, endpoints } from '../../services/api'

const auth = useAuthStore()
const user = computed(() => auth.user)

const stats = ref({
  appointments: 0,
  documents: 0,
  notifications: 0
})

const recentAppointments = ref<any[]>([])

async function loadDashboardData() {
  try {
    // Load appointments count
    const appointmentsResponse = await api.get(endpoints.appointments.mine)
    stats.value.appointments = appointmentsResponse.data.length
    recentAppointments.value = appointmentsResponse.data.slice(0, 5) // Get last 5 appointments
    
    // Load documents count
    const documentsResponse = await api.get(endpoints.documents.mine)
    stats.value.documents = documentsResponse.data.length
    
    // Load unread notifications count
    const notificationsResponse = await api.get(endpoints.notifications.unread)
    stats.value.notifications = notificationsResponse.data.count || 0
    
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  }
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function formatTime(dateString: string) {
  return new Date(dateString).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadDashboardData()
})
</script>



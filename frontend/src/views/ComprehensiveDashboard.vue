<template>
  <div class="comprehensive-dashboard">
    <!-- Header Section -->
    <div class="dashboard-header">
      <div class="container mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Sri Lanka Government Services Portal
        </h1>
        <p class="text-xl text-gray-600 mb-8">
          Comprehensive access to all government services, appointments, and administrative functions
        </p>
        
        <!-- Quick Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="stat-card">
            <div class="stat-icon">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.departments || '...' }}</h3>
              <p class="stat-label">Departments</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.services || '...' }}</h3>
              <p class="stat-label">Services</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.appointments || '...' }}</h3>
              <p class="stat-label">Appointments</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.users || '...' }}</h3>
              <p class="stat-label">Users</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 pb-12">
      <!-- Navigation Tabs -->
      <div class="dashboard-tabs mb-8">
        <nav class="flex space-x-8 border-b border-gray-200">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'tab-button',
              activeTab === tab.id ? 'tab-active' : 'tab-inactive'
            ]"
          >
            <component :is="tab.icon" class="w-5 h-5 mr-2" />
            {{ tab.name }}
          </button>
        </nav>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Citizen Services Tab -->
        <div v-if="activeTab === 'citizen'" class="space-y-8">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Book Appointment -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">Book Appointment</h3>
                <p class="feature-description">Schedule appointments for government services</p>
              </div>
              <div class="feature-actions">
                <router-link to="/book" class="btn btn-primary">
                  Book Now
                </router-link>
                <router-link to="/departments" class="btn btn-outline">
                  View Departments
                </router-link>
              </div>
            </div>

            <!-- My Appointments -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">My Appointments</h3>
                <p class="feature-description">View and manage your scheduled appointments</p>
              </div>
              <div class="feature-actions">
                <router-link to="/dashboard/user/appointments" class="btn btn-primary">
                  View Appointments
                </router-link>
                <router-link to="/dashboard/user/documents" class="btn btn-outline">
                  My Documents
                </router-link>
              </div>
            </div>

            <!-- Services Directory -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">Services Directory</h3>
                <p class="feature-description">Browse all available government services</p>
              </div>
              <div class="feature-actions">
                <router-link to="/services" class="btn btn-primary">
                  Browse Services
                </router-link>
                <router-link to="/departments" class="btn btn-outline">
                  View Departments
                </router-link>
              </div>
            </div>

            <!-- Feedback & Support -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">Feedback & Support</h3>
                <p class="feature-description">Share your experience and get help</p>
              </div>
              <div class="feature-actions">
                <router-link to="/dashboard/user/feedback" class="btn btn-primary">
                  Submit Feedback
                </router-link>
                <router-link to="/dashboard/user/notifications" class="btn btn-outline">
                  Notifications
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Government Officer Tab -->
        <div v-if="activeTab === 'officer'" class="space-y-8">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Manage Appointments -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">Manage Appointments</h3>
                <p class="feature-description">Handle citizen appointments and schedules</p>
              </div>
              <div class="feature-actions">
                <router-link to="/dashboard/officer/appointments" class="btn btn-primary">
                  View Appointments
                </router-link>
                <router-link to="/dashboard/officer/documents" class="btn btn-outline">
                  Review Documents
                </router-link>
              </div>
            </div>

            <!-- Department Services -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">Department Services</h3>
                <p class="feature-description">Manage services and time slots</p>
              </div>
              <div class="feature-actions">
                <router-link to="/services" class="btn btn-primary">
                  Manage Services
                </router-link>
                <router-link to="/departments" class="btn btn-outline">
                  Department Info
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Admin Tab -->
        <div v-if="activeTab === 'admin'" class="space-y-8">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- User Management -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">User Management</h3>
                <p class="feature-description">Manage system users and roles</p>
              </div>
              <div class="feature-actions">
                <router-link to="/dashboard/admin/users" class="btn btn-primary">
                  Manage Users
                </router-link>
                <button @click="showUserStats = true" class="btn btn-outline">
                  View Stats
                </button>
              </div>
            </div>

            <!-- Department Management -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">Department Management</h3>
                <p class="feature-description">Create and manage departments</p>
              </div>
              <div class="feature-actions">
                <router-link to="/dashboard/admin/departments" class="btn btn-primary">
                  Manage Departments
                </button>
                <button @click="showDepartmentStats = true" class="btn btn-outline">
                  View Stats
                </button>
              </div>
            </div>

            <!-- Service Management -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">Service Management</h3>
                <p class="feature-description">Configure government services</p>
              </div>
              <div class="feature-actions">
                <router-link to="/dashboard/admin/services" class="btn btn-primary">
                  Manage Services
                </router-link>
                <button @click="showServiceStats = true" class="btn btn-outline">
                  View Stats
                </button>
              </div>
            </div>

            <!-- Time Slot Management -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">Time Slot Management</h3>
                <p class="feature-description">Configure appointment time slots</p>
              </div>
              <div class="feature-actions">
                <router-link to="/dashboard/admin/time-slots" class="btn btn-primary">
                  Manage Time Slots
                </router-link>
              </div>
            </div>

            <!-- Analytics Dashboard -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">Analytics Dashboard</h3>
                <p class="feature-description">System performance and insights</p>
              </div>
              <div class="feature-actions">
                <router-link to="/dashboard/admin/analytics" class="btn btn-primary">
                  View Analytics
                </router-link>
                <button @click="showAnalytics = true" class="btn btn-outline">
                  Quick Stats
                </button>
              </div>
            </div>

            <!-- System Health -->
            <div class="feature-card">
              <div class="feature-header">
                <h3 class="feature-title">System Health</h3>
                <p class="feature-description">Monitor system status and performance</p>
              </div>
              <div class="feature-actions">
                <button @click="checkSystemHealth" class="btn btn-primary">
                  Check Health
                </button>
                <button @click="showSystemInfo = true" class="btn btn-outline">
                  System Info
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- API Explorer Tab -->
        <div v-if="activeTab === 'api'" class="space-y-8">
          <div class="api-explorer">
            <h3 class="text-2xl font-bold mb-6">API Endpoints Explorer</h3>
            
            <!-- API Categories -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div 
                v-for="category in apiCategories" 
                :key="category.name"
                class="api-category-card"
              >
                <div class="api-category-header">
                  <h4 class="api-category-title">{{ category.name }}</h4>
                  <span class="api-category-count">{{ category.endpoints.length }} endpoints</span>
                </div>
                <div class="api-category-endpoints">
                  <div 
                    v-for="endpoint in category.endpoints.slice(0, 3)" 
                    :key="endpoint.path"
                    class="api-endpoint-item"
                  >
                    <span class="api-method" :class="`method-${endpoint.method.toLowerCase()}`">
                      {{ endpoint.method }}
                    </span>
                    <span class="api-path">{{ endpoint.path }}</span>
                  </div>
                  <div v-if="category.endpoints.length > 3" class="api-more">
                    +{{ category.endpoints.length - 3 }} more
                  </div>
                </div>
                <button 
                  @click="showApiCategory(category)"
                  class="api-category-button"
                >
                  View All Endpoints
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <div v-if="showUserStats" class="modal-overlay" @click="showUserStats = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">User Statistics</h3>
          <button @click="showUserStats = false" class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-label">Total Users</span>
              <span class="stat-value">{{ userStats.total || 'Loading...' }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Active Users</span>
              <span class="stat-value">{{ userStats.active || 'Loading...' }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Citizens</span>
              <span class="stat-value">{{ userStats.citizens || 'Loading...' }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Government Officers</span>
              <span class="stat-value">{{ userStats.officers || 'Loading...' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- API Category Modal -->
    <div v-if="selectedApiCategory" class="modal-overlay" @click="selectedApiCategory = null">
      <div class="modal-content modal-large" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">{{ selectedApiCategory.name }} API Endpoints</h3>
          <button @click="selectedApiCategory = null" class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <div class="api-endpoints-list">
            <div 
              v-for="endpoint in selectedApiCategory.endpoints" 
              :key="endpoint.path"
              class="api-endpoint-detail"
            >
              <div class="api-endpoint-header">
                <span class="api-method" :class="`method-${endpoint.method.toLowerCase()}`">
                  {{ endpoint.method }}
                </span>
                <span class="api-path">{{ endpoint.path }}</span>
                <span class="api-description">{{ endpoint.description }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { api, endpoints } from '../services/api-comprehensive'

const auth = useAuthStore()

// Reactive state
const activeTab = ref('citizen')
const stats = ref({
  departments: 0,
  services: 0,
  appointments: 0,
  users: 0
})
const userStats = ref({})
const showUserStats = ref(false)
const selectedApiCategory = ref(null)

// Tab configuration
const tabs = computed(() => {
  const baseTabs = [
    {
      id: 'citizen',
      name: 'Citizen Services',
      icon: 'UserIcon'
    }
  ]

  if (auth.user?.role === 'government_officer' || auth.user?.role === 'admin') {
    baseTabs.push({
      id: 'officer',
      name: 'Government Officer',
      icon: 'ShieldCheckIcon'
    })
  }

  if (auth.user?.role === 'admin') {
    baseTabs.push({
      id: 'admin',
      name: 'Administration',
      icon: 'CogIcon'
    })
  }

  baseTabs.push({
    id: 'api',
    name: 'API Explorer',
    icon: 'CodeIcon'
  })

  return baseTabs
})

// API Categories
const apiCategories = [
  {
    name: 'Users',
    endpoints: [
      { method: 'GET', path: '/users/', description: 'Get all users' },
      { method: 'POST', path: '/users/register', description: 'Register new user' },
      { method: 'POST', path: '/users/login', description: 'User login' },
      { method: 'GET', path: '/users/me', description: 'Get current user' },
      { method: 'PUT', path: '/users/me', description: 'Update current user' },
      { method: 'GET', path: '/users/officers', description: 'Get government officers' }
    ]
  },
  {
    name: 'Departments',
    endpoints: [
      { method: 'GET', path: '/departments/', description: 'Get all departments' },
      { method: 'POST', path: '/departments/', description: 'Create department' },
      { method: 'GET', path: '/departments/{id}/services', description: 'Get department services' },
      { method: 'GET', path: '/departments/search/{term}', description: 'Search departments' }
    ]
  },
  {
    name: 'Services',
    endpoints: [
      { method: 'GET', path: '/services/', description: 'Get all services' },
      { method: 'POST', path: '/services/', description: 'Create service' },
      { method: 'GET', path: '/services/department/{id}', description: 'Get services by department' },
      { method: 'GET', path: '/services/search', description: 'Search services' }
    ]
  },
  {
    name: 'Appointments',
    endpoints: [
      { method: 'POST', path: '/appointments/', description: 'Create appointment' },
      { method: 'GET', path: '/appointments/me', description: 'Get my appointments' },
      { method: 'GET', path: '/appointments/time-slots/{id}/available', description: 'Get available time slots' },
      { method: 'PUT', path: '/appointments/{id}/status', description: 'Update appointment status' }
    ]
  },
  {
    name: 'Documents',
    endpoints: [
      { method: 'POST', path: '/documents/upload', description: 'Upload document' },
      { method: 'GET', path: '/documents/me', description: 'Get my documents' },
      { method: 'PUT', path: '/documents/{id}/verify', description: 'Verify document' },
      { method: 'GET', path: '/documents/download/{id}', description: 'Download document' }
    ]
  },
  {
    name: 'Analytics',
    endpoints: [
      { method: 'GET', path: '/analytics/dashboard/overview', description: 'Dashboard overview' },
      { method: 'GET', path: '/analytics/appointments/trends', description: 'Appointment trends' },
      { method: 'GET', path: '/analytics/departments/performance', description: 'Department performance' },
      { method: 'GET', path: '/analytics/users/engagement', description: 'User engagement' }
    ]
  }
]

// Methods
const loadStats = async () => {
  try {
    // Load basic statistics
    const [deptResponse, servicesResponse, usersResponse] = await Promise.all([
      api.get(endpoints.departments.list),
      api.get(endpoints.services.list),
      api.get(endpoints.users.list)
    ])

    stats.value = {
      departments: deptResponse.data.length,
      services: servicesResponse.data.length,
      appointments: 0, // Will be loaded separately
      users: usersResponse.data.length
    }

    // Load appointment count if user is authenticated
    if (auth.user) {
      try {
        const appointmentsResponse = await api.get(endpoints.appointments.mine)
        stats.value.appointments = appointmentsResponse.data.length
      } catch (error) {
        console.log('Could not load appointments')
      }
    }
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

const loadUserStats = async () => {
  try {
    const response = await api.get(endpoints.users.getStatistics)
    userStats.value = response.data
  } catch (error) {
    console.error('Error loading user stats:', error)
  }
}

const checkSystemHealth = async () => {
  try {
    const response = await api.get(endpoints.system.health)
    alert(`System Status: ${response.data.status}`)
  } catch (error) {
    alert('System health check failed')
  }
}

const showApiCategory = (category: any) => {
  selectedApiCategory.value = category
}

// Lifecycle
onMounted(() => {
  loadStats()
  
  // Set default tab based on user role
  if (auth.user?.role === 'admin') {
    activeTab.value = 'admin'
  } else if (auth.user?.role === 'government_officer') {
    activeTab.value = 'officer'
  }
})

// Watch for tab changes to load relevant data
watch(activeTab, (newTab) => {
  if (newTab === 'admin') {
    loadUserStats()
  }
})
</script>

<style scoped>
.comprehensive-dashboard {
  @apply min-h-screen bg-gray-50;
}

.dashboard-header {
  @apply bg-gradient-to-r from-blue-600 to-blue-800 text-white;
}

.stat-card {
  @apply bg-white rounded-lg shadow-md p-6 flex items-center space-x-4;
}

.stat-icon {
  @apply text-blue-600;
}

.stat-content {
  @apply flex-1;
}

.stat-number {
  @apply text-3xl font-bold text-gray-900;
}

.stat-label {
  @apply text-gray-600;
}

.dashboard-tabs {
  @apply bg-white rounded-lg shadow-sm;
}

.tab-button {
  @apply flex items-center px-6 py-4 text-sm font-medium border-b-2 transition-colors duration-200;
}

.tab-active {
  @apply border-blue-500 text-blue-600;
}

.tab-inactive {
  @apply border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300;
}

.feature-card {
  @apply bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow duration-200;
}

.feature-header {
  @apply mb-4;
}

.feature-title {
  @apply text-xl font-semibold text-gray-900 mb-2;
}

.feature-description {
  @apply text-gray-600;
}

.feature-actions {
  @apply flex flex-wrap gap-3;
}

.btn {
  @apply inline-flex items-center px-4 py-2 rounded-md font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2;
}

.btn-outline {
  @apply border border-gray-300 text-gray-700 hover:bg-gray-50;
}

.api-explorer {
  @apply bg-white rounded-lg shadow-md p-6;
}

.api-category-card {
  @apply bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow duration-200;
}

.api-category-header {
  @apply flex justify-between items-center mb-4;
}

.api-category-title {
  @apply text-lg font-semibold text-gray-900;
}

.api-category-count {
  @apply text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded-full;
}

.api-endpoint-item {
  @apply flex items-center space-x-2 py-2;
}

.api-method {
  @apply text-xs font-mono px-2 py-1 rounded text-white font-bold;
}

.method-get { @apply bg-green-600; }
.method-post { @apply bg-blue-600; }
.method-put { @apply bg-yellow-600; }
.method-delete { @apply bg-red-600; }

.api-path {
  @apply text-sm font-mono text-gray-700;
}

.api-more {
  @apply text-sm text-gray-500 italic;
}

.api-category-button {
  @apply w-full mt-4 px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors duration-200;
}

.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50;
}

.modal-content {
  @apply bg-white rounded-lg shadow-xl max-w-md w-full mx-4 max-h-96 overflow-y-auto;
}

.modal-large {
  @apply max-w-4xl;
}

.modal-header {
  @apply flex justify-between items-center p-6 border-b border-gray-200;
}

.modal-title {
  @apply text-xl font-semibold text-gray-900;
}

.modal-close {
  @apply text-gray-400 hover:text-gray-600 text-2xl font-bold;
}

.modal-body {
  @apply p-6;
}

.stats-grid {
  @apply grid grid-cols-2 gap-4;
}

.stat-item {
  @apply flex flex-col;
}

.stat-label {
  @apply text-sm text-gray-600 mb-1;
}

.stat-value {
  @apply text-lg font-semibold text-gray-900;
}

.api-endpoints-list {
  @apply space-y-4;
}

.api-endpoint-detail {
  @apply border border-gray-200 rounded-lg p-4;
}

.api-endpoint-header {
  @apply flex items-center space-x-4;
}

.api-description {
  @apply text-sm text-gray-600 flex-1;
}
</style>

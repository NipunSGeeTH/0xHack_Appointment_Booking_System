<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Government Departments</h1>
      <p class="page-subtitle">Explore our government departments and their services</p>
    </div>

    <div class="departments-container">
      <!-- Search and Filter -->
      <div class="filters-section">
        <div class="search-box">
          <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search departments..."
            class="search-input"
          />
        </div>
        
        <div class="filter-options">
          <label class="filter-label">
            <input 
              v-model="showActiveOnly" 
              type="checkbox" 
              class="filter-checkbox"
            />
            Show Active Departments Only
          </label>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading"></div>
        <p>Loading departments...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <p>{{ error }}</p>
        <button @click="loadDepartments" class="btn btn-primary">Try Again</button>
      </div>

      <!-- Departments Grid -->
      <div v-else class="departments-grid">
        <div 
          v-for="department in filteredDepartments" 
          :key="department.id" 
          class="department-card"
        >
          <div class="department-header">
            <div class="department-icon">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <div class="department-status" :class="department.is_active ? 'active' : 'inactive'">
              <span class="status-dot"></span>
              {{ department.is_active ? 'Active' : 'Inactive' }}
            </div>
          </div>
          
          <div class="department-content">
            <h3 class="department-name">{{ department.name }}</h3>
            <p class="department-description">
              {{ department.description || 'No description available' }}
            </p>
            
            <div class="department-details">
              <div class="detail-item" v-if="department.location">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                <span>{{ department.location }}</span>
              </div>
              
              <div class="detail-item" v-if="department.contact_number">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                </svg>
                <span>{{ department.contact_number }}</span>
              </div>
              
              <div class="detail-item" v-if="department.email">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
                <span>{{ department.email }}</span>
              </div>
              
              <div class="detail-item" v-if="department.operating_hours">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>{{ department.operating_hours }}</span>
              </div>
            </div>
          </div>
          
          <div class="department-actions">
            <router-link 
              :to="`/services?department=${department.id}`" 
              class="btn btn-primary"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 3v7a6 6 0 006 6 6 6 0 006-6V3"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 21v-7a6 6 0 00-6-6 6 6 0 00-6 6v7"></path>
              </svg>
              View Services
            </router-link>
            
            <button 
              v-if="department.is_active" 
              @click="viewDepartment(department)"
              class="btn btn-outline"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
              View Details
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && filteredDepartments.length === 0" class="empty-state">
        <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47-.881-6.08-2.33"></path>
        </svg>
        <h3>No departments found</h3>
        <p>No departments match your search criteria.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { api, endpoints } from '../services/api'

const departments = ref<any[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const showActiveOnly = ref(true)

const filteredDepartments = computed(() => {
  let filtered = departments.value

  // Filter by active status
  if (showActiveOnly.value) {
    filtered = filtered.filter(dept => dept.is_active)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(dept => 
      dept.name.toLowerCase().includes(query) ||
      (dept.description && dept.description.toLowerCase().includes(query)) ||
      (dept.location && dept.location.toLowerCase().includes(query))
    )
  }

  return filtered
})

async function loadDepartments() {
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get(endpoints.departments.list, {
      params: { active_only: showActiveOnly.value }
    })
    departments.value = response.data
  } catch (err: any) {
    error.value = err?.response?.data?.detail || 'Failed to load departments'
    console.error('Error loading departments:', err)
  } finally {
    loading.value = false
  }
}

function viewDepartment(department: any) {
  // TODO: Implement department detail view
  console.log('Viewing department:', department)
}

onMounted(() => {
  loadDepartments()
})
</script>

<style scoped>
.container {
  @apply max-w-7xl mx-auto px-4 py-8;
}

.page-header {
  @apply text-center mb-8;
}

.page-title {
  @apply text-3xl font-bold text-gray-900 mb-2;
}

.page-subtitle {
  @apply text-lg text-gray-600;
}

.departments-container {
  @apply space-y-6;
}

.filters-section {
  @apply flex flex-col sm:flex-row gap-4 items-center justify-between bg-white p-4 rounded-lg border border-gray-200;
}

.search-box {
  @apply relative flex-1 max-w-md;
}

.search-icon {
  @apply absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400;
}

.search-input {
  @apply w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent;
}

.filter-options {
  @apply flex items-center gap-2;
}

.filter-label {
  @apply flex items-center gap-2 text-sm text-gray-700 cursor-pointer;
}

.filter-checkbox {
  @apply w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500;
}

.loading-state {
  @apply text-center py-12;
}

.loading {
  @apply w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4;
}

.error-state {
  @apply text-center py-12 text-red-600;
}

.error-icon {
  @apply w-12 h-12 mx-auto mb-4;
}

.departments-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6;
}

.department-card {
  @apply border border-gray-200 rounded-lg p-6 cursor-pointer transition-all duration-200 hover:border-blue-300 hover:shadow-lg flex flex-col bg-white;
}

.department-header {
  @apply flex justify-between items-start mb-4;
}

.department-icon {
  @apply text-blue-600 bg-blue-100 p-2 rounded-lg;
}

.department-status {
  @apply text-xs px-2 py-1 rounded-full font-medium flex items-center gap-1;
}

.status-dot {
  @apply w-2 h-2 rounded-full;
}

.department-status.active {
  @apply bg-green-100 text-green-800;
}

.department-status.active .status-dot {
  @apply bg-green-600;
}

.department-status.inactive {
  @apply bg-red-100 text-red-800;
}

.department-status.inactive .status-dot {
  @apply bg-red-600;
}

.department-content {
  @apply flex-1 flex flex-col;
}

.department-name {
  @apply text-lg font-bold text-gray-900 mb-3;
}

.department-description {
  @apply text-sm text-gray-600 mb-4;
}

.department-details {
  @apply space-y-2 mb-4;
}

.detail-item {
  @apply flex items-center gap-2 text-xs text-gray-500;
}

.department-actions {
  @apply flex gap-3 mt-auto pt-4;
}

.btn {
  @apply inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-md font-medium transition-colors duration-200 min-h-[40px] text-sm;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 shadow-sm;
}

.btn-outline {
  @apply border border-gray-300 text-gray-700 hover:bg-gray-50 bg-white;
}

.empty-state {
  @apply text-center py-12 text-gray-500;
}

.empty-icon {
  @apply w-12 h-12 mx-auto mb-4;
}
</style>



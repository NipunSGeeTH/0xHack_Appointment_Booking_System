<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Government Services</h1>
      <p class="page-subtitle">Browse and book government services</p>
    </div>

    <div class="services-container">
      <!-- Filters -->
      <div class="filters-section">
        <div class="search-box">
          <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search services..."
            class="search-input"
          />
        </div>
        
        <div class="filter-controls">
          <select v-model="selectedDepartment" class="form-select">
            <option value="">All Departments</option>
            <option v-for="dept in departments" :key="dept.id" :value="dept.id">
              {{ dept.name }}
            </option>
          </select>
          
          <label class="filter-label">
            <input 
              v-model="showActiveOnly" 
              type="checkbox" 
              class="filter-checkbox"
            />
            Active Services Only
          </label>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading"></div>
        <p>Loading services...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <p>{{ error }}</p>
        <button @click="loadServices" class="btn btn-primary">Try Again</button>
      </div>

      <!-- Services Grid -->
      <div v-else class="services-grid">
        <div 
          v-for="service in filteredServices" 
          :key="service.id" 
          class="service-card"
        >
          <div class="service-header">
            <div class="service-icon">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div class="service-status" :class="service.is_active ? 'active' : 'inactive'">
              <span class="status-dot"></span>
              {{ service.is_active ? 'Available' : 'Unavailable' }}
            </div>
          </div>
          
          <div class="service-content">
            <h3 class="service-name">{{ service.name }}</h3>
            <p class="service-description">
              {{ service.description || 'No description available' }}
            </p>
            
            <div class="service-details">
              <div class="detail-item">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>{{ service.duration_minutes }} minutes</span>
              </div>
              
              <div class="detail-item">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                </svg>
                <span>{{ service.department?.name || 'Unknown Department' }}</span>
              </div>
              
              <div class="detail-item" v-if="service.required_documents">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <span>Documents Required</span>
              </div>
            </div>
          </div>
          
          <div class="service-actions">
            <router-link 
              :to="`/book?service=${service.id}`" 
              class="btn btn-primary"
              :class="{ 'disabled': !service.is_active }"
              :disabled="!service.is_active"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              Book Appointment
            </router-link>
            
            <button 
              @click="viewService(service)"
              class="btn btn-outline"
            >
              View Details
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && filteredServices.length === 0" class="empty-state">
        <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47-.881-6.08-2.33"></path>
        </svg>
        <h3>No services found</h3>
        <p>No services match your search criteria.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { api, endpoints } from '../services/api'

const route = useRoute()
const services = ref<any[]>([])
const departments = ref<any[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const selectedDepartment = ref('')
const showActiveOnly = ref(true)

const filteredServices = computed(() => {
  let filtered = services.value

  // Filter by department
  if (selectedDepartment.value) {
    filtered = filtered.filter(service => service.department_id === Number(selectedDepartment.value))
  }

  // Filter by active status
  if (showActiveOnly.value) {
    filtered = filtered.filter(service => service.is_active)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(service => 
      service.name.toLowerCase().includes(query) ||
      (service.description && service.description.toLowerCase().includes(query)) ||
      (service.department?.name && service.department.name.toLowerCase().includes(query))
    )
  }

  return filtered
})

async function loadServices() {
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get(endpoints.services.list, {
      params: { active_only: showActiveOnly.value }
    })
    services.value = response.data
  } catch (err: any) {
    error.value = err?.response?.data?.detail || 'Failed to load services'
    console.error('Error loading services:', err)
  } finally {
    loading.value = false
  }
}

async function loadDepartments() {
  try {
    const response = await api.get(endpoints.departments.list)
    departments.value = response.data
  } catch (err: any) {
    console.error('Error loading departments:', err)
  }
}

function viewService(service: any) {
  // TODO: Implement service detail view
  console.log('Viewing service:', service)
}

// Watch for route query changes (for department filter from departments page)
watch(() => route.query.department, (newDept) => {
  if (newDept) {
    selectedDepartment.value = String(newDept)
  }
}, { immediate: true })

onMounted(async () => {
  await Promise.all([loadServices(), loadDepartments()])
})
</script>



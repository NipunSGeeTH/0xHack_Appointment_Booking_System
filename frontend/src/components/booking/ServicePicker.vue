<template>
  <div class="service-picker">
    <!-- Department Selection -->
    <div class="department-selection">
      <h4 class="section-title">Select Department</h4>
      <p class="section-description">Choose a government department to see available services</p>
      
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <svg class="w-8 h-8 mx-auto text-blue-600 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
        <p class="text-center text-gray-600 mt-2">Loading available departments...</p>
      </div>
      
      <!-- Department Search -->
      <div v-else-if="departments.length > 0" class="search-section">
        <div class="form-group">
          <label class="form-label">Search Departments</label>
          <input 
            v-model="departmentSearch" 
            placeholder="Search by name, location, or description..." 
            class="form-input"
          />
        </div>
      </div>
      
      <!-- Departments Grid -->
      <div v-if="!loading && departments.length > 0" class="departments-grid">
        <div 
          v-for="dept in filteredDepartments" 
          :key="dept.id" 
          class="department-card"
          :class="{ 'selected': selectedDeptId === dept.id }"
          @click="selectDepartment(dept.id)"
        >
          <div class="department-header">
            <div class="department-icon">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <div class="department-status" :class="dept.is_active ? 'active' : 'inactive'">
              {{ dept.is_active ? 'Active' : 'Inactive' }}
            </div>
          </div>
          
          <div class="department-info">
            <h5 class="department-name">{{ dept.name }}</h5>
            <p class="department-description">{{ dept.description || 'Government services' }}</p>
            
            <div class="department-details">
              <div class="detail-item" v-if="dept.location">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                <span>{{ dept.location }}</span>
              </div>
              
              <div class="detail-item" v-if="dept.operating_hours">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>{{ dept.operating_hours }}</span>
              </div>
              
              <div class="detail-item" v-if="dept.contact_number">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                </svg>
                <span>{{ dept.contact_number }}</span>
              </div>
            </div>
            
            <div class="department-meta">
              <span class="service-count">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
                {{ getServiceCount(dept.id) }} services available
              </span>
            </div>
          </div>
          
          <!-- Department Action Buttons - Bottom Center -->
          <div class="department-actions-bottom">
            <button 
              @click.stop="selectDepartment(dept.id)"
              class="btn btn-primary btn-sm"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 3v7a6 6 0 006 6 6 6 0 006-6V3"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 21v-7a6 6 0 00-6-6 6 6 0 00-6 6v7"></path>
              </svg>
              View Services
            </button>
            <button 
              @click.stop="viewDepartmentDetails(dept)"
              class="btn btn-outline btn-sm"
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
      
      <!-- No Departments Message -->
      <div v-if="!loading && filteredDepartments.length === 0 && departments.length === 0" class="no-departments">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47-.881-6.08-2.33"></path>
        </svg>
        <p>No departments found</p>
        <p class="text-sm text-gray-500 mt-1">The database may not be initialized. Please run the initialization script.</p>
        <button @click="loadDepartments" class="btn btn-outline btn-sm mt-3">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          Retry Loading
        </button>
      </div>
      
      <!-- No Departments Message -->
      <div v-if="!loading && filteredDepartments.length === 0 && departments.length > 0" class="no-departments">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47-.881-6.08-2.33"></path>
        </svg>
        <p>No departments found matching your search criteria</p>
        <button @click="clearDepartmentSearch" class="btn btn-outline btn-sm">
          Clear Search
        </button>
      </div>
      
      <!-- Department Actions -->
      <div class="department-actions" v-if="selectedDeptId > 0">
        <button 
          @click="clearDepartmentSelection" 
          class="btn btn-outline btn-sm"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
          Change Department
        </button>
      </div>
    </div>

    <!-- Service Selection -->
    <div class="service-selection" v-if="selectedDeptId > 0">
      <h4 class="section-title">Available Services</h4>
      <p class="section-description">Select a service from {{ getSelectedDepartmentName() }}</p>
      
      <!-- Service Search -->
      <div class="filters">
        <div class="form-group">
          <label class="form-label">Search Services</label>
          <input 
            v-model="search" 
            placeholder="Search services..." 
            class="form-input"
          />
        </div>
      </div>
    
      <!-- Services Grid -->
      <div class="services-grid">
        <div 
          v-for="service in filtered" 
          :key="service.id" 
          class="service-item"
          :class="{ 'selected': selectedService?.id === service.id }"
          @click="selectService(service)"
        >
          <div class="service-info">
            <h4 class="service-name">{{ service.name }}</h4>
            <p class="service-description">{{ service.description || 'No description available' }}</p>
            <div class="service-meta">
              <span class="service-duration">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                {{ service.duration_minutes }} minutes
              </span>
              <span class="service-capacity">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                </svg>
                Max {{ service.max_daily_appointments }} appointments/day
              </span>
            </div>
            
            <div class="service-requirements" v-if="service.required_documents">
              <h6 class="requirements-title">Required Documents:</h6>
              <p class="requirements-text">{{ service.required_documents }}</p>
            </div>
          </div>
          
          <div class="service-select">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>
      </div>
      
      <!-- No Services Message -->
      <div v-if="filtered.length === 0" class="no-services">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47-.881-6.08-2.33"></path>
        </svg>
        <p>No services found matching your criteria</p>
        <p class="text-sm text-gray-500">Try adjusting your search or selecting a different department</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { api, endpoints } from '../../services/api'

const emit = defineEmits<{
  select: [service: any]
}>()

const departments = ref<any[]>([])
const services = ref<any[]>([])
const selectedDeptId = ref<number>(0)
const search = ref('')
const departmentSearch = ref('')
const selectedService = ref<any>(null)
const loading = ref(false)

// Computed properties
const filteredDepartments = computed(() => {
  if (!departmentSearch.value) return departments.value
  
  const searchTerm = departmentSearch.value.toLowerCase()
  return departments.value.filter(dept => 
    dept.name.toLowerCase().includes(searchTerm) ||
    (dept.description && dept.description.toLowerCase().includes(searchTerm)) ||
    (dept.location && dept.location.toLowerCase().includes(searchTerm))
  )
})

const filtered = computed(() => services.value.filter((s:any) => s.name.toLowerCase().includes(search.value.toLowerCase())))

// Methods
async function loadDepartments(){ 
  loading.value = true
  try {
    const response = await api.get(endpoints.departments.list, {
      params: { active_only: true }
    })
    departments.value = response.data
    console.log('Loaded departments:', departments.value)
  } catch (error) {
    console.error('Error loading departments:', error)
    // Show user-friendly error message
    departments.value = []
  } finally {
    loading.value = false
  }
}

async function loadServices(){
  if (!selectedDeptId.value) {
    services.value = []
    return
  }
  
  loading.value = true
  try {
    const url = endpoints.departments.services(selectedDeptId.value)
    const response = await api.get(url, {
      params: { active_only: true }
    })
    services.value = response.data
    console.log('Loaded services for department', selectedDeptId.value, ':', services.value)
  } catch (error) {
    console.error('Error loading services:', error)
    services.value = []
  } finally {
    loading.value = false
  }
}

function selectDepartment(deptId: number) {
  selectedDeptId.value = deptId
  selectedService.value = null
  search.value = ''
  loadServices()
}

function clearDepartmentSelection() {
  selectedDeptId.value = 0
  selectedService.value = null
  services.value = []
  search.value = ''
}

function clearDepartmentSearch() {
  departmentSearch.value = ''
}

function viewDepartmentDetails(department: any) {
  // Show department details in a modal or expand the card
  console.log('Viewing details for:', department.name)
  // You can implement a modal or expandable view here
  alert(`Department: ${department.name}\nLocation: ${department.location || 'N/A'}\nOperating Hours: ${department.operating_hours || 'N/A'}\nContact: ${department.contact_number || 'N/A'}`)
}

function selectService(service: any) {
  selectedService.value = service
  emit('select', service)
}

function getDepartmentName(departmentId: number) {
  const dept = departments.value.find(d => d.id === departmentId)
  return dept ? dept.name : 'Unknown Department'
}

function getSelectedDepartmentName() {
  return getDepartmentName(selectedDeptId.value)
}

function getServiceCount(departmentId: number) {
  // If services are loaded for this department, return actual count
  if (selectedDeptId.value === departmentId && services.value.length > 0) {
    return services.value.filter(s => s.department_id === departmentId).length
  }
  // Otherwise return a placeholder
  return '...'
}

onMounted(async () => { 
  await loadDepartments()
})
</script>

<style scoped>
.service-picker {
  @apply space-y-6;
}

.section-title {
  @apply text-lg font-semibold text-gray-900 mb-2;
}

.section-description {
  @apply text-sm text-gray-600 mb-4;
}

.loading-state {
  @apply text-center py-8;
}

.search-section {
  @apply mb-4;
}

.departments-grid {
  @apply grid grid-cols-1 md:grid-cols-2 gap-4 mb-4;
}

.department-card {
  @apply border border-gray-200 rounded-lg p-6 cursor-pointer transition-all duration-200 hover:border-blue-300 hover:shadow-lg flex flex-col bg-white;
}

.department-card.selected {
  @apply border-blue-500 bg-blue-50 shadow-md;
}

.department-header {
  @apply flex justify-between items-start mb-4;
}

.department-icon {
  @apply text-blue-600 bg-blue-100 p-2 rounded-lg;
}

.department-status {
  @apply text-xs px-2 py-1 rounded-full font-medium;
}

.department-status.active {
  @apply bg-green-100 text-green-800;
}

.department-status.inactive {
  @apply bg-red-100 text-red-800;
}

.department-info {
  @apply flex-1 flex flex-col;
}

.department-name {
  @apply text-lg font-bold text-gray-900 mb-3;
}

.department-description {
  @apply text-sm text-gray-600 mb-3;
}

.department-details {
  @apply space-y-2 mb-3;
}

.detail-item {
  @apply flex items-center gap-2 text-xs text-gray-500;
}

.department-meta {
  @apply flex items-center gap-2 text-xs text-blue-600 font-medium mt-auto;
}

.service-count {
  @apply flex items-center gap-1;
}

.no-departments {
  @apply text-center py-8 text-gray-500;
}

.department-actions {
  @apply flex justify-center items-center gap-3;
}

.service-selection {
  @apply border-t pt-6;
}

.filters {
  @apply mb-4;
}

.services-grid {
  @apply space-y-3;
}

.service-item {
  @apply border border-gray-200 rounded-lg p-4 cursor-pointer transition-all duration-200 hover:border-blue-300 hover:shadow-md;
}

.service-item.selected {
  @apply border-blue-500 bg-blue-50 shadow-md;
}

.service-info {
  @apply flex-1;
}

.service-name {
  @apply text-base font-semibold text-gray-900 mb-2;
}

.service-description {
  @apply text-sm text-gray-600 mb-3;
}

.service-meta {
  @apply flex flex-wrap gap-4 mb-3;
}

.service-duration,
.service-capacity {
  @apply flex items-center gap-1 text-xs text-gray-600;
}

.service-requirements {
  @apply mt-3 p-3 bg-gray-50 rounded-md;
}

.requirements-title {
  @apply text-sm font-medium text-gray-700 mb-1;
}

.requirements-text {
  @apply text-xs text-gray-600;
}

.service-select {
  @apply text-blue-600;
}

.no-services {
  @apply text-center py-8 text-gray-500;
}

.form-group {
  @apply mb-4;
}

.form-label {
  @apply block text-sm font-medium text-gray-700 mb-2;
}

.form-input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent;
}

.btn {
  @apply inline-flex items-center justify-center gap-2 px-4 py-2 rounded-md font-medium transition-colors duration-200;
}

.btn-outline {
  @apply border border-gray-300 text-gray-700 hover:bg-gray-50;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2;
}

.btn-sm {
  @apply px-3 py-1.5 text-sm;
}

/* Ensure consistent button heights and alignment */
.department-actions .btn {
  @apply min-h-[40px] flex-shrink-0;
}

/* Department action buttons styling - Bottom Center */
.department-actions-bottom {
  @apply flex gap-3 mt-4 justify-center mt-auto pt-4;
}

.department-actions-bottom .btn {
  @apply justify-center items-center min-h-[40px] text-sm px-4 py-2.5 font-medium;
}

.department-actions-bottom .btn-sm {
  @apply px-4 py-2.5;
}

/* Ensure buttons are perfectly aligned */
.department-actions-bottom .btn svg {
  @apply flex-shrink-0;
}

/* Primary button styling to match the image */
.department-actions-bottom .btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 shadow-sm;
}

/* Outline button styling to match the image */
.department-actions-bottom .btn-outline {
  @apply border border-gray-300 text-gray-700 hover:bg-gray-50 bg-white;
}
</style>



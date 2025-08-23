<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Book Appointment</h1>
      <p class="page-subtitle">Schedule your government service appointment</p>
    </div>

    <div class="booking-container">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Service Selection -->
        <div class="card">
          <div class="card-header">
            <h3>Select Service</h3>
            <p>First choose a department, then select the service you need</p>
          </div>
          <div class="card-body">
            <ServicePicker @select="onService" />
          </div>
        </div>

        <!-- Date & Time Selection -->
        <div class="card">
          <div class="card-header">
            <h3>Select Date & Time</h3>
            <p>Pick your preferred appointment slot</p>
          </div>
          <div class="card-body">
            <div v-if="!serviceId" class="no-service-selected">
              <svg class="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              <p class="text-center text-gray-500 mt-2">Please select a service first to see available time slots</p>
            </div>
            <DateTimePicker v-else :serviceId="serviceId" @select="onSelectSlot" />
          </div>
        </div>
      </div>

      <!-- Appointment Details -->
      <div class="card mt-8">
        <div class="card-header">
          <h3>Appointment Details</h3>
          <p>Add any additional notes for your appointment</p>
        </div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">Additional Notes</label>
            <textarea 
              v-model="notes" 
              class="form-textarea"
              placeholder="Any special requirements or notes for your appointment..."
              rows="4"
            ></textarea>
          </div>
          
          <div class="booking-summary" v-if="selectedService || selectedSlot">
            <h4>Booking Summary</h4>
            <div class="summary-item" v-if="selectedService">
              <span class="summary-label">Service:</span>
              <span class="summary-value">{{ selectedService.name }}</span>
            </div>
            <div class="summary-item" v-if="selectedService">
              <span class="summary-label">Department:</span>
              <span class="summary-value">{{ selectedService.department_name || 'Unknown Department' }}</span>
            </div>
            <div class="summary-item" v-if="selectedService">
              <span class="summary-label">Duration:</span>
              <span class="summary-value">{{ selectedService.duration_minutes }} minutes</span>
            </div>
            <div class="summary-item" v-if="selectedSlot">
              <span class="summary-label">Date & Time:</span>
              <span class="summary-value">{{ selectedSlot.date }} at {{ selectedSlot.time }}</span>
            </div>
            <div class="summary-item" v-if="selectedService?.required_documents">
              <span class="summary-label">Required Documents:</span>
              <span class="summary-value text-sm text-gray-600">{{ selectedService.required_documents }}</span>
            </div>
          </div>
          
          <div class="booking-actions">
            <button 
              class="btn btn-primary btn-lg" 
              :disabled="!time_slot_id || !serviceId || loading"
              @click="book"
            >
              <span v-if="loading" class="loading"></span>
              <span v-else>
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                Book Appointment
              </span>
            </button>
          </div>
          
          <div v-if="message" class="alert" :class="messageType === 'success' ? 'alert-success' : 'alert-error'">
            <svg v-if="messageType === 'success'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            {{ message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { api, endpoints } from '../services/api'
import ServicePicker from '../components/booking/ServicePicker.vue'
import DateTimePicker from '../components/booking/DateTimePicker.vue'

const serviceId = ref<number | null>(null)
const notes = ref('')
const time_slot_id = ref<number | null>(null)
const message = ref<string | null>(null)
const messageType = ref<'success' | 'error'>('success')
const loading = ref(false)
const selectedService = ref<any>(null)
const selectedSlot = ref<any>(null)

function onService(service: any) { 
  serviceId.value = service.id 
  selectedService.value = service
  // Reset time slot when service changes
  time_slot_id.value = null
  selectedSlot.value = null
}

function onSelectSlot(slot: { time_slot_id: number, date: string, time: string }) { 
  time_slot_id.value = slot.time_slot_id 
  selectedSlot.value = slot
}

async function book() {
  if (!serviceId.value || !time_slot_id.value) return
  
  loading.value = true
  message.value = null
  
  try {
    await api.post(endpoints.appointments.create, {
      service_id: serviceId.value,
      time_slot_id: time_slot_id.value,
      notes: notes.value,
    })
    message.value = 'Appointment booked successfully! You will receive a confirmation email shortly.'
    messageType.value = 'success'
    
    // Reset form
    serviceId.value = null
    time_slot_id.value = null
    notes.value = ''
    selectedService.value = null
    selectedSlot.value = null
  } catch (e: any) {
    message.value = e?.response?.data?.detail || 'Booking failed. Please try again.'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}
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

.booking-container {
  @apply space-y-8;
}

.card {
  @apply bg-white rounded-lg shadow-md border border-gray-200;
}

.card-header {
  @apply px-6 py-4 border-b border-gray-200;
}

.card-header h3 {
  @apply text-lg font-semibold text-gray-900 mb-1;
}

.card-header p {
  @apply text-sm text-gray-600;
}

.card-body {
  @apply p-6;
}

.no-service-selected {
  @apply text-center py-12;
}

.form-group {
  @apply mb-4;
}

.form-label {
  @apply block text-sm font-medium text-gray-700 mb-2;
}

.form-textarea {
  @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none;
}

.booking-summary {
  @apply bg-gray-50 rounded-lg p-4 mb-6;
}

.booking-summary h4 {
  @apply text-lg font-semibold text-gray-900 mb-3;
}

.summary-item {
  @apply flex justify-between items-start py-2 border-b border-gray-200 last:border-b-0;
}

.summary-label {
  @apply font-medium text-gray-700;
}

.summary-value {
  @apply text-gray-900 text-right;
}

.booking-actions {
  @apply flex justify-center;
}

.btn {
  @apply inline-flex items-center gap-2 px-6 py-3 rounded-md font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2;
}

.btn-primary:disabled {
  @apply bg-gray-400 cursor-not-allowed;
}

.btn-lg {
  @apply px-8 py-3 text-lg;
}

.loading {
  @apply inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin;
}

.alert {
  @apply flex items-center gap-3 p-4 rounded-md mt-4;
}

.alert-success {
  @apply bg-green-50 text-green-800 border border-green-200;
}

.alert-error {
  @apply bg-red-50 text-red-800 border border-red-200;
}

.alert svg {
  @apply flex-shrink-0;
}

/* Department card styles to match services page */
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

.department-actions-bottom {
  @apply flex gap-3 mt-4 justify-center mt-auto pt-4;
}

.department-actions-bottom .btn {
  @apply justify-center items-center min-h-[40px] text-sm px-4 py-2.5 font-medium;
}

.department-actions-bottom .btn-sm {
  @apply px-4 py-2.5;
}

.department-actions-bottom .btn svg {
  @apply flex-shrink-0;
}

.department-actions-bottom .btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 shadow-sm;
}

.department-actions-bottom .btn-outline {
  @apply border border-gray-300 text-gray-700 hover:bg-gray-50 bg-white;
}
</style>



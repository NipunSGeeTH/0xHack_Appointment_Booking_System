<template>
  <div class="datetime-picker">
    <div class="date-selection">
      <label class="form-label">Select Date</label>
      <input 
        type="date" 
        v-model="date" 
        @change="fetchSlots"
        class="form-input"
        :min="minDate"
        :max="maxDate"
      />
    </div>
    
    <div class="time-slots" v-if="date">
      <label class="form-label">Available Time Slots</label>
      
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading"></div>
        <p>Loading available slots...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <p>{{ error }}</p>
        <button @click="fetchSlots" class="btn btn-sm btn-outline">Try Again</button>
      </div>
      
      <!-- Time Slots Grid -->
      <div v-else-if="slots.length > 0" class="slots-grid">
        <button 
          v-for="slot in slots" 
          :key="slot.id" 
          :class="{ 
            'slot-button': true,
            'selected': selected === slot.id 
          }" 
          @click="selectSlot(slot)"
        >
          <div class="slot-time">
            <span class="start-time">{{ formatTime(slot.start_time) }}</span>
            <span class="time-separator">-</span>
            <span class="end-time">{{ formatTime(slot.end_time) }}</span>
          </div>
          <div class="slot-status">
            <span class="status-indicator available"></span>
            Available
          </div>
        </button>
      </div>
      
      <!-- No Slots Available -->
      <div v-else class="no-slots">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <p>No available slots for this date</p>
        <p class="text-sm">Please select a different date or try again later</p>
      </div>
    </div>
    
    <!-- Selected Slot Summary -->
    <div v-if="selectedSlot" class="selected-summary">
      <h4>Selected Appointment</h4>
      <div class="summary-details">
        <div class="summary-item">
          <span class="summary-label">Date:</span>
          <span class="summary-value">{{ formatDate(date) }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Time:</span>
          <span class="summary-value">
            {{ formatTime(selectedSlot.start_time) }} - {{ formatTime(selectedSlot.end_time) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import dayjs from 'dayjs'
import { api, endpoints } from '../../services/api'

const props = defineProps<{ serviceId: number | null }>()
const emit = defineEmits<{ (e:'select', payload: { time_slot_id: number, date: string, time: string }): void }>()

const date = ref('')
const slots = ref<any[]>([])
const selected = ref<number | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

// Date constraints (today to 30 days from now)
const minDate = computed(() => dayjs().format('YYYY-MM-DD'))
const maxDate = computed(() => dayjs().add(30, 'day').format('YYYY-MM-DD'))

const selectedSlot = computed(() => {
  return slots.value.find(slot => slot.id === selected.value)
})

function formatTime(timeString: string) {
  return dayjs(timeString).format('HH:mm')
}

function formatDate(dateString: string) {
  return dayjs(dateString).format('dddd, MMMM D, YYYY')
}

async function fetchSlots() {
  if (!props.serviceId || !date.value) {
    slots.value = []
    selected.value = null
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get(
      `${endpoints.appointments.timeSlotsAvailable(props.serviceId)}?date=${new Date(date.value).toISOString()}`
    )
    slots.value = response.data
    selected.value = null // Reset selection when date changes
  } catch (err: any) {
    error.value = err?.response?.data?.detail || 'Failed to load time slots'
    console.error('Error loading time slots:', err)
  } finally {
    loading.value = false
  }
}

function selectSlot(slot: any) {
  selected.value = slot.id
  emit('select', { 
    time_slot_id: slot.id, 
    date: date.value,
    time: `${formatTime(slot.start_time)} - ${formatTime(slot.end_time)}`
  })
}

// Watch for service ID changes
watch(() => props.serviceId, () => {
  date.value = ''
  slots.value = []
  selected.value = null
  error.value = null
})
</script>



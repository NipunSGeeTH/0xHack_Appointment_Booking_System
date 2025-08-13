<template>
  <div>
    <h2>Book Appointment</h2>
    <div class="grid two">
      <ServicePicker @select="onService" />
      <DateTimePicker :serviceId="serviceId" @select="onSelectSlot" />
    </div>
    <div class="card">
      <label>Notes</label>
      <input v-model="notes" />
      <button :disabled="!time_slot_id || !serviceId" @click="book">Book Appointment</button>
      <div v-if="message" class="info">{{ message }}</div>
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

function onService(s:any){ serviceId.value = s.id }
function onSelectSlot(p: { time_slot_id:number, date:string }){ time_slot_id.value = p.time_slot_id }

async function book() {
  if (!serviceId.value || !time_slot_id.value) return
  try {
    await api.post(endpoints.appointments.create, {
      service_id: serviceId.value,
      time_slot_id: time_slot_id.value,
      notes: notes.value,
    })
    message.value = 'Appointment booked successfully'
  } catch (e: any) {
    message.value = e?.response?.data?.detail || 'Booking failed'
  }
}
</script>



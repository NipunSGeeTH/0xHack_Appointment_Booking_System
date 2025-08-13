<template>
  <div class="card">
    <h3>Time Slots</h3>
    <form class="grid two" @submit.prevent="createRecurring">
      <div>
        <label>Service ID</label>
        <input v-model.number="service_id" />
        <label>Start Date</label>
        <input type="date" v-model="start_date" />
        <label>End Date</label>
        <input type="date" v-model="end_date" />
      </div>
      <div>
        <label>Start Time</label>
        <input placeholder="09:00" v-model="start_time" />
        <label>End Time</label>
        <input placeholder="12:00" v-model="end_time" />
        <label>Duration (min)</label>
        <input v-model.number="duration_minutes" />
        <button type="submit">Create Recurring Slots</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../../services/api'

const service_id = ref<number | null>(null)
const start_date = ref('')
const end_date = ref('')
const start_time = ref('09:00')
const end_time = ref('12:00')
const duration_minutes = ref(30)

async function createRecurring(){
  if(!service_id.value) return
  await api.post('/appointments/time-slots/recurring', {
    service_id: service_id.value,
    start_date: new Date(start_date.value).toISOString(),
    end_date: new Date(end_date.value).toISOString(),
    start_time: start_time.value,
    end_time: end_time.value,
    duration_minutes: duration_minutes.value,
  })
  alert('Time slots created')
}
</script>



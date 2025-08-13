<template>
  <div class="card">
    <h3>Select Date & Time</h3>
    <div class="grid two">
      <div>
        <label>Date</label>
        <input type="date" v-model="date" @change="fetch" />
      </div>
      <div>
        <label>Available Slots</label>
        <div class="grid">
          <button v-for="s in slots" :key="s.id" :class="{ selected: selected===s.id }" @click="select(s)">
            {{ time(s.start_time) }} - {{ time(s.end_time) }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import dayjs from 'dayjs'
import { api, endpoints } from '../../services/api'

const props = defineProps<{ serviceId: number | null }>()
const emit = defineEmits<{ (e:'select', payload: { time_slot_id:number, date:string }): void }>()
const date = ref('')
const slots = ref<any[]>([])
const selected = ref<number | null>(null)

function time(v: string){ return dayjs(v).format('HH:mm') }

async function fetch(){
  if(!props.serviceId || !date.value){ slots.value = []; return }
  const res = await api.get(`${endpoints.appointments.timeSlotsAvailable(props.serviceId)}?date=${new Date(date.value).toISOString()}`)
  slots.value = res.data
}

function select(s:any){ selected.value = s.id; emit('select', { time_slot_id: s.id, date: date.value }) }

watch(() => props.serviceId, fetch)
</script>



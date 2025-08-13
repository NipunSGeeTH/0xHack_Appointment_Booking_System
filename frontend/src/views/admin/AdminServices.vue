<template>
  <div class="card">
    <h3>Services</h3>
    <form class="grid two" @submit.prevent="save">
      <div>
        <label>Department ID</label>
        <input v-model.number="form.department_id" />
        <label>Name</label>
        <input v-model="form.name" />
      </div>
      <div>
        <label>Duration (min)</label>
        <input v-model.number="form.duration_minutes" />
        <label>Max Daily</label>
        <input v-model.number="form.max_daily_appointments" />
        <button type="submit">Save</button>
      </div>
    </form>
    <hr />
    <ul>
      <li v-for="s in items" :key="s.id">{{ s.name }} – Dept: {{ s.department_id }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { api, endpoints } from '../../services/api'

const items = ref<any[]>([])
const form = reactive<any>({ department_id: null, name: '', duration_minutes: 30, max_daily_appointments: 50 })

async function load(){ items.value = (await api.get(endpoints.services.list)).data }
async function save(){ await api.post('/services', form); await load() }

onMounted(load)
</script>



<template>
  <div>
    <h2>Services</h2>
    <div class="toolbar">
      <input placeholder="Filter by Department ID" v-model="deptId" />
      <button @click="load">Load</button>
    </div>
    <div class="grid">
      <div v-for="s in data" :key="s.id" class="card">
        <h3>{{ s.name }}</h3>
        <p>{{ s.description }}</p>
        <small>Duration: {{ s.duration_minutes }} min</small>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, endpoints } from '../services/api'

const data = ref<any[]>([])
const deptId = ref<string>('')

async function load() {
  const url = deptId.value ? endpoints.services.byDepartment(Number(deptId.value)) : endpoints.services.list
  const res = await api.get(url)
  data.value = res.data
}

onMounted(load)
</script>



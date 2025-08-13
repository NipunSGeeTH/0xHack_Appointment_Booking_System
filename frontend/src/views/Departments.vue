<template>
  <div>
    <h2>Departments</h2>
    <div class="grid">
      <div v-for="d in data" :key="d.id" class="card">
        <h3>{{ d.name }}</h3>
        <p>{{ d.description }}</p>
        <small>{{ d.location }}</small>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, endpoints } from '../services/api'

const data = ref<any[]>([])
onMounted(async () => {
  const res = await api.get(endpoints.departments.list)
  data.value = res.data
})
</script>



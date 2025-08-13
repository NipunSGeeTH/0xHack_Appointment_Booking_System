<template>
  <div class="card">
    <h3>Analytics Overview</h3>
    <pre>{{ data }}</pre>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api, endpoints } from '../../services/api'

const data = ref<any>(null)
onMounted(async () => { data.value = (await api.get(endpoints.analytics.overview)).data })
</script>



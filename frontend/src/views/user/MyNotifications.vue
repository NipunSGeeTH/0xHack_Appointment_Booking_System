<template>
  <div class="card">
    <h3>Notifications</h3>
    <ul>
      <li v-for="n in items" :key="n.id">{{ n.title }} – {{ n.is_read ? 'Read' : 'New' }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api, endpoints } from '../../services/api'

const items = ref<any[]>([])
onMounted(async () => { items.value = (await api.get(endpoints.notifications.mine)).data })
</script>



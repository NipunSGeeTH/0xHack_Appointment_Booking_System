<template>
  <div>
    <h2>My Dashboard</h2>
    <div class="grid three">
      <div class="card">
        <h3>Upcoming Appointments</h3>
        <ul>
          <li v-for="a in appointments" :key="a.id">
            {{ a.service?.name || a.service_id }} –
            {{ a.time_slot?.start_time ? new Date(a.time_slot.start_time).toLocaleString() : '' }} –
            {{ a.status }}
          </li>
        </ul>
      </div>
      <div class="card">
        <h3>Documents</h3>
        <ul>
          <li v-for="d in docs" :key="d.id">{{ d.document_type }} – {{ d.is_verified ? 'Verified' : 'Pending' }}</li>
        </ul>
      </div>
      <div class="card">
        <h3>Notifications</h3>
        <ul>
          <li v-for="n in notifications" :key="n.id">{{ n.title }} – {{ n.is_read ? 'Read' : 'New' }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api, endpoints } from '../services/api'

const appointments = ref<any[]>([])
const docs = ref<any[]>([])
const notifications = ref<any[]>([])

onMounted(async () => {
  appointments.value = (await api.get(endpoints.appointments.mine)).data
  docs.value = (await api.get(endpoints.documents.mine)).data
  notifications.value = (await api.get(endpoints.notifications.mine)).data
})
</script>



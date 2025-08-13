<template>
  <div class="card">
    <h3>My Appointments</h3>
    <ul>
      <li v-for="a in items" :key="a.id">
        Ref {{ a.booking_reference }} – {{ a.status }} –
        {{ a.time_slot?.start_time ? new Date(a.time_slot.start_time).toLocaleString() : '' }}
        <QRCodeVue :value="`SL-GOV-${a.booking_reference}-${a.id}`" :size="96" />
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api, endpoints } from '../../services/api'
// @ts-ignore
import QRCodeVue from 'qrcode.vue'

const items = ref<any[]>([])
onMounted(async () => { items.value = (await api.get(endpoints.appointments.mine)).data })
</script>



<template>
  <div class="card">
    <h3>Department/Service Appointments</h3>
    <div class="grid two">
      <div>
        <label>Service ID</label>
        <input v-model.number="serviceId" />
        <button @click="loadByService">Load by Service</button>
      </div>
      <div>
        <label>Department ID</label>
        <input v-model.number="departmentId" />
        <button @click="loadByDepartment">Load by Department</button>
      </div>
    </div>
    <ul>
      <li v-for="a in items" :key="a.id">
        {{ a.id }} – {{ a.status }} – Service {{ a.service_id }} – User {{ a.user_id }}
        <select v-model="a._new">
          <option value="confirmed">CONFIRMED</option>
          <option value="completed">COMPLETED</option>
          <option value="cancelled">CANCELLED</option>
          <option value="no_show">NO_SHOW</option>
        </select>
        <button @click="updateStatus(a.id, a._new)">Update</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../../services/api'

const items = ref<any[]>([])
const serviceId = ref<number | null>(null)
const departmentId = ref<number | null>(null)

async function loadByService(){ if(serviceId.value) items.value = (await api.get(`/appointments/service/${serviceId.value}`)).data }
async function loadByDepartment(){ if(departmentId.value) items.value = (await api.get(`/appointments/department/${departmentId.value}`)).data }
async function updateStatus(id: number, new_status: string){
  if(!new_status) return
  await api.put(`/appointments/${id}/status?new_status=${encodeURIComponent(new_status)}`)
  if(serviceId.value) await loadByService()
  else if(departmentId.value) await loadByDepartment()
}
</script>



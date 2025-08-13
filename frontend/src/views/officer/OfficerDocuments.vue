<template>
  <div class="card">
    <h3>Verify Documents</h3>
    <div class="toolbar">
      <label>Appointment ID</label>
      <input v-model.number="appointmentId" />
      <button @click="load">Load</button>
    </div>
    <ul>
      <li v-for="d in items" :key="d.id">
        {{ d.document_type }} – {{ d.file_name }} – {{ d.is_verified ? 'Verified' : 'Pending' }}
        <button @click="verify(d.id)" v-if="!d.is_verified">Mark Verified</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../../services/api'

const items = ref<any[]>([])
const appointmentId = ref<number | null>(null)

async function load(){ if(appointmentId.value) items.value = (await api.get(`/documents/appointment/${appointmentId.value}`)).data }
async function verify(id: number){ await api.put(`/documents/${id}/verify`); await load() }
</script>



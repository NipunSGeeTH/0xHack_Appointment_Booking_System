<template>
  <div class="card">
    <h3>My Documents</h3>
    <form @submit.prevent="upload">
      <label>Document Type</label>
      <input v-model="docType" />
      <label>Appointment ID (optional)</label>
      <input v-model.number="appointmentId" />
      <input type="file" @change="onFile" />
      <button type="submit">Upload</button>
    </form>
    <hr />
    <ul>
      <li v-for="d in items" :key="d.id">{{ d.document_type }} – {{ d.file_name }} – {{ d.is_verified ? 'Verified' : 'Pending' }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api, endpoints } from '../../services/api'

const items = ref<any[]>([])
const docType = ref('')
const appointmentId = ref<number | null>(null)
const file = ref<File | null>(null)

function onFile(e: Event){
  const t = e.target as HTMLInputElement
  file.value = t.files && t.files[0] ? t.files[0] : null
}

async function upload(){
  if(!file.value || !docType.value) return
  const form = new FormData()
  form.append('file', file.value)
  form.append('document_type', docType.value)
  if(appointmentId.value) form.append('appointment_id', String(appointmentId.value))
  await api.post(endpoints.documents.upload, form, { headers: { 'Content-Type': 'multipart/form-data' }})
  await load()
}

async function load(){ items.value = (await api.get(endpoints.documents.mine)).data }
onMounted(load)
</script>



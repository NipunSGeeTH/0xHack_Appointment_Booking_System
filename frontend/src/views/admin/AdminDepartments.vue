<template>
  <div class="card">
    <h3>Departments</h3>
    <form class="grid two" @submit.prevent="save">
      <div>
        <label>Name</label>
        <input v-model="form.name" />
        <label>Description</label>
        <input v-model="form.description" />
      </div>
      <div>
        <label>Location</label>
        <input v-model="form.location" />
        <label>Contact</label>
        <input v-model="form.contact_number" />
        <button type="submit">Save</button>
      </div>
    </form>
    <hr />
    <ul>
      <li v-for="d in items" :key="d.id">{{ d.name }} – {{ d.is_active ? 'Active' : 'Inactive' }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { api, endpoints } from '../../services/api'

const items = ref<any[]>([])
const form = reactive<any>({ name: '', description: '', location: '', contact_number: '' })

async function load(){ items.value = (await api.get(endpoints.departments.list)).data }
async function save(){ await api.post('/departments', form); await load() }

onMounted(load)
</script>



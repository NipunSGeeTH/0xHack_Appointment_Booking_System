<template>
  <div class="card">
    <h3>Select Service</h3>
    <div class="grid two">
      <div>
        <label>Department</label>
        <select v-model.number="selectedDeptId" @change="loadServices">
          <option :value="0">All Departments</option>
          <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
        </select>
      </div>
      <div>
        <label>Search</label>
        <input v-model="search" placeholder="Search services" />
      </div>
    </div>
    <div class="grid">
      <button v-for="s in filtered" :key="s.id" @click="$emit('select', s)">
        {{ s.name }} <small>({{ s.duration_minutes }} min)</small>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { api, endpoints } from '../../services/api'

const departments = ref<any[]>([])
const services = ref<any[]>([])
const selectedDeptId = ref<number>(0)
const search = ref('')

async function loadDepartments(){ departments.value = (await api.get(endpoints.departments.list)).data }
async function loadServices(){
  const url = selectedDeptId.value ? endpoints.services.byDepartment(selectedDeptId.value) : endpoints.services.list
  services.value = (await api.get(url)).data
}

const filtered = computed(() => services.value.filter((s:any) => s.name.toLowerCase().includes(search.value.toLowerCase())))

onMounted(async () => { await loadDepartments(); await loadServices() })
</script>



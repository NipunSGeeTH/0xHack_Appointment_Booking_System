<template>
  <div class="card">
    <h3>Users</h3>
    <div class="toolbar">
      <input v-model="search" placeholder="Search users (name/username/email/NIC)" />
      <button @click="doSearch">Search</button>
      <button @click="load">Refresh</button>
    </div>
    <div class="grid two">
      <div>
        <h4>All Users</h4>
        <ul>
          <li v-for="u in users" :key="u.id">
            {{ u.username }} ({{ u.role }}) – {{ u.is_active ? 'Active' : 'Inactive' }}
            <button @click="toggleActive(u)">{{ u.is_active ? 'Deactivate' : 'Activate' }}</button>
            <select v-model="u._role">
              <option value="citizen">citizen</option>
              <option value="government_officer">government_officer</option>
              <option value="admin">admin</option>
            </select>
            <button @click="changeRole(u)">Change Role</button>
            <button @click="resetPwd(u)">Reset Password</button>
          </li>
        </ul>
      </div>
      <div>
        <h4>Statistics</h4>
        <pre>{{ stats }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '../../services/api'

const users = ref<any[]>([])
const stats = ref<any>(null)
const search = ref('')

async function load(){
  // Admin endpoint returns citizens by default in our earlier controller, but fallback list is OK
  users.value = (await api.get('/users?skip=0&limit=100')).data.map((u:any)=>({ ...u, _role: u.role }))
  stats.value = (await api.get('/users/statistics/dashboard')).data
}

async function doSearch(){ if(!search.value) return load(); users.value = (await api.get(`/users/search/${encodeURIComponent(search.value)}?skip=0&limit=100`)).data }
async function toggleActive(u:any){ const path = u.is_active ? 'deactivate' : 'activate'; await api.put(`/users/${u.id}/${path}`); await load() }
async function changeRole(u:any){ await api.put(`/users/${u.id}/role?new_role=${u._role}`); await load() }
async function resetPwd(u:any){ const np = prompt('New password for '+u.username); if(!np) return; await api.post(`/users/${u.id}/reset-password?new_password=${encodeURIComponent(np)}`); alert('Password reset') }

onMounted(load)
</script>



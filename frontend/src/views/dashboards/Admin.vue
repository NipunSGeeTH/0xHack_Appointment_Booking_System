<template>
  <div>
    <h2>Admin Dashboard</h2>
    <div class="grid three">
      <router-link class="card" to="/dashboard/admin/users"><h3>Manage Users</h3></router-link>
      <router-link class="card" to="/dashboard/admin/departments"><h3>Manage Departments</h3></router-link>
      <router-link class="card" to="/dashboard/admin/services"><h3>Manage Services</h3></router-link>
      <router-link class="card" to="/dashboard/admin/time-slots"><h3>Manage Time Slots</h3></router-link>
      <router-link class="card" to="/dashboard/admin/analytics"><h3>Analytics</h3></router-link>
    </div>
    <router-view />
  </div>
</template>



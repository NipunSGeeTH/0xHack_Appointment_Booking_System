<template>
  <div>
    <h2>Government Officer Dashboard</h2>
    <div class="grid two">
      <router-link class="card" to="/dashboard/officer/appointments"><h3>Appointments</h3></router-link>
      <router-link class="card" to="/dashboard/officer/documents"><h3>Documents</h3></router-link>
    </div>
    <router-view />
  </div>
</template>



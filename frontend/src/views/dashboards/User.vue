<template>
  <div>
    <h2>My Dashboard</h2>
    <div class="grid two">
      <router-link class="card" to="/book"><h3>Book an Appointment</h3></router-link>
      <router-link class="card" to="/dashboard/user/appointments"><h3>My Appointments</h3></router-link>
      <router-link class="card" to="/dashboard/user/documents"><h3>My Documents</h3></router-link>
      <router-link class="card" to="/dashboard/user/notifications"><h3>Notifications</h3></router-link>
      <router-link class="card" to="/dashboard/user/feedback"><h3>Feedback</h3></router-link>
    </div>
    <router-view />
  </div>
</template>



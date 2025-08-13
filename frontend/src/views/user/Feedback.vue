<template>
  <div class="card">
    <h3>Submit Feedback</h3>
    <form @submit.prevent="submit">
      <label>Appointment ID</label>
      <input v-model.number="appointmentId" />
      <label>Rating (1-5)</label>
      <input v-model.number="rating" />
      <label>Comment</label>
      <input v-model="comment" />
      <button type="submit">Send</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../../services/api'

const appointmentId = ref<number | null>(null)
const rating = ref(5)
const comment = ref('')

async function submit(){
  await api.post('/feedback', { appointment_id: appointmentId.value, rating: rating.value, comment: comment.value })
  alert('Feedback submitted')
}
</script>



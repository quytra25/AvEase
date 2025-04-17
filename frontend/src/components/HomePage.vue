<script setup>
import { ref } from 'vue'
import WeeklyAvailabilityForm from './WeeklyAvailabilityForm.vue'
import SingleDayAvailabilityForm from './SingleDayAvailabilityForm.vue'
import MultiDayAvailabilityForm from './MultiDayAvailabilityForm.vue'

const selectedForm = ref('weekly')
</script>

<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold">Submit Your Availability</h1>

    <select v-model="selectedForm" class="border px-2 py-1">
      <option value="weekly">Weekly</option>
      <option value="single">Single-Day</option>
      <option value="multi">Multi-Day</option>
    </select>

    <div v-if="selectedForm === 'weekly'">
      <WeeklyAvailabilityForm />
    </div>

    <div v-else-if="selectedForm === 'single'">
      <SingleDayAvailabilityForm />
    </div>

    <div v-else-if="selectedForm === 'multi'">
      <MultiDayAvailabilityForm />
    </div>
  </div>
</template>

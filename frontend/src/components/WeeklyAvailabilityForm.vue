<script setup>
import { ref } from 'vue'
import axios from 'axios'

const participantId = 1  // Replace this dynamically later
const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

const availabilityInputs = ref(
    weekdays.map(day => ({
        day,
        selected: false,
        start_time: '',
        end_time: ''
    }))
)

const submitAvailability = async () => {
    try {
        for (const entry of availabilityInputs.value) {
            if (entry.selected) {
                await axios.post('http://localhost:8000/api/availabilities/weekly/', {
                participant: participantId,
                day: entry.day,
                start_time: entry.start_time,
                end_time: entry.end_time,
                availability_type: 'weekly'
                })
            }
        }
        alert('Availability submitted successfully!')
    } catch (err) {
        console.error(err)
        alert('Something went wrong')
    }
}
</script>

<template>
    <div class="space-y-4">
        <h2 class="text-xl font-bold">Submit Weekly Availability</h2>
        <form @submit.prevent="submitAvailability">
            <div v-for="entry in availabilityInputs" :key="entry.day" class="flex items-center gap-4">
                <label>
                    <input type="checkbox" v-model="entry.selected" />
                    {{ entry.day }}
                </label>
                <input type="time" v-model="entry.start_time" />
                    <span>to</span>
                <input type="time" v-model="entry.end_time" />
            </div>
            <button type="submit" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">Submit</button>
        </form>
    </div>
</template>

<style scoped>
input[type="time"] {
  padding: 2px;
}
</style>

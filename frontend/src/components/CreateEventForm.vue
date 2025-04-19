<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

import WeeklyFields from './WeeklyFields.vue'
import SingleDayFields from './SingleDayFields.vue'
import MultiDayFields from './MultiDayFields.vue'

const fieldMap = {
  weekly: WeeklyFields,
  single: SingleDayFields,
  multi: MultiDayFields
}

const dynamicFieldsComponent = computed(() => fieldMap[subtype.value])

const router = useRouter()

const eventType = ref('availability_match')
const subtype = ref('weekly')

const name = ref('')
const description = ref('')
const location = ref('')

// dynamic form fields per subtype
const subtypeFields = ref({
    days: [],
    start_time: '',
    end_time: '',
    start_date: '',
    end_date: '',
    num_days: ''
})

const submit = async () => {
    const endpointMap = {
        weekly: 'events/weekly/',
        single: 'events/single/',
        multi: 'events/multi/',
    }

    const endpoint = `http://localhost:8000/api/${endpointMap[subtype.value]}`

    // Combine static and dynamic form data
    const payload = {
        name: name.value,
        type: eventType.value,
        description: description.value,
        location: location.value,
        ...subtypeFields.value
    }

    const res = await axios.post(endpoint, payload)
    router.push(`/event/${res.data.link}`)
}
</script>

<template>
    <div>
        <p class="text-gray-500 mb-4 text-sm text-center">
            Fields will adjust automatically based on your selection.
        </p>

        <form @submit.prevent="submit" class="space-y-4">
            <!-- Event Type -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Event Type</label>
                <select v-model="eventType" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200">
                    <option value="availability_match">Availability Match</option>
                    <option value="rsvp_based">RSVP Based</option>
                </select>
            </div>

            <!-- Subtype -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Event Subtype</label>
                <select v-model="subtype" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200">
                    <option value="weekly">Weekly</option>
                    <option value="single">Single-Day</option>
                    <option value="multi">Multi-Day</option>
                </select>
            </div>

            <!-- Name -->
            <input v-model="name" placeholder="Event name" class="w-full border border-gray-300 rounded px-3 py-2" />

            <!-- Location -->
            <input v-model="location" placeholder="Location (optional)" class="w-full border border-gray-300 rounded px-3 py-2" />

            <!-- Description -->
            <textarea v-model="description" placeholder="Description (optional)" class="w-full border border-gray-300 rounded px-3 py-2"></textarea>

            <!-- Dynamic Subform -->
            <p class="text-red-500 text-sm">Selected subtype: {{ subtype }}</p>
            <component :is="dynamicFieldsComponent" v-model="subtypeFields" />
            
            <!-- Submit -->
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded shadow">
                Create
            </button>
        </form>
    </div>
</template>
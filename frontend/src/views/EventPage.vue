<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center p-4">
        <div class="w-full max-w-3xl bg-white rounded-2xl shadow-lg p-8">
            <div v-if="loading" class="text-center py-16">Loading event…</div>
            <div v-else-if="error" class="text-red-500 text-center py-16">Could not load event.</div>
            <div v-else>
                <h1 class="text-3xl font-bold text-blue-700 mb-4">{{ event.name }}</h1>
                <p class="text-gray-600 mb-6">{{ event.description }}</p>
                <!-- Dynamically swap in the right form component -->
                <component
                    :is="formComponent"
                    :event="event"
                    @submitted="onSubmitted"
                />
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

import AvailabilityForm from '../components/AvailabilityForm.vue'
import RsvpForm from '../components/RsvpForm.vue'

const route = useRoute()
const link = route.params.link

const event = ref(null)
const loading = ref(true)
const error = ref(false)

const formComponent = computed(() => {
    if (!event.value) {
        return null
    }
    return event.value.type === 'availability_match'
        ? AvailabilityForm
        : RsvpForm
})

onMounted(async () => {
    try {
        const res = await axios.get(`http://localhost:8000/api/events/${link}/`)
        event.value = res.data
    } catch (e) {
        error.value = true
    } finally {
        loading.value = false
    }
})

function onSubmitted() {
    alert('Thanks for submitting!')
}

</script>  
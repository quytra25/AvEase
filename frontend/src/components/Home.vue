<template>
    <div class="max-w-md mx-auto mt-8 p-6 bg-white shadow rounded">
        <div class="home">
            <h1 class="text-2xl font-bold mb-4">Create a new event</h1>

            <!-- Step 1: Choose main flow -->
            <div v-if="step === 1" class="space-y-4">
                <h2>1. Choose event type:</h2>
                <button class="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700" @click="selectFlow('availability_match')">Availability Match</button>
                <button class="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700" @click="selectFlow('rsvp_based')">RSVP‑Based</button>
            </div>

            <!-- Step 2: Choose sub‑type -->
            <div v-if="step === 2" class="space-y-4">
                <h2>2. Choose sub‑type:</h2>
                <button v-for="opt in subTypeOptions" :key="opt.value" @click="selectSubType(opt.value)">
                {{ opt.label }}
                </button>
                <button @click="step = 1">‹ Back</button>
            </div>

            <!-- Step 3: Fill in the form -->
            <div v-if="step === 3" class="space-y-4">
                <h2>3. Enter details:</h2>
                <!-- dynamic component based on flow+subType -->
                <component :is="currentFormComponent" :formData="formData" @submit="createEvent" @back="step = 2"/>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, computed } from 'vue'
import AvailabilityWeeklyForm from '@/components/forms/AvailabilityWeeklyForm.vue'
import AvailabilitySingleDayForm from '@/components/forms/AvailabilitySingleDayForm.vue'
import AvailabilityMultiDayForm from '@/components/forms/AvailabilityMultiDayForm.vue'
import RsvpSingleDayForm from '@/components/forms/RsvpSingleDayForm.vue'
import RsvpMultiDayForm from '@/components/forms/RsvpMultiDayForm.vue'
import api from '@/services/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const step = ref(1)
const flow = ref(null) // 'availability_match' or 'rsvp_based'
const subType = ref(null) // e.g. 'weekly', 'single_day', 'multi_day'

const formData = ref({
    name: '',
    description: '',
    location: '',
    // and subtype‑specific fields added by the form component
})

// map sub‑type buttons
const subTypeOptions = computed(() => {
    if (flow.value === 'availability_match') {
        return [
            { label: 'Weekly', value: 'weekly' },
            { label: 'Single‑Day', value: 'single_day' },
            { label: 'Multi‑Day', value: 'multi_day' },
        ]
    } else {
    return [
        { label: 'Single‑Day', value: 'rsvp_single_day' },
        { label: 'Multi‑Day', value: 'rsvp_multi_day' },
    ]
    }
})

// dynamic component name
const currentFormComponent = computed(() => {
    if (flow.value === 'availability_match') {
    if (subType.value === 'weekly') return AvailabilityWeeklyForm
    if (subType.value === 'single_day') return AvailabilitySingleDayForm
    if (subType.value === 'multi_day') return AvailabilityMultiDayForm
    } else {
    if (subType.value === 'rsvp_single_day') return RsvpSingleDayForm
    if (subType.value === 'rsvp_multi_day')  return RsvpMultiDayForm
    }
    return null
})

// handlers
function selectFlow(f) {
    flow.value = f
    step.value = 2
}

function selectSubType(st) {
    subType.value = st
    formData.value.type = flow.value
    formData.value.sub_type = st  // the serializer can look at this
    step.value = 3
}

// called by child form when user clicks “Submit”
async function createEvent(payload) {
    // payload should include all common + subtype fields
    const { data } = await api.createEvent(payload)
    router.push(`/events/${data.id}`)
}
</script>
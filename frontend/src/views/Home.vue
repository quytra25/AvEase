<template>
    <div class="p-8">
        <h1 class="text-2xl font-bold">Welcome to AvEase</h1>
        <p>Create or join an event from the links above.</p>
    </div>
    <div class="max-w-xl mx-auto mt-10 p-6 bg-white rounded-lg shadow">
        <h1 class="text-2xl font-bold mb-6 text-center">Create an Event</h1>
        <!-- Step 1: Choose main type -->
        <div class="grid grid-cols-1 gap-4">
            <button @click="selectType('availability_match')" :class="btnClass(selectedType === 'availability_match')">
                Availability-Match Event
            </button>
            <button @click="selectType('rsvp_based')" :class="btnClass(selectedType === 'rsvp_based')">
                RSVP-Based Event
            </button>
        </div>

        <!-- Step 2: Choose sub-type -->
        <div v-if="selectedType" class="mt-8">
            <h2 class="text-xl font-semibold mb-4">Select Sub-Type</h2>
            <div class="grid grid-cols-1 gap-3">
                <button v-for="opt in subOptions" :key="opt.value" @click="selectSub(opt.value)" :class="btnClass(selectedSub === opt.value)">
                    {{ opt.label }}
                </button>
            </div>
        </div>

        <!-- Step 3: Continue to creation form -->
        <div v-if="selectedSub" class="mt-8 text-center">
            <router-link :to="{ path: '/create', query: { type: selectedType, sub: selectedSub } }" class="inline-block mt-4 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                Next: Fill Event Details
            </router-link>
        </div>
    </div>
</template>
  
<script setup>
import { ref, computed } from 'vue'

const selectedType = ref('')
const selectedSub = ref('')

const subOptions = computed(() => {
    if (selectedType.value === 'availability_match') {
        return [
            { value: 'weekly', label: 'Weekly' },
            { value: 'single_day', label: 'Single-Day' },
            { value: 'multi_day', label: 'Multi-Day' }
        ]
    }
    if (selectedType.value === 'rsvp_based') {
        return [
            { value: 'rsvp_single_day', label: 'RSVP Single-Day' },
            { value: 'rsvp_multi_day', label: 'RSVP Multi-Day' }
        ]
    }
    return []
})

function selectType(type) {
    selectedType.value = type
    selectedSub.value = ''
}

function selectSub(sub) {
    selectedSub.value = sub
}

function btnClass(isActive) {
    return [
        'w-full px-4 py-2 text-left rounded-lg border',
        isActive
        ? 'bg-blue-100 border-blue-300'
        : 'bg-white border-gray-200 hover:bg-gray-50'
    ]
}
</script>
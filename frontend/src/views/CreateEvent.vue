<template>
    <Spinner v-if="loading" />
    <section class="section">
        <div class="container">
            <h1 class="title">Create an Event</h1>

            <!-- Main Type Toggle -->
            <div class="toggle-group">
                <div class="buttons has-addons mb-4">
                    <button class="button" :class="{ 'is-link': mainType === 'availability_match' }" @click="selectMainType('availability_match')">
                        Availability Match
                    </button>
                    <button class="button" :class="{ 'is-link': mainType === 'rsvp_based' }" @click="selectMainType('rsvp_based')">
                        RSVP-Based
                    </button>
                </div>
            </div>

            <!-- Sub-Type Toggle -->
            <div class="toggle-group">
                <div v-if="mainType === 'availability_match'" class="buttons has-addons mb-4">
                    <button class="button" :class="{ 'is-link': subType === 'weekly_match' }" @click="selectSubType('weekly_match')">Weekly</button>
                    <button class="button" :class="{ 'is-link': subType === 'date_match' }" @click="selectSubType('date_match')">Date</button>
                </div>
                <div v-else class="buttons has-addons mb-4">
                    <button class="button" :class="{ 'is-link': subType === 'rsvp_single' }" @click="selectSubType('rsvp_single')">Single Day</button>
                    <button class="button" :class="{ 'is-link': subType === 'rsvp_multi' }" @click="selectSubType('rsvp_multi')">Multi Day</button>
                </div>
            </div>

            <!-- Form -->
            <div class="event-form">
                <component :is="currentFormComponent" :formData="formData" @submit="onSubmit" />
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { useToast } from 'vue-toastification'
import Spinner from '@/components/Spinner.vue'
import { currentUser } from '@/composables/useAuth'

import AvailabilityWeeklyForm from '@/components/forms/AvailabilityWeeklyForm.vue'
import AvailabilityDateForm from '@/components/forms/AvailabilityDateForm.vue'
import RsvpSingleDayForm from '@/components/forms/RsvpSingleDayForm.vue'
import RsvpMultiDayForm from '@/components/forms/RsvpMultiDayForm.vue'

// State
const router = useRouter()
const toast = useToast()
const loading = ref(false)

const mainType = ref('availability_match')
const subType = ref('weekly_match')

// Reactive form state
const formData = reactive({
    event_type: subType.value,
    name: '',
    description: '',
    location: '',
    mon_selected: false,
    tue_selected: false,
    wed_selected: false,
    thur_selected: false,
    fri_selected: false,
    sat_selected: false,
    sun_selected: false,
    start_time: '',
    end_time: '',
    start_date_range: '',
    end_date_range: '',
    is_all_day: false,
    confirmed_date: '',
    confirmed_start_time: '',
    confirmed_end_time: '',
    num_days: 1,
    date: '',
    start_date: '',
    end_date: ''
})

// Keep formData.event_type in sync with subType
watch(subType, v => {
    formData.event_type = v
})

// Type selection handlers
function selectMainType(type) {
    mainType.value = type
    subType.value = type === 'availability_match' ? 'weekly_match' : 'rsvp_single'
}
function selectSubType(type) {
    subType.value = type
}

// Dynamic form component loader
const currentFormComponent = computed(() => {
    switch (subType.value) {
        case 'weekly_match': return AvailabilityWeeklyForm
        case 'date_match': return AvailabilityDateForm
        case 'rsvp_single': return RsvpSingleDayForm
        case 'rsvp_multi': return RsvpMultiDayForm
        default: return null
    }
})

// CSRF init
onMounted(async () => {
    try {
        await api.getCsrfToken()
    } catch (err) {
        console.error('Failed to fetch CSRF token', err)
    }
})

// Submit handler (sends backend-aligned payload)
async function onSubmit(validatedPayload) {
    loading.value = true
    try {
        await api.getCsrfToken()
        console.log('Submitting event with payload:', validatedPayload)
        const { data: created } = await api.createEvent(validatedPayload)

        // Auto join as participant if user is authenticated
        if (currentUser.value?.email) {
            const { data: participant } = await api.joinEvent(created.id)
            localStorage.setItem(`participant_${created.link}`, participant.id)
        }

        toast.success('Event created!')
        router.push({ name: 'EventDetail', params: { link: created.link } })
    } catch (err) {
        console.error(err)
        toast.error('Failed to create event. Try again.')
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.event-form {
    margin-top: 1rem !important;
}
</style>  
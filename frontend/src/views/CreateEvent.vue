<template>
    <section class="section">
        <div class="container">
            <h1 class="title">Create an Event</h1>

            <!-- Event Type Toggle -->
            <div class="toggle-group">
                <div class="buttons has-addons mb-4">
                    <button class="button" :class="{ 'is-link': eventType === 'availability_match' }" @click="selectType('availability_match')">
                        Availability Match
                    </button>
                    <button class="button" :class="{ 'is-link': eventType === 'rsvp_based' }" @click="selectType('rsvp_based')">
                        RSVP-Based
                    </button>
                </div>
            </div>
    
            <!-- Sub-Type Toggle -->
            <div class="toggle-group">
                <div v-if="eventType === 'availability_match'" class="buttons has-addons mb-4">
                    <button class="button" :class="{ 'is-link': subType === 'weekly' }" @click="selectSubType('weekly')">Weekly</button>
                    <button class="button" :class="{ 'is-link': subType === 'single_day' }" @click="selectSubType('single_day')">Single-Day</button>
                    <button class="button" :class="{ 'is-link': subType === 'multi_day' }" @click="selectSubType('multi_day')">Multi-Day</button>
                </div>
                <div v-else class="buttons has-addons mb-4">
                    <button class="button" :class="{ 'is-link': subType === 'rsvp_single_day' }" @click="selectSubType('rsvp_single_day')">
                        Single-Day
                    </button>
                    <button class="button" :class="{ 'is-link': subType === 'rsvp_multi_day' }" @click="selectSubType('rsvp_multi_day')">
                        Multi-Day
                    </button>
                </div>
            </div>

            <div class="event-form">
                <!-- Dynamically render the right form -->
                <component :is="currentFormComponent" :formData="formData" @submit="onSubmit"/>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { useToast } from 'vue-toastification'
import AvailabilityWeeklyForm from '@/components/forms/AvailabilityWeeklyForm.vue'
import AvailabilitySingleDayForm from '@/components/forms/AvailabilitySingleDayForm.vue'
import AvailabilityMultiDayForm from '@/components/forms/AvailabilityMultiDayForm.vue'
import RsvpSingleDayForm from '@/components/forms/RsvpSingleDayForm.vue'
import RsvpMultiDayForm from '@/components/forms/RsvpMultiDayForm.vue'

// hooks
const router = useRouter()
const toast = useToast()

const eventType = ref('availability_match')
const subType = ref('weekly')

const formData = reactive({
    type: eventType.value,
    sub_type: subType.value,
    // common fields
    name: '',
    description: '',
    location: '',
    // weekly
    mon_selected: false,
    tue_selected: false,
    wed_selected: false,
    thur_selected: false,
    fri_selected: false,
    sat_selected: false,
    sun_selected: false,
    start_time: '',
    end_time: '',
    // single-day
    start_date_range: '',
    end_date_range: '',
    is_all_day: false,
    // multi-day
    num_days: 1,
    // RSVP
    date: '',
    start_date: '',
    end_date: '',
})

// keep formData.type/sub_type in sync
watch(eventType, v => formData.type = v)
watch(subType, v => formData.sub_type = v)

function selectType(t) {
  eventType.value = t
  subType.value = t === 'availability_match' ? 'weekly' : 'rsvp_single_day'
}
function selectSubType(st) {
  subType.value = st
}

// 5) Pick the right form component
const currentFormComponent = computed(() => {
    if (eventType.value === 'availability_match') {
        if (subType.value === 'weekly') {
            return AvailabilityWeeklyForm
        }
        if (subType.value === 'single_day') {
            return AvailabilitySingleDayForm
        }
        if (subType.value === 'multi_day') {
            return AvailabilityMultiDayForm
        }  
        }
    else {
        if (subType.value === 'rsvp_single_day') {
            return RsvpSingleDayForm
        }
        if (subType.value === 'rsvp_multi_day') {
            return RsvpMultiDayForm
        }
    }
    return null
})

// 6) On final submit: smash together common + subtype fields & hit the API
async function onSubmit(payload) {
    try {
        // 1) send the payload to your server
        const { data: created } = await api.createEvent(payload)

        // 2) notify the user
        toast.success('Event created!')

        // 3) redirect to the newly created event’s detail page
        router.push({ name: 'EventDetail', params: { id: created.id } })

    } catch (err) {
        console.error(err)
        toast.error('Oops, could not create event. Please try again.')
    }
}
</script>

<style scoped>
</style>
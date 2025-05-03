<template>
    <ErrorBanner v-if="error" :message="error" />
    <div v-else-if="!event">
    <Spinner />
    </div>
    <div v-else>
    <h1 class="title">{{ event.name }}</h1>
    <p>{{ event.description }}</p>
    <p><strong>Shareable Link:</strong> {{ fullLink }}</p>

    <div v-if="!joined">
        <div v-if="isAuthenticated">
        <button class="button is-link" @click="join">Join this event</button>
        </div>
        <div v-else>
        <input v-model="guestName" class="input" placeholder="Your name" />
        <button class="button is-primary mt-2" @click="joinAsGuest" :disabled="!guestName">Join</button>
        </div>
    </div>

    <div v-else>
        <component :is="currentEventComponent" :event="event" :participantID="participantID" />
    </div>

    <h2 class="mt-6 text-lg font-semibold">Participants</h2>
    <ul class="list-disc ml-6 mt-2">
        <li v-for="p in event.participants" :key="p.id">
        {{ p.user_first_name }} {{ p.user_last_name || '(Guest)' }} —
        <span v-if="event.type === 'availability_match'">
            {{ p.availabilities.length }} slot(s)
        </span>
        <span v-else>
            {{ p.availabilities[0]?.rsvp_status || 'No Response' }}
        </span>
        </li>
    </ul>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'
import api from '@/services/api'
import { isAuthenticated } from '@/composables/useAuth.js'
import Spinner from '@/components/Spinner.vue'
import ErrorBanner from '@/components/ErrorBanner.vue'
import WeeklyAvailabilityTable from '@/components/eventViews/WeeklyAvailabilityTable.vue'
import SingleDayAvailabilityTable from '@/components/eventViews/SingleDayAvailabilityTable.vue'
import MultiDayAvailabilityTable from '@/components/eventViews/MultiDayAvailabilityTable.vue'
import RsvpEventPanel from '@/components/eventViews/RsvpEventPanel.vue'

const route = useRoute()
const toast = useToast()
const event = ref(null)
const joined = ref(false)
const participantID = ref(null)
const guestName = ref('')
const error = ref('')

const fullLink = computed(() => `${window.location.origin}/event/${event.value?.id}`)

const currentEventComponent = computed(() => {
    if (!event.value) return null
    const { event_type } = event.value
    if (['weekly'].includes(event_type)) return WeeklyAvailabilityTable
    if (['single_day'].includes(event_type)) return SingleDayAvailabilityTable
    if (['multi_day'].includes(event_type)) return MultiDayAvailabilityTable
    if (['rsvp_single', 'rsvp_multi'].includes(event_type)) return RsvpEventPanel
    return null
})

const currentParticipant = computed(() => event.value?.participants.find(p => p.id === participantID.value) || null)

onMounted(async () => {
    try {
    const { data } = await api.getEvent(route.params.link)
    event.value = data
    const storedId = localStorage.getItem(`participant_${data.id}`)
    const p = data.participants.find(p => p.id === storedId || p.user === currentParticipant.value?.user)
    if (p) {
        joined.value = true
        participantID.value = p.id
    }
    } catch (err) {
    error.value = 'Failed to load event. Please check the link or try again later.'
    }
})

async function join() {
    try {
    const { data } = await api.joinEvent(event.value.id)
    participantID.value = data.id
    joined.value = true
    } catch {
    toast.error('Failed to join the event')
    }
}

async function joinAsGuest() {
    try {
    const { data } = await api.joinEventAsGuest(event.value.id, { guest_name: guestName.value })
    participantID.value = data.id
    joined.value = true
    localStorage.setItem(`participant_${event.value.id}`, data.id)
    } catch {
    toast.error('Failed to join as guest')
    }
}
</script>

<style scoped>
input.input {
    width: 250px;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
}
</style>
<template>
    <ErrorBanner v-if="error" :message="error" />
    <div v-else-if="!event">
        <Spinner />
    </div>
    <div v-else class="section">
        <div class="container">
            <h1 class="title has-text-centered">{{ event.name }}</h1>
            <p class="subtitle has-text-centered">{{ event.description }}</p>

            <!-- Shareable Link -->
            <div class="box is-shadowless has-background-light">
                <p class="mb-2"><strong>Shareable Link:</strong></p>
                <div class="is-flex is-align-items-center">
                    <input
                    class="input mr-2 is-small"
                    :value="fullLink"
                    readonly
                    ref="linkInput"
                    style="max-width: 100%;"
                    />
                    <button class="button is-info is-light is-small" @click="copyLink">
                        Copy
                    </button>
                </div>
                <p v-if="copied" class="has-text-success mt-2">Link copied!</p>
            </div>

            <!-- Join Section -->
            <div v-if="!joined" class="box has-background-light">
            <!-- Logged-in user -->
            <div v-if="isAuthenticated">
                <button class="button is-link" @click="join">Join this event</button>
            </div>

            <!-- Guest -->
            <div v-else>
                <label class="label">Enter your name to join as guest</label>
                <div class="field has-addons">
                    <div class="control is-expanded">
                        <input
                        v-model="guestName"
                        class="input"
                        placeholder="Your name"
                        />
                    </div>
                    <div class="control">
                        <button
                        class="button is-primary"
                        @click="joinAsGuest"
                        :disabled="!guestName"
                        >
                            Join
                        </button>
                    </div>
                </div>
            </div>
            </div>

            <!-- Event Interaction -->
            <div v-else>
                <component :is="currentEventComponent" :event="event" :participantID="participantID" />
            </div>

            <!-- Participants -->
            <div class="mt-6">
                <h2 class="title is-5">Participants</h2>
                <ul class="content">
                    <li v-for="p in event.participants" :key="p.id">
                        {{ p.user_first_name }} {{ p.user_last_name || '(Guest)' }} —
                        <span v-if="event.event_type.startsWith('rsvp')">
                            {{ p.availabilities[0]?.rsvp_status || 'No Response' }}
                        </span>
                        <span v-else>
                            {{ p.availabilities.length }} slot(s)
                        </span>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>  

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'
import api from '@/services/api'
import { currentUser, isAuthenticated } from '@/composables/useAuth'
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
const copied = ref(false)
const rsvp = ref('')

const link = route.params.link
const fullLink = computed(() => `${window.location.origin}/events/${event.value?.link}`)

const currentEventComponent = computed(() => {
    const type = event.value?.event_type
    if (type === 'weekly') return WeeklyAvailabilityTable
    if (type === 'single_day') return SingleDayAvailabilityTable
    if (type === 'multi_day') return MultiDayAvailabilityTable
    if (['rsvp_single', 'rsvp_multi'].includes(type)) return RsvpEventPanel
    return null
})

function copyLink() {
    navigator.clipboard.writeText(fullLink.value).then(() => {
        copied.value = true
        setTimeout(() => (copied.value = false), 1500)
    })
}

onMounted(async () => {
    try {
        await api.getCsrfToken()
        const { data } = await api.getEvent(link)

        if (!data || !data.name) throw new Error('Invalid event data')
        event.value = data

        // Guest rejoin
        const savedID = localStorage.getItem(`participant_${link}`)
        if (savedID) {
            const match = data.participants.find(p => p.id === parseInt(savedID))
            if (match) {
                participantID.value = match.id
                joined.value = true
                if (data.event_type.startsWith('rsvp')) {
                    rsvp.value = match.availabilities[0]?.status || ''
                }
                return
            }
        }

        // Authenticated user rejoin
        if (isAuthenticated.value && currentUser.value?.email) {
            const existing = data.participants.find(
                p => p.user_email === currentUser.value.email
            )
            if (existing) {
                participantID.value = existing.id
                joined.value = true
                if (data.event_type.startsWith('rsvp')) {
                    rsvp.value = existing.availabilities[0]?.status || ''
                }
            }
        }
    } catch (err) {
        console.error('Error while fetching event:', err)
        error.value = 'Failed to load event. Please check the link or try again later.'
    }
})

async function join() {
    try {
        const { data } = await api.joinEvent(event.value.id)
        participantID.value = data.id
        joined.value = true
        toast.success('Joined event successfully!')
    } catch (err) {
        console.error(err)
        toast.error('Failed to join the event')
    }
}

async function joinAsGuest() {
    try {
        await api.getCsrfToken()
        const { data } = await api.joinEventAsGuest(event.value.id, {
            guest_name: guestName.value
        })

        participantID.value = data.id
        joined.value = true
        localStorage.setItem(`participant_${event.value.link}`, data.id)
        toast.success(`Welcome, ${guestName.value}!`)
    } catch (err) {
        console.error('Guest join failed:', err)
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
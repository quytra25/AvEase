<template>
    <ErrorBanner v-if="error" :message="error" />
    <div v-else-if="!event">
        <Spinner />
    </div>
    <div v-else class="section">
        <div class="container">
            <!-- Event Header Section -->
            <div class="event-header-box box has-background-light has-text-centered p-5 mb-5">
                <h1 class="title is-3 has-text-weight-semibold mb-3">{{ event.name }}</h1>

                <p v-if="event.location" class="is-size-6 mb-2">📍 {{ event.location }}</p>
                <p v-if="event.description" class="is-size-6 has-text-grey mb-2">{{ event.description }}</p>
                <p class="is-size-7 has-text-grey is-italic mb-4">Created by: {{ event.coordinator_name }}</p>

                <div class="share-link-wrapper is-flex is-justify-content-center is-align-items-center is-flex-wrap-wrap">
                    <p class="mr-2 has-text-dark has-text-weight-semibold">Shareable Link:</p>
                    <input
                    class="input is-small is-flex-grow-1 mr-2"
                    style="max-width: 300px;"
                    :value="fullLink"
                    readonly
                    ref="linkInput"
                    />
                    <button class="button is-info is-light is-small" @click="copyLink">
                        Copy
                    </button>
                </div>
                <p v-if="copied" class="has-text-success mt-2">Link copied!</p>
            </div>


            <!-- Join Section -->
            <div v-if="!joined" class="box has-background-light join-wrapper">
                <!-- Logged-in user -->
                <div v-if="isAuthenticated">
                    <button class="button is-link is-large px-5 py-4" @click="join">Join this event</button>
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
                <component :is="currentEventComponent" :event="event" :participantID="participantID" :participants="event.participants" />
            </div>

            <!-- Participants -->
            <div v-if="!event.event_type.startsWith('rsvp')" class="mt-6">
                <h2 class="title is-5">Participants</h2>
                <ul class="content">
                    <li v-for="p in event.participants" :key="p.id">
                        {{ p.user_first_name }} {{ p.user_last_name || '(Guest)' }}
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
import DateAvailabilityTable from '@/components/eventViews/DateAvailabilityTable.vue'
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
    if (type === 'weekly_match') return WeeklyAvailabilityTable
    if (type === 'date_match') return DateAvailabilityTable
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
        // const savedID = localStorage.getItem(`participant_${link}`)
        // if (savedID) {
        //     const match = data.participants.find(p => p.id === parseInt(savedID))
        //     if (match) {
        //         participantID.value = match.id
        //         joined.value = true
        //         if (data.event_type.startsWith('rsvp')) {
        //             rsvp.value = match.availabilities[0]?.status || ''
        //         }
        //         return
        //     }
        // }

        // Authenticated user rejoin
        if (isAuthenticated.value && currentUser.value?.email) {
            const existing = data.participants.find(
                p => p.user_email === currentUser.value.email
            )
            if (existing) {
                participantID.value = existing.id
                joined.value = true
                if (data.event_type.startsWith('rsvp')) {
                    rsvp.value = existing.rsvp_status?.[0]?.status || ''
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

.join-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 20vh;
    text-align: center;
}

.event-header {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.text-medium {
    color: #4f4f4f;
}

.event-header-box {
    border: 1px solid #d8e6f2;
    border-radius: 12px;
    background-color: #f9fbfd;
}

.share-link-wrapper {
    margin-top: 1rem;
    flex-direction: row;
    gap: 0.5rem;
}

.section {
    padding-top: 0rem !important;
}

.container {
    margin-top: 0 !important;
}

</style>
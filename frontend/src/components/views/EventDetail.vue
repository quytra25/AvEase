<template>
    <div v-if="event">
        <h1>{{ event.name }}</h1>
        <p>{{ event.description }}</p>
        <p>
            <strong>Link:</strong> {{ event.link }}
        </p>

        <div v-if="!joined">
            <!-- Signed-in users just click to join -->
            <div v-if="isAuthenticated">
                <button @click="join">Join this event</button>
            </div>

            <!-- Guests must enter their name -->
            <div v-else>
                <input v-model="guestName" placeholder="Your name" />
                <button @click="joinAsGuest" :disabled="!guestName">Join</button>
            </div>
        </div>

        <div v-else>
            <!-- AVAILABILITY MATCH -->
            <div v-if="event.type === 'availability_match'">
                <!-- Weekly -->
                <div v-if="event.sub_type === 'weekly'">
                    <table>
                        <thead>
                            <tr>
                                <th>Time\Day</th>
                                <th v-for="d in days" :key="d">{{ d }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="t in timeSlots" :key="t">
                                <td>{{ t }}</td>
                                <td v-for="d in days" :key="d">
                                <input
                                    type="checkbox"
                                    :checked="hasWeekly(d, t)"
                                    @change="toggleWeekly(d, t, $event.target.checked)"
                                />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Single‑Day -->
                <div v-else-if="event.sub_type === 'single_day'">
                    <table>
                        <thead>
                            <tr>
                                <th>Time\Date</th>
                                <th v-for="date in dateSlots" :key="date">{{ date }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="t in timeSlots" :key="t">
                                <td>{{ t }}</td>
                                <td v-for="date in dateSlots" :key="date">
                                <input
                                    type="checkbox"
                                    :checked="hasSingle(date, t)"
                                    @change="toggleSingle(date, t, $event.target.checked)"
                                />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Multi‑Day -->
                <div v-else-if="event.sub_type === 'multi_day'">
                    <div v-for="date in dateSlots" :key="date">
                        <label>
                            <input
                                type="checkbox"
                                :checked="hasMulti(date)"
                                @change="toggleMulti(date, $event.target.checked)"
                            />
                            {{ date }}
                        </label>
                    </div>
                </div>
            </div>

            <!-- RSVP BASED -->
            <div v-else-if="event.type === 'rsvp_based'">
                <div v-if="event.sub_type === 'rsvp_single_day'">
                    <p>
                        <strong>Date:</strong> {{ event.date }}
                        <span v-if="!event.is_all_day">
                            ({{ event.start_time }}–{{ event.end_time }})
                        </span>
                    </p>
                </div>
                <div v-else-if="event.sub_type === 'rsvp_multi_day'">
                    <p>
                        <strong>From:</strong> {{ event.start_date }}
                        <br>
                        <strong>To:</strong> {{ event.end_date }}
                    </p>
                </div>
                <label>
                    RSVP:
                    <select v-model="rsvp" @change="submitRsvp">
                        <option value="" disabled>Select…</option>
                        <option value="available">Available</option>
                        <option value="unavailable">Unavailable</option>
                        <option value="tentative">Tentative</option>
                    </select>
                </label>
            </div>
        </div>

        <h2>Participants</h2>
        <ul>
            <li v-for="p in event.participants" :key="p.id">
                {{ p.user_email }} —
                <span v-if="event.type === 'availability_match'">
                    {{ p.availabilities.length }} slot(s)
                </span>
                <span v-else>
                    {{ p.availabilities[0]?.rsvp_status || 'No Response' }}
                </span>
            </li>
        </ul>
    </div>

    <div v-else>
        Loading…
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import { currentUser }     from '@/composables/useAuth'

const route = useRoute()
const event = ref(null)
const joined = ref(false)
const participantID = ref(null)
const rsvp = ref('')
const guestName = ref('')
const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

const dateSlots = computed(() => {
    if (!event.value?.start_date_range) return []
    const arr = []
    let d = new Date(event.value.start_date_range)
    const end = new Date(event.value.end_date_range)
    while (d <= end) {
        arr.push(d.toISOString().slice(0,10))
        d.setDate(d.getDate()+1)
    }
    return arr
})

const timeSlots = computed(() => {
    if (!event.value?.start_time) return []
    const arr = []
    const [sh,sm] = event.value.start_time.split(':').map(Number)
    const [eh,em] = event.value.end_time.split(':').map(Number)
    let dt = new Date(0,0,0,sh,sm)
    const end = new Date(0,0,0,eh,em)
    while (dt <= end) {
        arr.push(dt.toTimeString().slice(0,5))
        dt.setHours(dt.getHours()+1)
    }
    return arr
})

onMounted(async () => {
    // Call API and fetch event object
    const { data } = await api.getEvent(route.params.id)
    event.value = data

    // If signed in, match by userID
    if (isAuthenticated.value) {
        const me = data.participants.find(p => p.user === currentUser.value.id)
        if (me) {
            joined.value = true
            participantId.value = me.id
        }
    } else {
        // If guest, pull saved participantID from localStorage
        const sid = localStorage.getItem(`participant_${route.params.id}`)
        if (sid) {
            const me = data.participants.find(p => p.id === +sid)
            if (me) {
                joined.value = true
                participantId.value = me.id
            }
        }
    }

    // Looks through data.participants to see if the participant already joined the event
    const me = data.participants.find(p => p.user_email === currentUser.id)
    if (me) {
        joined.value = true
        participantID.value = me.id
        if (data.type === 'rsvp_based') {
            rsvp.value = me.availabilities[0]?.rsvp_status || ''
        }
    }
})

// Join as 'signed-in' user
async function join() {
    const { data } = await api.joinEvent(event.value.id)
    participantID.value = data.id
    joined.value = true
}

// Join as guest
async function joinAsGuest() {
    const { data } = await api.joinEventAsGuest(event.value.id, { email: guestName.value })
    participantId.value = data.id
    joined.value = true
    localStorage.setItem(`participant_${event.value.id}`, data.id)
}

// Availability Match - Weekly Event
function hasWeekly(day, time) {
    const p = event.value.participants.find(p=>p.id===participantID.value)
    return p?.availabilities.some(a=>a.selected_day===day && a.selected_start_time===time)
}

async function toggleWeekly(day, time, checked) {
    if (checked) {
        await api.addAvailability({
            participant: participantID.value,
            availability_type: 'weekly',
            selected_day: day,
            selected_start_time: time,
            selected_end_time: time
        })
    }
    const { data } = await api.getEvent(event.value.id)
    event.value = data
}

// Availability Match - Single-day Event
function hasSingle(date, time) {
    const p = event.value.participants.find(p=>p.id===participantID.value)
    return p?.availabilities.some(a=>a.selected_date===date && a.selected_start_time===time)
}

async function toggleSingle(date, time, checked) {
    if (checked) {
        await api.addAvailability({
            participant: participantID.value,
            availability_type: 'date_time',
            selected_date: date,
            selected_start_time: time,
            selected_end_time: time
        })
    }
    const { data } = await api.getEvent(event.value.id)
    event.value = data
}

// Availability Match - Multi-day Event
function hasMulti(date) {
    const p = event.value.participants.find(p=>p.id===participantID.value)
    return p?.availabilities.some(a=>a.selected_date===date)
}

async function toggleMulti(date, checked) {
    if (checked) {
        await api.addAvailability({
            participant: participantID.value,
            availability_type: 'date_only',
            selected_date: date
        })
    }
    const { data } = await api.getEvent(event.value.id)
    event.value = data
}

// RSVP-based Event 
async function submitRsvp() {
    await api.addAvailability({
        participant: participantID.value,
        availability_type: 'rsvp',
        rsvp_status: rsvp.value
    })
    const { data } = await api.getEvent(event.value.id)
    event.value = data
}
</script>
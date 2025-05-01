<template>
    <ErrorBanner v-if="error" :message="error"/>

    <div v-else-if="!event">
        <Spinner/>
    </div>

    <div v-else>
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
                    <div class="sm:-mx-6 lg:-mx-8 overflow-auto sm:px-6 lg:px-8">
                        <table class="min-w-full table-auto border-collapse">
                            <thead>
                                <tr class="bg-gray-100">
                                    <th class="border px-2 py-1">Time/Day</th>
                                    <th v-for="d in days" :key="d" class="border px-2 py-1">{{ d }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="t in timeSlots" :key="t" class="hover:bg-gray-50">
                                    <td class="border px-2 py-1 font-mono">{{ t }}</td>
                                    <td v-for="d in days" :key="d" class="border px-2 py-1 text-center" :class="{'bg-blue-100': daySlots.has(d + '|' + t), 'bg-green-50': !daySlots.has(d + '|' + t) && countDaySlots(d, t) > 0}">
                                        <input type="checkbox" :checked="hasWeekly(d, t)" @change="toggleWeekly(d, t, $event.target.checked)"/>
                                        <div class="text-xs mt-1">{{ countDaySlots(d, t) }}</div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Single‑Day -->
                <div v-else-if="event.sub_type === 'single_day'">
                    <div v-if="event.is_all_day" class="space-y-2">
                        <div v-for="date in dateSlots" :key="date">
                            <label class="inline-flex items-center">
                                <input type="checkbox" :checked="hasMulti(date)" @change="toggleMulti(date,$event.target.checked)" class="mr-2"/>
                                {{ date }}
                            </label>
                        </div>
                    </div>
                    <div v-else class="sm:-mx-6 lg:-mx-8 overflow-auto sm:px-6 lg:px-8">
                        <table class="min-w-full table-auto border-collapse">
                            <thead>
                                <tr class="bg-gray-100">
                                    <th class="border px-2 py-1">Time/Date</th>
                                    <th v-for="date in dateSlots" :key="date" class="border px-2 py-1 text-center">{{ date }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="t in timeSlots" :key="t">
                                    <td class="border px-2 py-1 font-mono">{{ t }}</td>
                                    <td v-for="date in dateSlots" :key="date" class="border px-2 py-1 text-center" :class="{'bg-blue-100': dateTimeSelections.has(date + '|' + t), 'bg-green-50': !dateTimeSelections.has(date + '|' + t) && countDateTimeSelections(date, t) > 0}">
                                        <input type="checkbox" :checked="hasSingle(date, t)" @change="toggleSingle(date, t, $event.target.checked)"/>
                                        <div class="text-xs mt-1">{{ countDateTimeSelections(date, t) }}</div>
                                    </td>   
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Multi‑Day -->
                <div v-else-if="event.sub_type === 'multi_day'">
                    <div class="sm:-mx-6 lg:-mx-8">
                        <div class="overflow-auto sm:px-6 lg:px-8">
                            <table class="min-w-full table-auto border-collapse">
                                <thead>
                                    <tr class="bg-gray-100">
                                        <th class="border px-2 py-1">Date</th>
                                        <th class="border px-2 py-1 text-center">Available?</th>
                                        <th class="border px-2 py-1 text-center">Count</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="date in dateSlots" :key="date" class="hover:bg-gray-50">
                                        <td class="border px-2 py-1 font-mono sticky left-0 bg-white z-10">{{ date }}</td>
                                        <td class="border px-2 py-1 text-center" :class="{'bg-blue-100': dateSelections.has(date),'bg-green-50': !dateSelections.has(date) && countDateSelections(date) > 0}">
                                        <input
                                            type="checkbox"
                                            :checked="hasMulti(date)"
                                            @change="toggleMulti(date, $event.target.checked)"
                                        />
                                        </td>
                                        <td class="border px-2 py-1 text-center">
                                            {{ countDateSelections(date) }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- RSVP BASED -->
            <div v-else-if="event.type === 'rsvp_based'" class="space-y-4">
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
                    <span class="font-medium">Your RSVP</span>
                    <select v-model="rsvp" @change="submitRsvp" :disabled="savingRsvp" class="mt-1 block w-full border rounded px-2 py-1">
                    <option value="" disabled>Select…</option>
                    <option value="available">Available</option>
                    <option value="unavailable">Unavailable</option>
                    <option value="tentative">Tentative</option>
                    </select>
                </label>
                <!-- summary of everyone’s responses -->
                <div class="mt-2 p-3 bg-gray-50 border rounded">
                    <p class="font-semibold mb-1">Current RSVPs:</p>
                    <ul class="list-disc list-inside text-sm space-y-1">
                    <li>Available: {{ rsvpCounts.available }}</li>
                    <li>Unavailable: {{ rsvpCounts.unavailable }}</li>
                    <li>Tentative: {{ rsvpCounts.tentative }}</li>
                    </ul>
                </div>
            </div>
        </div>

        <h2>Participants</h2>
        <ul>
            <li v-for="p in event.participants" :key="p.id">
                {{ p.user_first_name }} {{ p.user_last_name }} —
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
import api from '@/services/api'
import { currentUser, isAuthenticated } from '@/composables/useAuth.js'
import Spinner from '@/components/Spinner.vue'
import ErrorBanner from '@/components/ErrorBanner.vue'
import { useToast } from 'vue-toastification'

const route = useRoute()
const event = ref(null)
const joined = ref(false)
const participantID = ref(null)
const rsvp = ref('')
const guestName = ref('')
const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const error = ref('')
const savingRsvp = ref(false)
const toast = useToast()
const currentParticipant = computed(() => event.value?.participants.find(x => x.id === participantID.value) || null)

// for weekly event
const daySlots = computed(() => {
    const p = currentParticipant.value
    if (!p){
        return new Set()
    }
    return new Set(
        p.availabilities.map(a => `${a.selected_day}|${a.selected_start_time}`)
    )
})

function countDaySlots(day,time) {
    return event.value.participants.filter(p=>p.availabilities.some(a=>a.selected_day===day && a.selected_start_time===time)).length
}

// for single-day events
const dateTimeSelections = computed(() => {
    const p = currentParticipant.value
    if (!p) {
        return new Set()
    }
    return new Set(
        p.availabilities.filter(a => a.availability_type === 'date_time').map(a => `${a.selected_date}|${a.selected_start_time}`)
    )
})

function countDateTimeSelections(date, time) {
    return event.value.participants.filter(p => p.availabilities.some(a => a.availability_type === 'date_time' && a.selected_date === date && a.selected_start_time === time)).length
}

// for weekly and single-day events
const timeSlots = computed(() => {
    if (!event.value?.start_time) {
        return []
    }
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

// for multi-day events
const dateSelections = computed(() => {
    const p = currentParticipant.value
    if (!p) {
        return new Set()
    }
    return new Set(p.availabilities.filter(a => a.availability_type === 'date_only').map(a => a.selected_date)
    )
})

function countDateSelections(date) {
    return event.value.participants.filter(p => p.availabilities.some(a => a.availability_type === 'date_only' && a.selected_date === date)).length
}

// for single-day and multi-day events
const dateSlots = computed(() => {
    if (!event.value?.start_date_range) {
        return []
    }
    const arr = []
    let d = new Date(event.value.start_date_range)
    const end = new Date(event.value.end_date_range)
    while (d <= end) {
        arr.push(d.toISOString().slice(0,10))
        d.setDate(d.getDate()+1)
    }
    return arr
})

// RSVP-based events

// Counts how many participants chose each status
const rsvpCounts = computed(() => {
    if (!event.value) {
        return { available:0, unavailable:0, tentative:0 }
    }
    else {
        const counts = { available:0, unavailable:0, tentative:0 }
        event.value.participants.forEach(p => {
            const status = p.availabilities[0]?.rsvp_status
            if (status && counts[status] !== undefined) {
                counts[status] += 1
            }
        })
        return counts
    }
})

// Determine auth state
//const isAuthenticated = computed(() => !!currentUser.value?.id)

onMounted(async () => {
    // Call API and fetch event object
    const { data } = await api.getEvent(route.params.id)
    event.value = data
    const p = currentParticipant.value
    if (p) {
        joined.value = true
        participantID.value = p.id
        if (data.type === 'rsvp_based') {
            rsvp.value = p.availabilities[0]?.rsvp_status || ''
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
    const { data } = await api.joinEventAsGuest(event.value.id, { guest_name: guestName.value })
    participantID.value = data.id
    joined.value = true
    localStorage.setItem(`participant_${event.value.id}`, data.id)
}

// Availability Match - Weekly Event
function hasWeekly(day, time) {
    const p = currentParticipant.value
    return p?.availabilities.some(a=>a.selected_day===day && a.selected_start_time===time)
}

async function toggleWeekly(day, time, checked) {
    try {
        if (checked) {
            await api.addAvailability({
                participant: participantID.value,
                availability_type: 'weekly',
                selected_day: day,
                selected_start_time: time,
                selected_end_time: time
            })
        }
        // re-fetch to update UI
        const { data } = await api.getEvent(event.value.id)
        event.value = data
        toast.success("Weekly availability saved")
    } catch {
        toast.error("Failed to save weekly availability — try again")
    }
}

// Availability Match - Single-day Event
function hasSingle(date, time) {
    const p = currentParticipant.value
    return p?.availabilities.some(a=>a.selected_date===date && a.selected_start_time===time)
}

async function toggleSingle(date, time, checked) {
    try {
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
        toast.success('Single-day availability saved')
    } catch (err) {
        toast.error('Failed to save single-day availability — try again')
    } 
}

// Availability Match - Multi-day Event
function hasMulti(date) {
    const p = currentParticipant.value
    return p?.availabilities.some(a=>a.selected_date===date)
}

async function toggleMulti(date, checked) {
    try {
        if (checked) {
            await api.addAvailability({
                participant: participantID.value,
                availability_type: 'date_only',
                selected_date: date
            })
        }
        const { data } = await api.getEvent(event.value.id)
        event.value = data
        toast.success('Multi-day availability saved')
    } catch (err) {
        toast.error('Failed to save multi-day availability — try again')
    }
}

// RSVP-based Event
async function submitRsvp() {
    savingRsvp.value = true
    try {
        await api.addAvailability({
            participant: participantID.value,
            availability_type: 'rsvp',
            rsvp_status: rsvp.value
        })
        const { data } = await api.getEvent(event.value.id)
        event.value = data
        toast.success('Your RSVP has been recorded')
    } catch (err) {
        toast.error('Failed to submit RSVP')
    }
    finally {
        savingRsvp.value=false
    }
}
</script>

<style scoped>
@media (max-width: 640px) {
    table {
        display: block;
    }
    thead, tbody, tr, th, td {
        display: block;
    }
    
    th:first-child, td:first-child {
        position: sticky;
        left: 0;
        background: white;
        z-index: 10;
    }
}
</style>
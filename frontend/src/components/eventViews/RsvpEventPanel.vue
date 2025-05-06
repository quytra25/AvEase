<template>
    <div class="rsvp-panel">
        <p class="event-date" v-if="event.event_type === 'rsvp_single'">
            Date: {{ formattedDate }}
        </p>

        <p class="event-date" v-else>
            From: {{ formattedStartDate }}<br/>
            To: {{ formattedEndDate }}
        </p>

        <p v-if="!props.event.event_details.is_all_day" class="event-time">
            Start time: {{ formattedStartTime }}<br/>
            End time: {{ formattedEndTime }}
        </p>

        <div class="field mt-4">
            <label class="label dark-text">Your RSVP</label>
            <div class="control">
                <div class="select is-fullwidth">
                    <select v-model="rsvpStatus" @change="submitRsvp" :disabled="saving">
                        <option disabled value="">Select…</option>
                        <option value="available">Available</option>
                        <option value="unavailable">Unavailable</option>
                        <option value="tentative">Tentative</option>
                    </select>
                </div>
            </div>
        </div>

        <div class="rsvp-summary-box mt-4">
            <p class="summary-title">Current RSVPs:</p>
            <table class="rsvp-table">
                <thead>
                    <tr>
                    <th>Available ({{ rsvpCounts.available }})</th>
                    <th>Unavailable ({{ rsvpCounts.unavailable }})</th>
                    <th>Tentative ({{ rsvpCounts.tentative }})</th>
                    <th>No Response ({{ rsvpCounts.no_response }})</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <div v-for="p in participantsByStatus.available" :key="'a-' + p.id">
                            {{ formatName(p) }}
                            </div>
                        </td>
                        <td>
                            <div v-for="p in participantsByStatus.unavailable" :key="'u-' + p.id">
                            {{ formatName(p) }}
                            </div>
                        </td>
                        <td>
                            <div v-for="p in participantsByStatus.tentative" :key="'t-' + p.id">
                            {{ formatName(p) }}
                            </div>
                        </td>
                        <td>
                            <div v-for="p in participantsByStatus.no_response" :key="'n-' + p.id">
                            {{ formatName(p) }}
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

const props = defineProps({
    event: Object,
    participantID: Number
})

const toast = useToast()
const rsvpStatus = ref('')
const saving = ref(false)

const participantsByStatus = computed(() => {
    const groups = { available: [], unavailable: [], tentative: [], no_response: [] }
    props.event.participants.forEach(p => {
        const status = p.rsvp_status?.status || 'no_response'
        groups[status].push(p)
    })
    return groups
})

const rsvpCounts = computed(() => {
    const counts = { available: 0, unavailable: 0, tentative: 0, no_response: 0 }
    props.event.participants.forEach(p => {
        const status = p.rsvp_status?.status
        if (status && counts[status] !== undefined) {
            counts[status]++
        }
    })
    return counts
})

watchEffect(() => {
    const p = props.event.participants.find(p => p.id === props.participantID)
    if (p) {
        rsvpStatus.value = p.rsvp_status?.status || ''
    }
})

async function submitRsvp() {
    saving.value = true
    try {
        await api.getCsrfToken()

        await api.addRsvpStatus({
            participant: props.participantID,
            status: rsvpStatus.value
        })

        const { data } = await api.getEvent(props.event.link)
        Object.assign(props.event, data)

        toast.success('RSVP status successfully submitted')
    } catch (err) {
        console.error('RSVP submission failed:', err)
        toast.error('Failed to submit RSVP')
    } finally {
        saving.value = false
    }
}

function formatName(p) {
    return `${p.user_first_name || ''} ${p.user_last_name || '(Guest)'}`.trim()
}

function addOrdinalSuffix(day) {
    if (day > 3 && day < 21) return `${day}th`
    const suffixes = ['st', 'nd', 'rd']
    const v = day % 10
    return `${day}${suffixes[v - 1] || 'th'}`
}

function formatDate(dateStr) {
    const date = new Date(dateStr)
    const day = addOrdinalSuffix(date.getDate())
    const month = date.toLocaleString('default', { month: 'long' })
    const weekday = date.toLocaleDateString(undefined, { weekday: 'long' })
    const shortDate = date.toLocaleDateString('en-GB')
    return `${weekday} ${day} ${month} ${date.getFullYear()} (${shortDate})`
}

function formatTime(timeStr) {
    if (!timeStr) return ''
    const [h, m] = timeStr.split(':')
    return `${h.padStart(2, '0')}:${m}`
}

const formattedDate = computed(() => formatDate(props.event.event_details.date))
const formattedStartDate = computed(() => formatDate(props.event.event_details.start_date))
const formattedEndDate = computed(() => formatDate(props.event.event_details.end_date))
const formattedStartTime = computed(() => formatTime(props.event.event_details.start_time))
const formattedEndTime = computed(() => formatTime(props.event.event_details.end_time))
</script>

<style scoped>
.rsvp-panel {
    padding: 1.5rem;
    border-radius: 12px;
    background-color: #f8fbff;
    border: 1px solid #d1e3f0;
}

.event-date,
.event-time {
    font-size: 1rem;
    color: #333;
}

.select select {
    background-color: #f1f6ff;
    color: #333;
}

.label.dark-text {
    color: #222;
}

.rsvp-summary-box {
    background: #e6eaf1;
    padding: 1rem;
    border-radius: 8px;
}

.summary-title {
    font-weight: bold;
    color: #444;
    margin-bottom: 0.5rem;
}

.rsvp-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

.rsvp-table th {
    background-color: #f0f4fa;
    color: #2a2a2a;
    padding: 0.5rem;
}

.rsvp-table td {
    background-color: #fafafa;
    color: #333;
    padding: 0.5rem;
    border: 1px solid #ddd;
    vertical-align: top;
}
</style>
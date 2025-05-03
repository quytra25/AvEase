<template>
    <div class="box">
        <div v-if="event.event_type === 'rsvp_single'">
            <p>
                <strong>Date:</strong> {{ event.date }}
                <span v-if="!event.is_all_day">
                    ({{ event.start_time }} – {{ event.end_time }})
                </span>
            </p>
        </div>
        <div v-else-if="event.event_type === 'rsvp_multi'">
            <p>
                <strong>From:</strong> {{ event.start_date }}<br />
                <strong>To:</strong> {{ event.end_date }}
            </p>
        </div>

        <div class="field mt-4">
            <label class="label">Your RSVP</label>
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

        <div class="notification is-light mt-4">
            <p class="has-text-weight-semibold mb-2">Current RSVPs:</p>
            <ul>
                <li>Available: {{ rsvpCounts.available }}</li>
                <li>Unavailable: {{ rsvpCounts.unavailable }}</li>
                <li>Tentative: {{ rsvpCounts.tentative }}</li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

const props = defineProps({ event: Object, participantID: [String, Number] })
const toast = useToast()
const rsvpStatus = ref('')
const saving = ref(false)

watchEffect(() => {
    const p = props.event.participants.find(p => p.id === props.participantID)
    if (p) {
        rsvpStatus.value = p.availabilities[0]?.rsvp_status || ''
    }
})

const rsvpCounts = computed(() => {
    const counts = { available: 0, unavailable: 0, tentative: 0 }
    props.event.participants.forEach(p => {
        const status = p.availabilities[0]?.rsvp_status
        if (status && counts[status] !== undefined) {
            counts[status]++
        }
    })
    return counts
})

async function submitRsvp() {
    saving.value = true
    try {
        await api.addAvailability({
            participant: props.participantID,
            availability_type: 'rsvp',
            rsvp_status: rsvpStatus.value
        })
        const { data } = await api.getEvent(props.event.id)
        props.event.participants = data.participants
        toast.success('RSVP submitted')
    } catch (err) {
        toast.error('Failed to submit RSVP')
    } finally {
        saving.value = false
    }
}
</script>
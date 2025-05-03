<template>
    <div class="overflow-auto">
    <table class="table is-bordered is-hoverable is-fullwidth">
        <thead>
        <tr>
            <th>Date</th>
            <th class="has-text-centered">Available?</th>
            <th class="has-text-centered">Count</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="date in dateSlots" :key="date">
            <td><code>{{ date }}</code></td>
            <td :class="cellClass(date)" class="has-text-centered">
            <input
                type="checkbox"
                :checked="hasSlot(date)"
                @change="toggleSlot(date, $event.target.checked)"
            />
            </td>
            <td class="has-text-centered">{{ countSlot(date) }}</td>
        </tr>
        </tbody>
    </table>
    </div>
</template>

<script setup>
import { computed, ref, watchEffect } from 'vue'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

const props = defineProps({ event: Object, participantID: [String, Number] })
const toast = useToast()
const selections = ref(new Set())

watchEffect(() => {
    const p = props.event.participants.find(p => p.id === props.participantID)
    if (p) {
    selections.value = new Set(
        p.availabilities
        .filter(a => a.availability_type === 'date_only')
        .map(a => a.selected_date)
    )
    }
})

const dateSlots = computed(() => {
    const start = new Date(props.event.start_date_range)
    const end = new Date(props.event.end_date_range)
    const dates = []
    let d = new Date(start)
    while (d <= end) {
    dates.push(d.toISOString().slice(0, 10))
    d.setDate(d.getDate() + 1)
    }
    return dates
})

function hasSlot(date) {
    return selections.value.has(date)
}

function countSlot(date) {
    return props.event.participants.filter(p =>
    p.availabilities.some(
        a => a.availability_type === 'date_only' && a.selected_date === date
    )
    ).length
}

function cellClass(date) {
    if (selections.value.has(date)) return 'has-background-primary-light'
    if (countSlot(date) > 0) return 'has-background-success-light'
    return ''
}

async function toggleSlot(date, checked) {
    try {
    if (checked) {
        await api.addAvailability({
        participant: props.participantID,
        availability_type: 'date_only',
        selected_date: date
        })
    }
    const { data } = await api.getEvent(props.event.id)
    props.event.participants = data.participants
    toast.success('Availability updated')
    } catch (err) {
    toast.error('Error saving availability')
    }
}
</script>
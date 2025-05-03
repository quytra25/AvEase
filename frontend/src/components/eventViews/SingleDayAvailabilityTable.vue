<template>
    <div class="overflow-auto">
    <table class="table is-bordered is-hoverable is-fullwidth">
        <thead>
        <tr>
            <th>Time / Date</th>
            <th v-for="date in dateSlots" :key="date">{{ date }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="time in timeSlots" :key="time">
            <td><code>{{ time }}</code></td>
            <td
            v-for="date in dateSlots"
            :key="date"
            :class="cellClass(date, time)"
            class="has-text-centered"
            >
            <input
                type="checkbox"
                :checked="hasSlot(date, time)"
                @change="toggleSlot(date, time, $event.target.checked)"
            />
            <div class="is-size-7 mt-1">{{ countSlot(date, time) }}</div>
            </td>
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
        .filter(a => a.availability_type === 'date_time')
        .map(a => `${a.selected_date}|${a.selected_start_time}`)
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

const timeSlots = computed(() => {
    const [sh, sm] = props.event.start_time.split(':').map(Number)
    const [eh, em] = props.event.end_time.split(':').map(Number)
    const slots = []
    let d = new Date(0, 0, 0, sh, sm)
    const end = new Date(0, 0, 0, eh, em)
    while (d <= end) {
    slots.push(d.toTimeString().slice(0, 5))
    d.setMinutes(d.getMinutes() + 15)
    }
    return slots
})

function hasSlot(date, time) {
    return selections.value.has(`${date}|${time}`)
}

function countSlot(date, time) {
    return props.event.participants.filter(p =>
    p.availabilities.some(
        a =>
        a.availability_type === 'date_time' &&
        a.selected_date === date &&
        a.selected_start_time === time
    )
    ).length
}

function cellClass(date, time) {
    const key = `${date}|${time}`
    if (selections.value.has(key)) return 'has-background-primary-light'
    if (countSlot(date, time) > 0) return 'has-background-success-light'
    return ''
}

async function toggleSlot(date, time, checked) {
    try {
    if (checked) {
        await api.addAvailability({
        participant: props.participantID,
        availability_type: 'date_time',
        selected_date: date,
        selected_start_time: time,
        selected_end_time: time
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
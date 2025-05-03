<template>
    <div class="overflow-auto">
        <table class="table is-bordered is-hoverable is-fullwidth">
            <thead>
                <tr>
                    <th>Time / Day</th>
                    <th v-for="day in days" :key="day">{{ day }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="time in timeSlots" :key="time">
                    <td><code>{{ time }}</code></td>
                    <td
                    v-for="day in days"
                    :key="day"
                    :class="cellClass(day, time)"
                    class="has-text-centered"
                    >
                    <input
                    type="checkbox"
                    :checked="hasSlot(day, time)"
                    @change="toggleSlot(day, time, $event.target.checked)"
                    />
                    <div class="is-size-7 mt-1">{{ countSlot(day, time) }}</div>
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
const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const selections = ref(new Set())

watchEffect(() => {
    const p = props.event.participants.find(p => p.id === props.participantID)
    if (p) {
        selections.value = new Set(
            p.availabilities
            .filter(a => a.availability_type === 'weekly')
            .map(a => `${a.selected_day}|${a.selected_start_time}`)
        )
    }
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

function hasSlot(day, time) {
    return selections.value.has(`${day}|${time}`)
}

function countSlot(day, time) {
    return props.event.participants.filter(p =>
    p.availabilities.some(
        a =>
        a.availability_type === 'weekly' &&
        a.selected_day === day &&
        a.selected_start_time === time
    )
    ).length
}

function cellClass(day, time) {
    const key = `${day}|${time}`
    if (selections.value.has(key)) return 'has-background-primary-light'
    if (countSlot(day, time) > 0) return 'has-background-success-light'
    return ''
}

async function toggleSlot(day, time, checked) {
    try {
        if (checked) {
            await api.addAvailability({
                participant: props.participantID,
                availability_type: 'weekly',
                selected_day: day,
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
<template>
    <Spinner v-if="loading" />
    <div class="availability-wrapper">
    <!-- USER INTERACTION TABLE -->
    <h2>Your Availability</h2>
    <table class="availability-table">
        <thead>
        <tr>
            <th class="header">Time</th>
            <th v-for="day in selectedDays" :key="day" class="header">{{ formatDay(day) }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="time in timeSlots" :key="time">
            <td class="time-label">{{ time }}</td>
            <td
            v-for="day in selectedDays"
            :key="day + time"
            :class="{ cell: true, selected: userSelections.has(`${day}_${time}`) }"
            @mousedown="startDrag(day, time)"
            @mouseenter="dragOver(day, time)"
            @mouseup="endDrag"
            @mouseleave="hoverKey = null"
            @mouseover="hoverKey = `${day}_${time}`"
            >
            </td>
        </tr>
        </tbody>
    </table>

    <div class="submit-wrapper">
        <button class="button is-link mt-4" @click="submitAvailability">
        Submit My Availability
        </button>
    </div>

    <!-- HEATMAP TABLE -->
    <h2>Group Availability</h2>
    <table class="availability-table">
        <thead>
        <tr>
            <th class="header">Time</th>
            <th v-for="day in selectedDays" :key="day + '-group'" class="header">{{ formatDay(day) }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="time in timeSlots" :key="time + '-group'">
            <td class="time-label">{{ time }}</td>
            <td
            v-for="day in selectedDays"
            :key="day + time + '-group'"
            :class="getGroupCellClass(day, time)"
            @mouseover="hoverKey = `${day}_${time}`"
            @mouseleave="hoverKey = null"
            >
            <div class="tooltip" v-if="hoverKey === `${day}_${time}`">
                <div>Available ({{ getUsers(day, time, true).length }}): {{ getUsers(day, time, true).join(', ') || 'None' }}</div>
                <div>Unavailable ({{ getUsers(day, time, false).length }}): {{ getUsers(day, time, false).join(', ') || 'None' }}</div>
            </div>
            </td>
        </tr>
        </tbody>
    </table>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '@/services/api'
import { useToast } from 'vue-toastification'
import Spinner from '@/components/Spinner.vue'

const toast = useToast()
const loading = ref(false)

const props = defineProps({
    event: Object,
    participantID: Number,
    participants: Array
})

const selectedDays = computed(() => {
    const details = props.event?.event_details || {}
    return ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun'].filter(d => details[`${d}_selected`])
})

const timeSlots = computed(() => {
    const start = props.event?.event_details?.start_time || '09:00'
    const end = props.event?.event_details?.end_time || '17:00'
    const [sh, sm] = start.split(':').map(Number)
    const [eh, em] = end.split(':').map(Number)

    const slots = []
    let d = new Date(0, 0, 0, sh, sm)
    const endTime = new Date(0, 0, 0, eh, em)
    while (d <= endTime) {
    slots.push(d.toTimeString().slice(0, 5))
    d.setMinutes(d.getMinutes() + 15)
    }
    return slots
})

function formatDay(day) {
    return {
    mon: 'Mon', tue: 'Tue', wed: 'Wed', thur: 'Thu', fri: 'Fri', sat: 'Sat', sun: 'Sun'
    }[day] || day
}

const userSelections = ref(new Set())
const availabilityMap = ref({})
const isDragging = ref(false)
const dragMode = ref('select')
const hoverKey = ref(null)

function startDrag(day, time) {
    isDragging.value = true
    const key = `${day}_${time}`
    dragMode.value = userSelections.value.has(key) ? 'deselect' : 'select'
    toggleUserCell(day, time)
}

function dragOver(day, time) {
    if (isDragging.value) toggleUserCell(day, time)
}

function endDrag() {
    isDragging.value = false
}

function toggleUserCell(day, time) {
    const key = `${day}_${time}`
    if (dragMode.value === 'select') userSelections.value.add(key)
    else userSelections.value.delete(key)
}

function getGroupCellClass(day, time) {
    const key = `${day}_${time}`
    const count = availabilityMap.value[key]?.length || 0
    return {
    cell: true,
    [`level-${count}`]: count > 0
    }
}

function getUsers(day, time, available = true) {
    const key = `${day}_${time}`
    const availableUsers = availabilityMap.value[key] || []
    if (available) return availableUsers.map(p => p.user_first_name)
    return props.event.participants.filter(p => !availableUsers.includes(p)).map(p => p.user_first_name)
}

async function submitAvailability() {
    const newKeys = Array.from(userSelections.value)
    const currentKeys = Object.keys(availabilityMap.value).filter(key =>
    availabilityMap.value[key]?.some(p => p.id === props.participantID)
    )

    const toAdd = newKeys.filter(k => !currentKeys.includes(k))
    const toRemove = currentKeys.filter(k => !newKeys.includes(k))

    loading.value = true
    try {
    await api.getCsrfToken()

    await Promise.all([
        ...toAdd.map(k => {
        const [day, time] = k.split('_')
        return api.addWeeklyAvailability({
            event: props.event.id,
            participant: props.participantID,
            selected_day: day,
            selected_start_time: time
        })
        }),
        ...toRemove.map(k => {
        const [day, time] = k.split('_')
        return api.deleteWeeklyAvailability({
            event: props.event.id,
            participant: props.participantID,
            selected_day: day,
            selected_start_time: time
        })
        })
    ])

    const { data } = await api.getEvent(props.event.link)
    Object.assign(props.event, data)
    updateMap()
    syncUserSelections()
    toast.success('Availability updated!')
    } catch (err) {
    console.error('Failed to submit availability', err)
    toast.error('Error submitting availability.')
    } finally {
    loading.value = false
    }
}

function updateMap() {
    const map = {}
    props.event?.participants?.forEach(p => {
    p.weekly_availabilities?.forEach(a => {
        const time = a.selected_start_time.toString().slice(0, 5)
        const key = `${a.selected_day}_${time}`
        if (!map[key]) map[key] = []
        map[key].push(p)
    })
    })
    availabilityMap.value = { ...map }
}

function syncUserSelections() {
    const mine = []
    props.event.participants?.forEach(p => {
    if (p.id !== props.participantID) return
    p.weekly_availabilities?.forEach(a => {
        const time = a.selected_start_time.toString().slice(0, 5)
        mine.push(`${a.selected_day}_${time}`)
    })
    })
    userSelections.value = new Set(mine)
}

onMounted(() => {
    updateMap()
    syncUserSelections()
})

watch(
    () => props.event.participants,
    () => {
    updateMap()
    syncUserSelections()
    },
    { deep: true }
)
</script>

<style scoped>
.availability-wrapper {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    background-color: #e8f0fe;
    padding: 1rem;
    border-radius: 8px;
}
.availability-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}
.header {
    background-color: #003366;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
    padding: 0.5rem;
}
.time-label {
    background-color: #005599;
    color: white;
    text-align: center;
    padding: 0.5rem;
}
.cell {
    height: 2rem;
    border: 1px solid #ccc;
    background-color: #f9f9f9;
    cursor: pointer;
    position: relative;
}
.cell.selected {
    background-color: #4a90e2;
}
.cell.level-1 { background-color: #cce0ff; }
.cell.level-2 { background-color: #99c2ff; }
.cell.level-3 { background-color: #66a3ff; }
.cell.level-4,
.cell.level-5 { background-color: #3385ff; }
.tooltip {
    position: absolute;
    top: -5px;
    left: 105%;
    background: #fff;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    font-size: 0.75rem;
    z-index: 10;
    white-space: nowrap;
}
.submit-wrapper {
    text-align: center;
}
</style>
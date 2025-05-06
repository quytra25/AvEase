<template>
    <div class="availability-wrapper">
        <div class="calendar-header">
            <button v-if="currentMonthIndex > 0" @click="prevMonth" class="nav-btn">←</button>
            <h2 class="calendar-title">{{ monthYearLabel }}</h2>
            <button v-if="currentMonthIndex < monthGroups.length - 1" @click="nextMonth" class="nav-btn">→</button>
        </div>

        <div class="availability-block">
            <h3 class="availability-title">Your Availability</h3>
            <div class="calendar-grid">
                <div v-for="day in weekdays" :key="day" class="calendar-header-cell">{{ day }}</div>
                <div
                    v-for="(cell, index) in currentMonthDates"
                    :key="'user-' + index"
                    class="calendar-cell"
                    :class="{ selected: userSelections.has(cell.date), inactive: !cell.isCurrentMonth }"
                    @mousedown.prevent="startDrag(cell.date)"
                    @mouseover="dragSelect(cell.date)"
                    @mouseup="stopDrag"
                >
                    {{ cell.day }}
                </div>
            </div>
            <div class="submit-wrapper">
                <button class="button is-link mt-4" @click="submitAvailability">
                    Submit My Availability
                </button>
            </div>
        </div>

        <!-- Group Heatmap Calendar -->
        <div class="availability-block">
            <h3 class="availability-title">Group Availability</h3>
            <div class="calendar-grid">
                <div v-for="day in weekdays" :key="day + '-header'" class="calendar-header-cell">{{ day }}</div>
                <div
                v-for="(cell, index) in currentMonthDates"
                :key="'group-' + index"
                :class="{
                'calendar-cell': true,
                'group': true,
                'inactive': !cell.isCurrentMonth || !availableDateSet.has(cell.date)
                }"
                :style="cell.isCurrentMonth && availableDateSet.has(cell.date) ? getCellStyle(cell.date) : {}"
                @mouseover="hoveredDate = cell.date"
                @mouseleave="hoveredDate = null"
                >
                <template v-if="cell.isCurrentMonth && availableDateSet.has(cell.date)">
                    {{ cell.day }}
                    <div class="tooltip" v-if="hoveredDate === cell.date">
                        <div>Available ({{ getUsers(cell.date, true).length }}): {{ getUsers(cell.date, true).join(', ') }}</div>
                        <div>Unavailable ({{ getUsers(cell.date, false).length }}): {{ getUsers(cell.date, false).join(', ') }}</div>
                    </div>
                </template>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import Spinner from '@/components/Spinner.vue'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

const props = defineProps({
    event: Object,
    participantID: Number,
    participants: Array
})

const toast = useToast()
const loading = ref(true)
const userSelections = ref(new Set())
const dateAvailabilityMap = ref({})
const hoveredDate = ref(null)
const dragging = ref(false)

const weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

const getDaysInRange = (startDate, endDate) => {
    const start = new Date(startDate)
    const end = new Date(endDate)
    const days = []
    while (start <= end) {
        days.push(new Date(start))
        start.setDate(start.getDate() + 1)
    }
    return days
}

const availableDates = computed(() => {
    const details = props.event?.event_details || {}
    return details.start_date && details.end_date ? getDaysInRange(details.start_date, details.end_date) : []
})

const availableDateSet = computed(() => new Set(availableDates.value.map(d => d.toISOString().slice(0, 10))))

const monthGroups = computed(() => {
    const groups = {}
    availableDates.value.forEach(date => {
        const key = `${date.getFullYear()}-${date.getMonth()}`
        if (!groups[key]) groups[key] = []
        groups[key].push(date)
    })
    return Object.values(groups)
})

const currentMonthIndex = ref(0)

const currentMonthDates = computed(() => {
    const monthDates = monthGroups.value[currentMonthIndex.value] || []
    if (!monthDates.length) return []

    const firstDay = (monthDates[0].getDay() + 6) % 7
    const cells = []

    for (let i = 0; i < firstDay; i++) {
        cells.push({ day: '', date: '', isCurrentMonth: false })
    }

    monthDates.forEach(date => {
        const dateStr = date.toISOString().split('T')[0]
        cells.push({
            day: date.getDate(),
            date: dateStr,
            isCurrentMonth: true
        })
    })

    return cells
})

const monthYearLabel = computed(() => {
    const monthDates = monthGroups.value[currentMonthIndex.value]
    return monthDates?.[0]?.toLocaleDateString(undefined, { month: 'long', year: 'numeric' }) || ''
})

function prevMonth() {
    if (currentMonthIndex.value > 0) currentMonthIndex.value--
}
function nextMonth() {
    if (currentMonthIndex.value < monthGroups.value.length - 1) currentMonthIndex.value++
}

function startDrag(date) {
    dragging.value = true
    toggleSelection(date)
}
function dragSelect(date) {
    if (dragging.value) toggleSelection(date)
}
function stopDrag() {
    dragging.value = false
}
function toggleSelection(date) {
    if (!date) return
    userSelections.value.has(date)
    ? userSelections.value.delete(date)
    : userSelections.value.add(date)
}

const participantNameMap = computed(() => {
    const map = {}
    props.participants.forEach(p => {
        map[p.id] = p.user_first_name || 'Guest'
    })
    return map
})

function getUsers(date, available = true) {
    const allAvailable = dateAvailabilityMap.value[date] || []
    if (available) return allAvailable.map(p => participantNameMap.value[p.id])
    return props.participants.filter(p => !allAvailable.includes(p)).map(p => participantNameMap.value[p.id])
}

function getCellStyle(date) {
    const count = getUsers(date, true).length
    const alpha = Math.min(count / props.participants.length, 1)
    return {
        backgroundColor: `rgba(100, 149, 237, ${alpha})`
    }
}

function updateMap() {
    const map = {}
    props.participants.forEach(p => {
        p.date_availabilities?.forEach(a => {
            const date = a.selected_date
            if (!map[date]) map[date] = []
            map[date].push(p)
        })
    })
    dateAvailabilityMap.value = { ...map }
}

function syncUserSelections() {
    const mine = []
    props.participants.forEach(p => {
        if (p.id === props.participantID) {
            p.date_availabilities?.forEach(a => {
                mine.push(a.selected_date)
            })
        }
    })
    userSelections.value = new Set(mine)
}

async function submitAvailability() {
    loading.value = true
    try {
        await api.getCsrfToken()
        await api.deleteDateAvailabilities({ participant: props.participantID })

        const payload = Array.from(userSelections.value).map(date => ({
            participant: props.participantID,
            selected_date: date
        }))
        await Promise.all(payload.map(entry => api.addDateAvailability(entry)))

        const { data } = await api.getEvent(props.event.link)
        Object.assign(props.event, data)
        updateMap()
        syncUserSelections()
        toast.success('Availability submitted!')
    } catch (err) {
        console.error('Submit failed:', err)
        toast.error('Failed to submit availability.')
    } finally {
        loading.value = false
    }
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
    padding: 1rem 0;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}
.calendar-header {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1rem;
    gap: 1rem;
}
.calendar-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
}
.nav-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #333;
}
.availability-block {
    border: 1px solid #ccc;
    padding: 1rem;
    border-radius: 8px;
    background-color: #fafafa;
}
.availability-title {
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 0.75rem;
    color: #444;
}
.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 0.5rem;
    margin-bottom: 1rem;
}
.calendar-header-cell {
    text-align: center;
    font-weight: 500;
    color: #666;
}
.calendar-cell {
    background-color: #e0e0e0;
    padding: 0.75rem;
    text-align: center;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    user-select: none;
}
.calendar-cell.selected {
    background-color: cornflowerblue;
    color: white;
    font-weight: bold;
}
.calendar-cell.inactive {
    background-color: transparent;
    pointer-events: none;
}
.calendar-cell.group {
    cursor: default;
}
.tooltip {
    position: absolute;
    background-color: white;
    padding: 0.5rem;
    border: 1px solid #ccc;
    font-size: 0.75rem;
    border-radius: 4px;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    white-space: nowrap;
    z-index: 10;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.submit-wrapper {
    text-align: center;
}
</style>
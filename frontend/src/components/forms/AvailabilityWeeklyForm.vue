<template>
    <form @submit.prevent="submit">
        <h2 class="form-title">Weekly Availability Match</h2>

        <label class="label">Name of Event *</label>
        <input v-model="local.name" type="text" class="input" placeholder="Event name" />

        <label class="label">Description</label>
        <textarea
        v-model="local.description"
        class="textarea"
        placeholder="Optional details..."
        maxlength="1000"
        rows="1"
        @input="autoResize"
        ></textarea>
        <div class="char-counter">{{ local.description.length }} / 1000</div>

        <label class="label">Location</label>
        <input v-model="local.location" type="text" class="input" placeholder="e.g. Zoom, Café..." />

        <label class="label">Days of week *</label>
        <div class="day-selector" @mousedown.prevent="startDrag" @mouseup="stopDrag" @mouseleave="stopDrag">
            <button
            v-for="(day, index) in days"
            :key="index"
            type="button"
            class="day-button"
            :class="{ active: local[day.key] }"
            @mouseover="dragging && toggleDay(day.key)"
            @click="toggleDay(day.key)"
            >
                {{ day.label }}
            </button>
        </div>

        <div class="time-row">
            <div>
                <label class="label">Start time *</label>
                <select v-model="local.start_time" class="input">
                    <option disabled value="">Select time</option>
                    <option v-for="time in timeOptions" :key="'start-' + time" :value="time">{{ time }}</option>
                </select>
            </div>
            <div>
                <label class="label">End time *</label>
                <select v-model="local.end_time" class="input">
                    <option disabled value="">Select time</option>
                    <option v-for="time in timeOptions" :key="'end-' + time" :value="time">{{ time }}</option>
                </select>
            </div>
        </div>

        <div class="form-footer">
            <button type="submit" class="button is-success">Create</button>
        </div>
    </form>
</template>

<script setup>
import { reactive, watch, ref } from 'vue'
import { useToast } from 'vue-toastification'

const props = defineProps({ formData: Object })
const emit = defineEmits(['submit'])

const toast = useToast()

const local = reactive({ ...props.formData })

watch(local, () => Object.assign(props.formData, local), { deep: true })

const days = [
    { label: 'Mon', key: 'mon_selected' },
    { label: 'Tue', key: 'tue_selected' },
    { label: 'Wed', key: 'wed_selected' },
    { label: 'Thu', key: 'thur_selected' },
    { label: 'Fri', key: 'fri_selected' },
    { label: 'Sat', key: 'sat_selected' },
    { label: 'Sun', key: 'sun_selected' }
]

const timeOptions = []
for (let h = 0; h < 24; h++) {
    for (let m = 0; m < 60; m += 15) {
        const hh = h.toString().padStart(2, '0')
        const mm = m.toString().padStart(2, '0')
        timeOptions.push(`${hh}:${mm}`)
    }
}

// Drag logic for day selector
const dragging = ref(false)
function startDrag() { dragging.value = true }
function stopDrag() { dragging.value = false }
function toggleDay(key) { local[key] = !local[key] }

// Auto-resize for description
function autoResize(e) {
    const el = e.target
    el.style.height = 'auto'
    el.style.height = el.scrollHeight + 'px'
}

function submit() {
    const daysSelected = days.some(day => local[day.key])
    if (!local.name.trim()) {
        toast.error('Event name is required.')
        return
    }
    if (!daysSelected) {
        toast.error('Select at least one day.')
        return
    }
    if (!local.start_time || !local.end_time) {
        toast.error('Both start and end times are required.')
        return
    }
    if (local.start_time >= local.end_time) {
        toast.error('Start time must be earlier than end time.')
        return
    }

    emit('submit', { ...local })
}
</script>
<template>
    <form @submit.prevent="submit">
        <h2 class="form-title">Weekly Availability Match</h2>

        <label class="label">Name *</label>
        <input v-model="local.name" type="text" required class="input" placeholder="Event name" />

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
                <input v-model="local.start_time" type="time" required class="input" />
            </div>
            <div>
                <label class="label">End time *</label>
                <input v-model="local.end_time" type="time" required class="input" />
            </div>
        </div>

        <div class="form-footer">
            <button type="submit" class="button is-success">Create</button>
        </div>
    </form>
</template>

<script setup>
import { reactive, watch, ref } from 'vue'

const props = defineProps({ formData: Object })
const emit = defineEmits(['submit'])

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

let dragging = ref(false)
function startDrag() {
    dragging.value = true
}
function stopDrag() {
    dragging.value = false
}
function toggleDay(dayKey) {
    local[dayKey] = !local[dayKey]
}

function autoResize(event) {
    const el = event.target
    el.style.height = 'auto'
    el.style.height = el.scrollHeight + 'px'
}

function submit() {
    emit('submit', { ...props.formData })
}
</script>
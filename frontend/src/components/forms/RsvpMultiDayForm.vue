<template>
    <form @submit.prevent="submit">
    <h2 class="form-title">RSVP - Multi Day Event</h2>

    <label class="label">Name of Event *</label>
    <input
    v-model="local.name"
    type="text"
    class="input"
    placeholder="Event name"
    />

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
    <input
    v-model="local.location"
    type="text"
    class="input"
    placeholder="e.g. Conference Room"
    />

    <div class="date-row">
        <div>
            <label class="label">Start Date *</label>
            <input
            type="date"
            v-model="local.start_date"
            class="input"
            />
        </div>
        <div>
            <label class="label">End Date *</label>
            <input
            type="date"
            v-model="local.end_date"
            class="input"
            />
        </div>
    </div>

    <label class="checkbox-wrapper">
        <input type="checkbox" v-model="local.is_all_day" />
        Is an all-day event
    </label>

    <div v-if="!local.is_all_day" class="time-row">
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
import { reactive, watch } from 'vue'
import { useToast } from 'vue-toastification'

const props = defineProps({ formData: Object })
const emit = defineEmits(['submit'])

const toast = useToast()
const local = reactive({ ...props.formData })

watch(local, () => Object.assign(props.formData, local), { deep: true })

function autoResize(e) {
    const el = e.target
    el.style.height = 'auto'
    el.style.height = el.scrollHeight + 'px'
}

const timeOptions = []
for (let h = 0; h < 24; h++) {
    for (let m = 0; m < 60; m += 15) {
        const hh = h.toString().padStart(2, '0')
        const mm = m.toString().padStart(2, '0')
        timeOptions.push(`${hh}:${mm}`)
    }
}

function submit() {
    if (!local.name.trim()) {
        toast.error('Event name is required.')
        return
    }

    if (!local.start_date || !local.end_date) {
        toast.error('Start and end dates are required.')
        return
    }

    if (local.start_date > local.end_date) {
        toast.error('Start date must be before or equal to end date.')
        return
    }

    if (!local.is_all_day) {
        if (!local.start_time || !local.end_time) {
            toast.error('Start and end times are required.')
            return
        }
        if (local.start_time >= local.end_time) {
            toast.error('Start time must be earlier than end time.')
            return
        }
    }

    emit('submit', { ...local })
}
</script>
<template>
    <form @submit.prevent="submit">
        <h2 class="form-title">RSVP - Single Day Event</h2>

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
        placeholder="e.g. Zoom, Café..."
        />

        <label class="label">Date of Event *</label>
        <input
        type="date"
        v-model="local.date"
        class="input"
        />

        <label class="checkbox-wrapper">
            <input type="checkbox" v-model="local.is_all_day" />
            Is an all-day event
        </label>

        <div v-if="!local.is_all_day" class="time-row">
            <div>
                <label class="label">Start time *</label>
                <input v-model="local.start_time" type="time" class="input" />
            </div>
            <div>
                <label class="label">End time *</label>
                <input v-model="local.end_time" type="time" class="input" />
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

function submit() {
    const today = new Date().toISOString().split('T')[0]

    if (!local.name.trim()) {
        toast.error('Event name is required.')
        return
    }

    if (!local.date) {
        toast.error('Please select a date.')
        return
    }

    if (local.date < today) {
        toast.error('Date must be today or later.')
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
<template>
    <form @submit.prevent="submit">
        <h2 class="form-title">Date Availability Match</h2>

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
        <input v-model="local.location" type="text" class="input" placeholder="e.g. Zoom, Office, etc..." />

        <div class="date-range">
            <div>
                <label class="label">Start Date *</label>
                <input v-model="local.start_date" type="date" class="input" />
            </div>
            <div>
                <label class="label">End Date *</label>
                <input v-model="local.end_date" type="date" class="input" />
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
    const today = new Date().toISOString().split('T')[0]  // Format as 'YYYY-MM-DD
    
    if (!local.name.trim()) {
        toast.error('Event name is required.')
        return
    }
    if (!local.start_date || !local.end_date) {
        toast.error('Both start and end dates are required.')
        return
    }
    if (local.start_date < today) {
        toast.error('Start date must be today or later.')
        return
    }
    if (local.start_date > local.end_date) {
        toast.error('Start date must be before end date.')
        return
    }
    emit('submit', { ...local })
}
</script>
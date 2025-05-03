<template>
    <form @submit.prevent="submit">
    <h2 class="form-title">Multi-Day Availability Match</h2>

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

    <div class="date-row">
        <div>
        <label class="label">Start Date Range *</label>
        <input
            type="date"
            v-model="local.start_date_range"
            class="input"            
        />
        </div>
        <div>
        <label class="label">End Date Range *</label>
        <input
            type="date"
            v-model="local.end_date_range"
            class="input"
        />
        </div>
    </div>

    <label class="label">Number of days required *</label>
    <input
        type="number"
        v-model.number="local.num_days"
        min="2"
        class="input"
        placeholder="e.g. 3"
    />

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
    if (!local.name.trim()) {
    toast.error('Event name is required.')
    return
    }

    if (!local.start_date_range || !local.end_date_range) {
    toast.error('Both start and end dates are required.')
    return
    }

    if (local.start_date_range > local.end_date_range) {
    toast.error('Start date must be before or equal to end date.')
    return
    }

    if (!local.num_days || local.num_days < 2) {
    toast.error('Please enter a valid number of days (at least 2).')
    return
    }

    emit('submit', { ...local })
}
</script>
<template>
    <form @submit.prevent="submit">
        <h2 class="form-title">Multi-Day Availability Match</h2>

        <label class="label">Name *</label>
        <input
        v-model="local.name"
        type="text"
        required
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

        <label class="label">Number of Days *</label>
        <input
        v-model="local.num_days"
        type="number"
        min="1"
        required
        class="input"
        />

        <div class="date-row">
            <div>
                <label class="label">Start Date Range *</label>
                <input
                type="date"
                v-model="local.start_date_range"
                class="input"
                required
                />
            </div>
            <div>
                <label class="label">End Date Range *</label>
                <input
                type="date"
                v-model="local.end_date_range"
                class="input"
                required
                />
            </div>
        </div>

        <div class="form-footer">
            <button type="submit" class="button is-success">Create</button>
        </div>
    </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({ formData: Object })
const emit = defineEmits(['submit'])

const local = reactive({ ...props.formData })

watch(local, () => Object.assign(props.formData, local), { deep: true })

function autoResize(event) {
    const el = event.target
    el.style.height = 'auto'
    el.style.height = el.scrollHeight + 'px'
}

function submit() {
    emit('submit', { ...props.formData })
}
</script>
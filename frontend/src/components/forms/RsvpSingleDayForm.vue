<template>
    <form @submit.prevent="submit">
        <h2 class="form-title">RSVP Single-Day Event</h2>

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

        <label class="label">Date *</label>
        <input
        type="date"
        v-model="local.date"
        required
        class="input"
        />

        <label class="label checkbox">
            <input type="checkbox" v-model="local.is_all_day" />
            Is an all-day event
        </label>

        <div v-if="!local.is_all_day" class="time-row">
            <div>
                <label class="label">Start time*</label>
                <input
                v-model="local.start_time"
                type="time"
                required
                class="input"
                />
            </div>
            <div>
                <label class="label">End time *</label>
                <input
                v-model="local.end_time"
                type="time"
                required
                class="input"
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
<template>
    <section class="section">
        <div class="container">
            <h1 class="title">Edit Event</h1>

            <div v-if="loading">Loading event...</div>
            <div v-else-if="error" class="notification is-danger">{{ error }}</div>

            <div v-else-if="!canEdit">
                <div class="notification is-warning">
                    This type of event cannot be edited after creation.
                </div>
            </div>

            <form v-else @submit.prevent="submitUpdate">
                <div class="field">
                    <label class="label">Event Name *</label>
                    <div class="control">
                    <input v-model="form.name" class="input" type="text" required />
                    </div>
                </div>

                <div class="field">
                    <label class="label">Location</label>
                    <div class="control">
                    <input v-model="form.location" class="input" type="text" />
                    </div>
                </div>

                <div class="field">
                    <label class="label">Description</label>
                    <div class="control">
                        <textarea v-model="form.description" class="textarea" rows="3" maxlength="1000" />
                    </div>
                </div>

                <!-- RSVP SINGLE -->
                <div v-if="event.event_type === 'rsvp_single'">
                    <div class="field">
                        <label class="checkbox">
                            <input type="checkbox" v-model="form.is_all_day" />
                            All day event
                        </label>
                    </div>

                    <div class="field">
                        <label class="label">Date</label>
                        <input type="date" v-model="form.date" class="input" />
                    </div>

                    <div v-if="!form.is_all_day" class="field is-grouped">
                        <div class="control is-expanded">
                            <label class="label">Start Time</label>
                            <input type="time" v-model="form.start_time" class="input" />
                        </div>
                        <div class="control is-expanded">
                            <label class="label">End Time</label>
                            <input type="time" v-model="form.end_time" class="input" />
                        </div>
                    </div>
                </div>

                <!-- RSVP MULTI -->
                <div v-if="event.event_type === 'rsvp_multi'">
                    <div class="field">
                        <label class="checkbox">
                            <input type="checkbox" v-model="form.is_all_day" />
                            All day event
                        </label>
                    </div>

                    <div class="field is-grouped">
                        <div class="control is-expanded">
                            <label class="label">Start Date</label>
                            <input type="date" v-model="form.start_date" class="input" />
                        </div>
                        <div class="control is-expanded">
                            <label class="label">End Date</label>
                            <input type="date" v-model="form.end_date" class="input" />
                        </div>
                    </div>

                    <div v-if="!form.is_all_day" class="field is-grouped">
                        <div class="control is-expanded">
                            <label class="label">Start Time</label>
                            <input type="time" v-model="form.start_time" class="input" />
                        </div>
                        <div class="control is-expanded">
                            <label class="label">End Time</label>
                            <input type="time" v-model="form.end_time" class="input" />
                        </div>
                    </div>
                </div>

                <!-- Submit -->
                <div class="field mt-4">
                    <button type="submit" class="button is-primary">Update Event</button>
                </div>
            </form>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const event = ref(null)
const form = ref({})
const loading = ref(true)
const error = ref('')

// Disallow editing for availability match events
const canEdit = computed(() => {
    return event.value?.event_type === 'rsvp_single' || event.value?.event_type === 'rsvp_multi'
})

onMounted(async () => {
    try {
        const { data } = await api.getEvent(route.params.link)
        event.value = data

        if (canEdit.value) {
            form.value = {
            name: data.name || '',
            location: data.location || '',
            description: data.description || '',
            ...data.event_details
            }
        }
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load event data.'
    } finally {
        loading.value = false
    }
})

async function submitUpdate() {
    try {
        if (form.value.is_all_day) {
            form.value.start_time = null
            form.value.end_time = null
        }
        await api.updateEvent(event.value.link, form.value)
        toast.success('Event updated successfully!')
        router.push({ name: 'EventDetail', params: { link: event.value.link } })
    } catch (err) {
        console.error('Update failed:', err)
        toast.error('Failed to update event.')
    }
}
</script>

<style scoped>
.section {
    padding: 2rem;
}

.label {
    font-weight: 600;
}
</style>
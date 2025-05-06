<template>
    <div class="event-list-container">
        <div class="event-column">
            <h2>Events I've Created</h2>
            <div v-if="events.created.length === 0" class="event-card empty">
                You haven't created any events yet.
            </div>
            <div
            v-for="event in events.created"
            :key="event.id"
            class="event-card clickable"
            @click="goToEvent(event.link)"
            >
                <h3>{{ event.name }}</h3>
                <div class="event-actions">
                    <button class="button is-info is-small" @click.stop="editEvent(event)">Edit</button>
                    <button class="button is-danger is-small" @click.stop="deleteEvent(event)">Delete</button>
                </div>
            </div>
        </div>

        <div class="event-column">
            <h2>Events I've Joined</h2>
            <div v-if="filteredJoinedEvents.length === 0" class="event-card empty">
                You haven't joined any events yet.
            </div>
            <div
            v-for="event in filteredJoinedEvents"
            :key="event.id"
            class="event-card clickable"
            @click="goToEvent(event.link)"
            >
                <h3>{{ event.name }}</h3>
                <p class="hosted-text">Hosted by {{ event.coordinator_name }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { useToast } from 'vue-toastification'
import { currentUser } from '@/composables/useAuth'

const toast = useToast()
const router = useRouter()
const events = ref({ created: [], joined: [] })

onMounted(async () => {
    try {
        const { data } = await api.getMyEvents()
        events.value = data
    } catch (err) {
        console.error('Event loading error:', err)
        toast.error('Failed to load events.')
    }
})

function editEvent(event) {
    router.push({ name: 'EditEvent', params: { link: event.link } })
}

async function deleteEvent(event) {
    try {
        if (!confirm(`Are you sure you want to delete "${event.name}"?`)) return

        await api.deleteEvent(`events/${event.link}/`)

        events.value.created = events.value.created.filter(e => e.link !== event.link)

        toast.success('Event deleted successfully.')
    } catch (err) {
        console.error('Delete failed:', err)
        toast.error('Failed to delete event.')
    }
}

function goToEvent(link) {
    router.push(`/events/${link}`)
}

// Exclude events the user created from the joined list
const filteredJoinedEvents = computed(() => {
    const fullName = `${currentUser.value?.first_name} ${currentUser.value?.last_name}`.trim()
    return events.value.joined.filter(e => e.coordinator_name !== fullName)
})
</script>

<style scoped>
.event-list-container {
    display: flex;
    justify-content: space-between;
    gap: 2rem;
    padding: 2rem;
    background-color: #eaf5ff;
}

.event-column {
    flex: 1;
    background-color: #ffffff;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.event-column h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #333;
}

.event-card {
    background-color: #f5faff;
    border: 1px solid #d8e6f3;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
    transition: background-color 0.2s;
}

.event-card.clickable:hover {
    background-color: #e0f0ff;
    cursor: pointer;
}

.event-card.empty {
    color: #888;
    font-style: italic;
}

.event-card h3 {
    margin: 0 0 0.5rem;
    font-weight: 600;
    color: #1d3557;
}

.event-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.hosted-text {
    font-size: 0.9rem;
    color: #555;
}
</style>
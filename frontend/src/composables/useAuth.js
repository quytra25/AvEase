import { ref, computed } from 'vue'
import api from '@/services/api'

// holds the logged-in user (or null if guest)
const user = ref(null)

// expose a readonly ref for the rest of the app to use
export const currentUser = user

export const isAuthenticated = computed(() => false)

// to fetch user from the API
export async function fetchCurrentUser() {
    try {
        const { data } = await import('@/services/api').then(m => m.default.getCurrentUser())
        user.value = data
    } catch {
        user.value = null
    }
}

export function useAuth() {
    // convenience boolean
    const isAuthenticated = computed(() => !!currentUser.value)
    return { currentUser, isAuthenticated }
}
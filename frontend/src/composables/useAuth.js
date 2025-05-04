import { ref } from 'vue'
import apiService from '@/services/api'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const api = apiService.axios

export const currentUser = ref(null)
export const isAuthenticated = ref(false)
export const loading = ref(false)

export function useAuth() {
    const router = useRouter()
    const toast = useToast()
    
    const fetchCurrentUser = async () => {
        try {
            const { data } = await api.get('/current-user/')
            if (data && data.email) {
                currentUser.value = data
                isAuthenticated.value = true
            } else {
                currentUser.value = null
                isAuthenticated.value = false
            }
        } catch {
            currentUser.value = null
            isAuthenticated.value = false
        }
    }

    const login = async (email, password) => {
        loading.value = true
        try {
            await api.post('/login/', { email, password })
            await fetchCurrentUser()
            toast.success('Logged in successfully!')
            router.push('/')
        } catch (err) {
            toast.error('Login failed. Check your credentials.')
        } finally {
            loading.value = false
        }
    }

    const signup = async (payload) => {
        loading.value = true
        try {
            const response = await api.post('/signup/', payload)
            if (response.status === 200 || response.status === 201) {
                try {
                    await login(payload.email, payload.password)
                    return true
                } catch (err) {
                    console.error("Login after signup failed", err)
                    return false
                }
            }
        } catch (err) {
            const errorMsg = err.response?.data?.error || "Signup failed. Please check your input."
            toast.error(errorMsg)
            console.error("Signup error:", err)
            return false
        } finally {
            loading.value = false
        }
    }

    const logout = async () => {
        try {
            const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1]
            await api.post('/logout/', null, {
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                withCredentials: true,
            })

            currentUser.value = null
            isAuthenticated.value = false
            toast.success('Logged out successfully!')
            router.push('/login')
        } catch (err) {
            console.error("Logout error:", err)
            toast.error('Logout failed.')
        }
    }

    return {
        currentUser,
        isAuthenticated,
        loading,
        login,
        signup,
        logout,
        fetchCurrentUser,
    }
}
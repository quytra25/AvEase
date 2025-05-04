<template>
    <Spinner v-if="loading" />
    <div class="auth-container">
    <h1>{{ isLogin ? 'Login' : 'Sign Up' }}</h1>
    <form @submit.prevent="isLogin ? handleLogin() : handleSignup()">
        <div class="field">
        <label>Email</label>
        <input v-model="email" type="email" placeholder="e.g. user@example.com" />
        </div>

        <div v-if="!isLogin" class="field-row">
        <div class="field">
            <label>First Name</label>
            <input v-model="firstName" type="text" placeholder="First Name" />
        </div>
        <div class="field">
            <label>Last Name</label>
            <input v-model="lastName" type="text" placeholder="Last Name" />
        </div>
        </div>

        <div class="field password-wrapper">
        <label>Password</label>
        <div class="password-input">
            <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Enter your password" />
            <span class="toggle-icon" @click="showPassword = !showPassword">
            <i class="fas" :class="showPassword ? 'fa-eye-slash' : 'fa-eye'"></i>
            </span>
        </div>
        </div>

        <div v-if="!isLogin" class="field password-wrapper">
        <label>Confirm Password</label>
        <div class="password-input">
            <input :type="showPassword ? 'text' : 'password'" v-model="confirmPassword" placeholder="Confirm your password" />
            <span class="toggle-icon" @click="showPassword = !showPassword">
            <i class="fas" :class="showPassword ? 'fa-eye-slash' : 'fa-eye'"></i>
            </span>
        </div>
        </div>

        <button type="submit" class="btn is-primary" :disabled="loading">
        {{ isLogin ? 'Login' : 'Create Account' }}
        </button>

        <p class="switch-mode">
        <span>{{ isLogin ? 'New user?' : 'Already have an account?' }}</span>
        <a href="#" @click.prevent="isLogin = !isLogin">{{ isLogin ? 'Sign up' : 'Login' }}</a>
        </p>
    </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useToast } from 'vue-toastification'
import Spinner from '@/components/Spinner.vue'
import { useRouter } from 'vue-router'

const { login, signup, loading } = useAuth()
const toast = useToast()
const router = useRouter()

const isLogin = ref(true)
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const firstName = ref('')
const lastName = ref('')
const showPassword = ref(false)

const handleLogin = () => {
    if (!email.value || !password.value) {
        toast.error("Please fill in all fields")
        return
    }
    login(email.value, password.value)
}

const handleSignup = async () => {
    try {
        if (!email.value || !password.value || !confirmPassword.value || !firstName.value || !lastName.value) {
            toast.error("All fields are required")
            return
        }

        if (password.value !== confirmPassword.value) {
            toast.error("Passwords do not match")
            return
        }

        const success = await signup({
            email: email.value,
            password: password.value,
            first_name: firstName.value,
            last_name: lastName.value
        })

        if (success) {
            toast.success("Sign-up successful!")
            router.push('/')
        } else {
            toast.error("Sign-up failed. Please check your input.")
        }
    } catch (err) {
        console.log("Signup error:", err)
        toast.error("An unexpected error occurred.")
    }
}
</script>

<style scoped>
.auth-container {
    max-width: 400px;
    margin: 40px auto;
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.field {
    margin-bottom: 1rem;
    text-align: left;
}

.field label {
    font-weight: bold;
    display: block;
    margin-bottom: 0.3rem;
}

input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.field-row {
    display: flex;
    gap: 0.5rem;
}

.password-wrapper .password-input {
    display: flex;
    align-items: center;
    position: relative;
}

.password-input input {
    width: 100%;
    padding-right: 2.5rem;
}

.toggle-icon {
    position: absolute;
    right: 10px;
    cursor: pointer;
    color: #555;
}

.btn {
    width: 100%;
    padding: 0.6rem;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    background-color: #00d1b2;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.btn:hover {
    background-color: #00b89c;
}

.switch-mode {
    margin-top: 1rem;
    font-size: 0.9rem;
}

.switch-mode a {
    color: #3e8ed0;
    font-weight: bold;
    margin-left: 5px;
    cursor: pointer;
}
</style>
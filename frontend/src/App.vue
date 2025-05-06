<template>
    <nav class="navbar is-link" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" @click="toggleMobileMenu">
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
            </a>
        </div>

        <div :class="['navbar-menu', { 'is-active': mobileMenu }]">
            <div class="navbar-start">
                <router-link class="navbar-item" to="/">Create Event</router-link>
                <router-link v-if="isAuthenticated" class="navbar-item" to="/events">My Events</router-link>
            </div>

            <div class="navbar-end">
                <div class="navbar-item">
                    <div class="buttons">
                        <span v-if="isAuthenticated" class="has-text-white mr-2">Hi, {{ currentUser?.first_name }}</span>
                        <router-link v-if="!isAuthenticated" class="button is-light" to="/login">Login</router-link>
                        <button v-else class="button is-danger" @click="handleLogout">Logout</button>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <section class="section">
        <div class="container">
            <router-view />
        </div>
    </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const { isAuthenticated, logout, currentUser } = useAuth()
const router = useRouter()
const mobileMenu = ref(false)

function toggleMobileMenu() {
    mobileMenu.value = !mobileMenu.value
}

async function handleLogout() {
    await logout()
    router.push('/login')
}
</script>

<style>
.router-link-active.navbar-item {
    font-weight: bold;
    background-color: rgba(255, 255, 255, 0.1);
}

.section {
    padding-top: 1rem !important;
}

.container {
    margin-top: 0 !important;
}
</style>
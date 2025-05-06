<template>
    <nav class="navbar is-link" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" @click="toggleMobileMenu">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        </a>
    </div>

    <div class="navbar-menu is-flex is-align-items-center w-100">
        <!-- Left: Navigation -->
        <div class="navbar-start">
        <router-link class="navbar-item" to="/">Create Event</router-link>
        <router-link v-if="isAuthenticated" class="navbar-item" to="/events">My Events</router-link>
        </div>

        <!-- Center: Animated Brand -->
        <div class="navbar-center is-flex-grow-1 is-flex is-justify-content-center">
        <a class="navbar-item brand-title">
            <span class="start">Av</span>
            <transition name="fade-collapse">
            <span v-if="!collapsed" class="middle">ailabilit</span>
            </transition>
            <span class="end">Ease</span>
        </a>
        </div>

        <!-- Right: User + Logout -->
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const { isAuthenticated, logout, currentUser } = useAuth()
const router = useRouter()
const mobileMenu = ref(false)
const collapsed = ref(false)

function toggleMobileMenu() {
  mobileMenu.value = !mobileMenu.value
}

async function handleLogout() {
  await logout()
  router.push('/login')
}

onMounted(() => {
  setTimeout(() => {
    collapsed.value = true
  }, 3000)
})
</script>

<style>
.brand-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  font-family: 'Segoe UI', sans-serif;
}

.brand-title span {
  transition: all 0.5s ease;
  display: inline-block;
}

.fade-collapse-enter-active,
.fade-collapse-leave-active {
  transition: opacity 0.5s ease, width 0.5s ease;
}
.fade-collapse-leave-to {
  opacity: 0;
  width: 0;
  overflow: hidden;
  display: inline-block;
}

.navbar-center {
  flex: 1;
}

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
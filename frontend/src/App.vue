<template>
    <nav class="p-4 border-b flex space-x-4">
        <router-link to="/">Home - Create Event</router-link>
        <router-link v-if="isAuthenticated" to="/events">All Events</router-link>
        <router-link v-if="!isAuthenticated" to="/login">Login</router-link>
    </nav>
    <router-view/>
</template>

<script setup>
import { useAuth } from '@/composables/useAuth'
const { isAuthenticated } = useAuth()
</script>

<style>
</style>
<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center px-4">
        <div class="w-full max-w-3xl bg-white rounded-2xl shadow-lg p-8 md:p-12">
            <div class="text-center mb-8">
                <h1 class="text-3xl md:text-4xl font-extrabold text-blue-700 mb-2">
                    Create an Event
                </h1>
                <p class="text-gray-600 text-md md:text-lg">
                    Choose the format, add your details, and get a shareable link.
                </p>
            </div>
            <CreateEventForm />
        </div>
    </div>
</template>

<script setup>
import CreateEventForm from '@/components/CreateEventForm.vue'
</script>  
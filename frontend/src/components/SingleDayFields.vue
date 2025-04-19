<script setup>
const modelValue = defineProps(['modelValue'])
</script>

<template>
    <div class="space-y-2">
        <label>Date Range:</label>
        <input type="date" v-model="modelValue.start_date" required/>
        to
        <input type="date" v-model="modelValue.end_date" required/>

        <label>Time:</label>
        <input type="time" v-model="modelValue.start_time" required/>
        to
        <input type="time" v-model="modelValue.end_time" required/>
    </div>
</template>

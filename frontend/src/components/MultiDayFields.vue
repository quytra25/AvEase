<script setup>
import { defineProps } from 'vue'
const modelValue = defineProps(['modelValue'])
</script>

<template>
    <div class="space-y-2">
    <label>Date Range:</label>
    <input type="date" v-model="modelValue.start_date" required/>
    to
    <input type="date" v-model="modelValue.end_date" required/>

    <label>How many days?</label>
    <input type="number" min="1" v-model="modelValue.num_days" required/>
    </div>
</template>
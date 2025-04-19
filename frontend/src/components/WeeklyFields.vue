<template>
    <div class="space-y-4">
        <!-- Days -->
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Select Days</label>
            <div class="grid grid-cols-4 gap-2">
                <label
                v-for="day in days"
                :key="day.value"
                class="inline-flex items-center space-x-1 text-sm"
                >
                <input
                    type="checkbox"
                    :value="day.value"
                    v-model="model.days"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span>{{ day.label }}</span>
                </label>
            </div>
        </div>

        <!-- Time Range -->
        <div class="flex gap-4 items-center">
            <label class="text-sm font-medium text-gray-700">From</label>
            <input
                type="time"
                v-model="model.start_time"
                class="border border-gray-300 rounded px-3 py-2 w-full"
            />

            <label class="text-sm font-medium text-gray-700">To</label>
            <input
                type="time"
                v-model="model.end_time"
                class="border border-gray-300 rounded px-3 py-2 w-full"
            />
        </div>
    </div>
</template>
  
<script setup>
import { computed } from 'vue'
const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const model = computed({
    get: () => props.modelValue,
    set: (val) => emit('update:modelValue', val)
})

const days = [
    { value: 'mon', label: 'Mon' },
    { value: 'tue', label: 'Tue' },
    { value: 'wed', label: 'Wed' },
    { value: 'thu', label: 'Thu' },
    { value: 'fri', label: 'Fri' },
    { value: 'sat', label: 'Sat' },
    { value: 'sun', label: 'Sun' }
]
</script>  
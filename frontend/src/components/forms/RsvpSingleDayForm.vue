<template>
    <form @submit.prevent="submit">
        <input v-model="local.name" placeholder="Name" required />
        <input v-model="local.description" placeholder="Description" />
        <input v-model="local.location" placeholder="Location" />

        <label>
            Date
            <input type="date" v-model="local.date" required />
        </label>

        <label>
            <input type="checkbox" v-model="local.is_all_day" />
            All Day
        </label>

        <input v-if="!local.is_all_day" type="time" v-model="local.start_time" required />
        <input v-if="!local.is_all_day" type="time" v-model="local.end_time" required />

        <button type="button" @click="back">‹ Back</button>
        <button type="submit">Create</button>
    </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({ formData: Object })
const emit = defineEmits(['submit','back'])
const local = reactive({ ...props.formData })

watch(local, () => { Object.assign(props.formData, local) }, { deep: true })

function submit() {
    emit('submit', { ...props.formData })
}

function back() {
    emit('back')
}
</script>
<template>
    <form @submit.prevent="submit">
        <label>
            Name
            <input v-model="local.name" required />
        </label>

        <label>
            Description
            <textarea v-model="local.description"></textarea>
        </label>

        <label>
            Location
            <input v-model="local.location" />
        </label>
        
        <!-- Weekly‑specific fields -->
        <fieldset>
            <legend>Days of Week</legend>
            <label><input type="checkbox" v-model="local.mon_selected" />Monday</label>
            <label><input type="checkbox" v-model="local.tue_selected" />Tuesday</label>
            <label><input type="checkbox" v-model="local.wed_selected" />Wednesday</label>
            <label><input type="checkbox" v-model="local.thur_selected" />Thursday</label>
            <label><input type="checkbox" v-model="local.fri_selected" />Friday</label>
            <label><input type="checkbox" v-model="local.sat_selected" />Saturday</label>
            <label><input type="checkbox" v-model="local.sun_selected" />Sunday</label>
        </fieldset>

        <label>
            Start Time
            <input v-model="local.start_time" type="time" required />
        </label>

        <label>
            End Time
            <input v-model="local.end_time" type="time" required />
        </label>

        <button type="button" @click="back">‹ Back</button>
        <button type="submit">Create</button>
    </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
    formData: Object
})
const local = reactive({ ...props.formData })

// keep parent’s formData updated
watch(local, v => { Object.assign(props.formData, v) }, { deep: true })

function submit() {
    // call parent with the entire formData
    $emit('submit', { ...props.formData })
}

function back() {
    emit('back')
}
</script>
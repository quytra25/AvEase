<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const message = ref('Loading...')

onMounted(async () => {
  const res = await axios.get('http://127.0.0.1:8000/api/test/')
  message.value = res.data.message
})

</script>

<template>
  <h1>{{ message }}</h1>
</template>

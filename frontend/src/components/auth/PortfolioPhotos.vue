<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const photosLoading = ref(true)
const photosList = ref([])

const getPhotosData = async () => {
  try {
    const response = await axios.get('/portfolio/photos/')
    photosList.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    photosLoading.value = false
  }
}

onMounted(() => {
  getPhotosData()
})
</script>

<template>
  <div class="portfolio-photos">
    {{ $t('auth.portfolio.photos') }}
  </div>
</template>

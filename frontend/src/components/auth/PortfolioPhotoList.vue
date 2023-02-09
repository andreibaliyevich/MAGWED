<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const photosLoading = ref(true)
const photoList = ref([])

const getPhotosData = async () => {
  try {
    const response = await axios.get('/portfolio/photos/')
    photoList.value = response.data
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
  <div class="portfolio-photo-list">
    {{ $t('auth.portfolio.photos') }}
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const albumsLoading = ref(true)
const albumList = ref([])

const getPhotosData = async () => {
  try {
    const response = await axios.get('/portfolio/albums/')
    albumList.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    albumsLoading.value = false
  }
}

onMounted(() => {
  getPhotosData()
})
</script>

<template>
  <div class="portfolio-albums-view">
    {{ $t('auth.portfolio.albums') }}
  </div>
</template>

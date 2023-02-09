<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const albumsLoading = ref(true)
const albumList = ref([])

const getAlbumsData = async () => {
  try {
    const response = await axios.get('/portfolio/photos/')
    albumList.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    albumsLoading.value = false
  }
}

onMounted(() => {
  getAlbumsData()
})
</script>

<template>
  <div class="portfolio-album-list">
    {{ $t('auth.portfolio.albums') }}
  </div>
</template>

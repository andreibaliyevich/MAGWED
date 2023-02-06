<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const albumsLoading = ref(true)
const albumsList = ref([])

const getAlbumsData = async () => {
  try {
    const response = await axios.get('/portfolio/albums/')
    albumsList.value = response.data
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
  <div class="portfolio-albums">
    {{ $t('auth.portfolio.albums') }}
  </div>
</template>

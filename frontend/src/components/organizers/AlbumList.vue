<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const props = defineProps({
  userUUID: {
    type: String,
    required: true
  }
})

const albumLoading = ref(true)
const albumMoreLoading = ref(false)
const albumList = ref([])
const nextURL = ref(null)

const getOrganizerAlbums = async () => {
  try {
    const response = await axios.get(
      '/portfolio/album/list/'
        + '?owner='
        + props.userUUID
    )
    albumList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    albumLoading.value = false
  }
}

const getMoreOrganizerAlbums = async () => {
  albumMoreLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    albumList.value = [...albumList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    albumMoreLoading.value = false
  }
}

onMounted(() => {
  getOrganizerAlbums()
})
</script>

<template>
  <div class="album-list">
    <LoadingIndicator v-if="albumLoading" />
    <div
      v-else-if="albumList.length > 0"
      class="row g-3 mt-3"
    >
      <div
        v-for="albumItem in albumList"
        :key="albumItem.uuid"
        class="col-12 col-md-6 col-lg-4 col-xl-3"
      >
        <div class="card border border-light shadow-sm h-100">
          <LocaleRouterLink
            routeName="AlbumDetail"
            :routeParams="{ uuid: albumItem.uuid }"
          >
            <img
              :src="albumItem.thumbnail"
              :alt="albumItem.title"
              class="card-img-top"
            >
          </LocaleRouterLink>
          <div class="card-body">
            <LocaleRouterLink
              routeName="AlbumDetail"
              :routeParams="{ uuid: albumItem.uuid }"
              class="text-decoration-none link-dark"
            >
              <h5 class="card-title">{{ albumItem.title }}</h5>
            </LocaleRouterLink>
            <div class="d-flex justify-content-between mt-1">
              <div>
                <i class="fa-regular fa-eye"></i>
                {{ albumItem.view_count }}
              </div>
              <div>
                <i class="fa-regular fa-heart"></i>
                {{ albumItem.like_count }}
              </div>
              <div>
                <i class="fa-regular fa-star"></i>
                {{ albumItem.rating }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="nextURL" v-intersection="getMoreOrganizerAlbums"></div>
      <LoadingIndicator v-if="albumMoreLoading" />
    </div>
    <div
      v-else
      class="lead d-flex justify-content-center py-3"
    >
      {{ $t('portfolio.no_albums') }}
    </div>
  </div>
</template>

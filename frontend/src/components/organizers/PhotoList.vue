<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const props = defineProps({
  userUUID: {
    type: String,
    required: true
  }
})

const photoLoading = ref(true)
const photoMoreLoading = ref(false)
const photoList = ref([])
const nextURL = ref(null)

const getOrganizerPhotos = async () => {
  try {
    const response = await axios.get(
      '/portfolio/photos/list/'
        + '?owner='
        + props.userUUID
        + '&album_is_null=true'
    )
    photoList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    photoLoading.value = false
  }
}

const getMoreOrganizerPhotos = async () => {
  photoMoreLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    photoList.value = [...photoList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    photoMoreLoading.value = false
  }
}

onMounted(() => {
  getOrganizerPhotos()
})
</script>

<template>
  <div class="photo-list">
    <LoadingIndicator v-if="photoLoading" />
    <div
      v-else-if="photoList.length > 0"
      class="row g-3 mt-3"
    >
      <div
        v-for="photoItem in photoList"
        :key="photoItem.uuid"
        class="col-12 col-md-6 col-lg-4 col-xl-3"
      >
        <div class="card border border-0 h-100">
          <LocaleRouterLink
            routeName="PhotoDetail"
            :routeParams="{ uuid: photoItem.uuid }"
            :routeQuery="{ from: this.$route.query.filter }"
            class="link-light"
          >
            <img
              :src="photoItem.thumbnail"
              class="card-img"
            >
            <div class="card-img-overlay">
              <div class="position-absolute top-0 start-50 translate-middle-x mt-2">
                <h5 class="card-title text-center">{{ photoItem.title }}</h5>
              </div>
              <div class="position-absolute bottom-0 start-0 ms-2 mb-2">
                <i class="fa-regular fa-eye"></i>
                {{ photoItem.num_views }}
              </div>
              <div class="position-absolute bottom-0 start-50 translate-middle-x mb-2">
                <i class="fa-regular fa-heart"></i>
                {{ photoItem.likes_count }}
              </div>
              <div class="position-absolute bottom-0 end-0 me-2 mb-2">
                <i class="fa-regular fa-star"></i>
                {{ photoItem.rating }}
              </div>
            </div>
          </LocaleRouterLink>
        </div>
      </div>
      <div v-if="nextURL" v-intersection="getMoreOrganizerPhotos"></div>
      <LoadingIndicator v-if="photoMoreLoading" />
    </div>
    <div
      v-else
      class="lead d-flex justify-content-center py-3"
    >
      {{ $t('portfolio.no_photos') }}
    </div>
  </div>
</template>

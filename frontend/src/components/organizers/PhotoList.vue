<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const props = defineProps({
  userUUID: {
    type: String,
    required: true
  }
})

const photoListLoading = ref(true)
const photoList = ref([])
const nextURL = ref(null)

const getPhotoList = async () => {
  try {
    const response = await axios.get('/portfolio/photo/list/', {
      params: {
        author: props.userUUID,
        album_is_null: true
      }
    })
    photoList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    photoListLoading.value = false
  }
}

const getMorePhotoList = async () => {
  photoListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    photoList.value = [...photoList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    photoListLoading.value = false
  }
}

onMounted(() => {
  getPhotoList()
})
</script>

<template>
  <div class="photo-list">
    <div
      v-if="photoList.length > 0"
      class="row g-3 mt-3"
    >
      <div
        v-for="photoItem in photoList"
        :key="photoItem.uuid"
        class="col-12 col-md-6 col-lg-4 col-xl-3"
      >
        <div class="card border border-0 h-100">
          <router-link
            :to="{
              name: 'PhotoDetail',
              params: { uuid: photoItem.uuid },
              query: {
                from: 'author',
                author: props.userUUID
              }
            }"
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
                {{ photoItem.view_count }}
              </div>
              <div class="position-absolute bottom-0 start-50 translate-middle-x mb-2">
                <i class="fa-regular fa-heart"></i>
                {{ photoItem.like_count }}
              </div>
              <div class="position-absolute bottom-0 end-0 me-2 mb-2">
                <i class="fa-regular fa-star"></i>
                {{ photoItem.rating }}
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
    <div
      v-else-if="!photoListLoading"
      class="lead d-flex justify-content-center py-3"
    >
      {{ $t('portfolio.no_photos') }}
    </div>
    <div
      v-if="nextURL"
      style="min-height: 1px; margin-bottom: 1px;"
      v-intersection="{
        'scrollArea': null,
        'callbackFunction': getMorePhotoList,
        'functionArguments': []
      }"
    ></div>
    <LoadingIndicator v-if="photoListLoading" />
  </div>
</template>

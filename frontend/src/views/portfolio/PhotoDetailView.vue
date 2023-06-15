<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import NotFound from '@/components/NotFound.vue'

const route = useRoute()

const photoLoading = ref(true)
const photoData = ref({
  uuid: '',
  owner: {
    name: '',
    avatar: null,
    profile_url: ''
  },
  album: null,
  image: null,
  device: '',
  f_number: 0.00,
  exposure_time: '',
  focal_length: 0.00,
  photographic_sensitivity: 0,
  title: '',
  description: '',
  tags: [],
  uploaded_at: null,
  num_views: 0,
  likes_count: 0,
  rating: 0
})

const errorStatus = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

const getPhotoData = async () => {
  try {
    const response = await axios.get(
      '/portfolio/photos/detail/'
        + route.params.uuid
    )
    photoData.value = response.data
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    photoLoading.value = false
  }
}

onMounted(() => {
  getPhotoData()
})
</script>

<template>
  <div class="photo-detail-view">
    <LoadingIndicator
      v-if="photoLoading"
      class="my-5"
    />
    <NotFound v-else-if="errorStatus == 404" />
    <div
      v-else
      class="container my-5"
    >
      <div class="card border border-light shadow-sm">
        <div class="d-flex justify-content-center">
          <img
            :src="photoData.image"
            class="card-img-top"
          >
        </div>
        <div class="card-body mx-3 mx-lg-5">
          <div class="row">
            <div class="col-lg-6">
              <div class="d-flex justify-content-center justify-content-lg-start">
                <div class="d-inline-block">
                  <h1 class="h3">{{ photoData.title }}</h1>
                  <ul class="list-inline mb-2">
                    <li class="list-inline-item">
                      <i class="fa-regular fa-calendar-days"></i>
                      {{ $t('portfolio.uploaded') }}
                      {{ getLocaleDateString(photoData.uploaded_at) }}
                    </li>
                    <li class="list-inline-item ms-3">
                      <i class="fa-regular fa-eye"></i>
                      {{ photoData.num_views }}
                    </li>
                    <li class="list-inline-item ms-3">
                      <i class="fa-regular fa-star"></i>
                      {{ photoData.rating }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="col-lg-6">
              <div class="d-flex justify-content-center justify-content-lg-end">
                <button
                  type="button"
                  class="btn btn-outline-brand"
                >
                  <i class="fa-regular fa-heart"></i>
                  {{ photoData.likes_count }}
                </button>
                <button
                  type="button"
                  class="btn btn-light ms-2"
                >
                  <i class="fa-regular fa-bookmark"></i>
                  Add to favourites
                </button>
              </div>
            </div>
          </div>

          <div class="d-flex align-items-center mb-3">
            <LocaleRouterLink
              routeName="OrganizerDetail"
              :routeParams="{ profile_url: photoData.owner.profile_url }"
            >
              <UserAvatar
                :src="photoData.owner.avatar"
                :width="32"
                :height="32"
              />
            </LocaleRouterLink>
            <LocaleRouterLink
              routeName="OrganizerDetail"
              :routeParams="{ profile_url: photoData.owner.profile_url  }"
              class="text-decoration-none link-dark ms-2"
            >
              {{ photoData.owner.name }}
            </LocaleRouterLink>
          </div>

          <div class="row flex-lg-row-reverse align-items-center g-3">
            <div class="col-lg-4">
              <ul class="list-group list-group-flush">
                <li
                  v-if="photoData.device"
                  class="list-group-item"
                >
                  <i class="fa-solid fa-camera"></i>
                  {{ photoData.device }}
                </li>
                <li
                  v-if="photoData.f_number"
                  class="list-group-item"
                >
                  {{ $t('portfolio.f_number') }}:
                  f/{{ photoData.f_number }}
                </li>
                <li
                  v-if="photoData.exposure_time"
                  class="list-group-item"
                >
                  {{ $t('portfolio.exposure_time') }}:
                  {{ photoData.exposure_time }}
                </li>
                <li
                  v-if="photoData.focal_length"
                  class="list-group-item"
                >
                  {{ $t('portfolio.focal_length') }}:
                  {{ photoData.focal_length }}
                </li>
                <li
                  v-if="photoData.photographic_sensitivity"
                  class="list-group-item"
                >
                  {{ $t('portfolio.photographic_sensitivity') }}:
                  {{ photoData.photographic_sensitivity }}
                </li>
              </ul>
            </div>
            <div class="col-lg-8">
              <p
                v-if="photoData.description"
                class="card-text lead"
              >
                {{ photoData.description }}
              </p>
              <div
                v-if="photoData.tags.length > 0"
                class="d-inline-block"
              >
                <div class="row g-1">
                  <div
                    v-for="tagValue in photoData.tags"
                    :key="tagValue"
                    class="col"
                  >
                    <a
                      :href="tagValue"
                      role="button"
                      class="btn btn-light btn-sm"
                    >
                      #{{ tagValue }}
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-img-top {
  height: auto;
  width: 100%;
  max-width: 720px;
}
</style>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import NotFound from '@/components/NotFound.vue'

const route = useRoute()

const albumLoading = ref(true)
const albumData = ref({
  uuid: '',
  owner: {
    name: '',
    avatar: null,
    profile_url: ''
  },
  image: null,
  title: '',
  description: '',
  tags: [],
  created_at: null,
  num_views: 0,
  likes_count: 0,
  rating: 0
})

const photosLoading = ref(true)
const photosMoreLoading = ref(false)
const photoList = ref([])
const nextURL = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

const errorStatus = ref(null)

const getAlbumPhotos = async () => {
  try {
    const response = await axios.get(
      '/portfolio/photos/list/'
        + '?album='
        + albumData.value.uuid
    )
    photoList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    photosLoading.value = false
  }
}

const getMoreOrganizerPhotos = async () => {
  photosMoreLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    photoList.value = [...photoList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    photosMoreLoading.value = false
  }
}

const getAlbumData = async () => {
  try {
    const response = await axios.get(
      '/portfolio/albums/detail/'
        + route.params.uuid
        + '/'
    )
    albumData.value = response.data
    getAlbumPhotos()
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    albumLoading.value = false
  }
}

onMounted(() => {
  getAlbumData()
})
</script>

<template>
  <div class="album-detail-view">
    <LoadingIndicator
      v-if="albumLoading"
      class="my-5"
    />
    <NotFound v-else-if="errorStatus == 404" />
    <div
      v-else
      class="container my-5"
    >
      <div class="card border border-light shadow-sm">
        <img
          :src="albumData.image"
          class="card-img-top"
        >
        <div class="card-body mx-3 mx-lg-5">
          <div class="row">
            <div class="col-lg-6">
              <div class="d-flex justify-content-center justify-content-lg-start">
                <div class="d-inline-block">
                  <h1 class="h3">{{ albumData.title }}</h1>
                  <ul class="list-inline mb-2">
                    <li class="list-inline-item">
                      <i class="fa-regular fa-calendar-days"></i>
                      {{ $t('portfolio.created') }}
                      {{ getLocaleDateString(albumData.created_at) }}
                    </li>
                    <li class="list-inline-item ms-3">
                      <i class="fa-regular fa-eye"></i>
                      {{ albumData.num_views }}
                    </li>
                    <li class="list-inline-item ms-3">
                      <i class="fa-regular fa-star"></i>
                      {{ albumData.rating }}
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
                  {{ albumData.likes_count }}
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
              :routeParams="{ profile_url: albumData.owner.profile_url }"
            >
              <UserAvatar
                :src="albumData.owner.avatar"
                :width="32"
                :height="32"
              />
            </LocaleRouterLink>
            <LocaleRouterLink
              routeName="OrganizerDetail"
              :routeParams="{ profile_url: albumData.owner.profile_url  }"
              class="text-decoration-none link-dark ms-2"
            >
              {{ albumData.owner.name }}
            </LocaleRouterLink>
          </div>

          <p
            v-if="albumData.description"
            class="card-text lead"
          >
            {{ albumData.description }}
          </p>

          <div
            v-if="albumData.tags.length > 0"
            class="d-inline-block"
          >
            <div class="row g-1">
              <div
                v-for="tagValue in albumData.tags"
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

      <LoadingIndicator v-if="photosLoading" />
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
        <LoadingIndicator v-if="photosMoreLoading" />
      </div>
      <div
        v-else
        class="lead d-flex justify-content-center py-3"
      >
        {{ $t('portfolio.no_photos') }}
      </div>
    </div>
  </div>
</template>

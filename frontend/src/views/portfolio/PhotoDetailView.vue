<script setup>
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import CommentList from '@/components/comments/CommentList.vue'
import NotFound from '@/components/NotFound.vue'
import FavoriteDropdownItem from '@/components/FavoriteDropdownItem.vue'
import ReportDropdownItemModal from '@/components/ReportDropdownItemModal.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const photoLoading = ref(true)
const photoData = ref({
  author: {
    name: '',
    avatar: null,
    profile_url: null
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
  view_count: 0,
  like_count: 0,
  liked: null,
  rating: 0,
  favorite: null,
  prev_photo_uuid: null,
  next_photo_uuid: null
})

const { getLocaleDateString } = useLocaleDateTime()

const upViewCountTimeout = ref(null)
const errorStatus = ref(null)

const upPhotoViewCount = async () => {
  try {
    const response = await axios.post(
      '/portfolio/photo/up-view-count/'
        + route.params.uuid
        + '/'
    )
    photoData.value.view_count += 1
  } catch (error) {
    console.error(error)
  }
}

const getPhotoData = async () => {
  photoLoading.value = true

  let params = new URLSearchParams()
  if (route.query.from === 'popular') {
    params.append('ordering', '-rating')
  } else if (route.query.from === 'fresh') {
    params.append('ordering', '-uploaded_at')
  } else if (route.query.from === 'editors') {
    params.append('editors_choice', true)
  } else if (route.query.from === 'album') {
    params.append('album', route.query.album)
  } else if (route.query.from === 'author') {
    params.append('author', route.query.author)
    params.append('album_is_null', true)
  } else if (route.query.from === 'tags') {
    params.append('tags', route.query.tags)
  } else {
    params.append('ordering', 'rating')
  }

  try {
    const response = await axios.get(
      '/portfolio/photo/retrieve/'
        + route.params.uuid
        + '/',
      { params: params }
    )
    photoData.value = response.data
    upViewCountTimeout.value = setTimeout(upPhotoViewCount, 3000)
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    photoLoading.value = false
  }
}

const likePhoto = async () => {
  try {
    const response = await axios.post(
      '/portfolio/photo/like/'
        + route.params.uuid
        + '/'
    )
    photoData.value.like_count += 1
    photoData.value.liked = true
  } catch (error) {
    console.error(error)
  }
}

const dislikePhoto = async () => {
  try {
    const response = await axios.delete(
      '/portfolio/photo/like/'
        + route.params.uuid
        + '/'
    )
    photoData.value.like_count -= 1
    photoData.value.liked = false
  } catch (error) {
    console.error(error)
  }
}

const keyUpArrowLeftRight = (event) => {
  if (event.keyCode === 37 && photoData.value.prev_photo_uuid) {
    router.push({
      params: { uuid: photoData.value.prev_photo_uuid },
      query: route.query
    })
  } else if (event.keyCode === 39 && photoData.value.next_photo_uuid) {
    router.push({
      params: { uuid: photoData.value.next_photo_uuid },
      query: route.query
    })
  }
}

watch(
  () => route.params.uuid,
  (newValue) => {
    if (route.name === 'PhotoDetail') {
      getPhotoData()
    }
  }
)

onMounted(() => {
  getPhotoData()
  window.addEventListener('keyup', keyUpArrowLeftRight)
})

onUnmounted(() => {
  clearTimeout(upViewCountTimeout.value)
  window.removeEventListener('keyup', keyUpArrowLeftRight)
})
</script>

<template>
  <div class="photo-detail-view">
    <LoadingIndicator
      v-if="photoLoading"
      class="my-5"
    />
    <NotFound v-else-if="errorStatus === 404" />
    <div
      v-else
      class="container my-5"
    >

      <div class="card border-0">
        <div class="d-flex justify-content-center">
          <img
            :src="photoData.image"
            class="card-img"
          >
          <div
            class="card-img-overlay mx-1"
            style="background-color: rgba(33, 37, 41, 0);"
          >
            <div
              v-if="photoData.prev_photo_uuid"
              class="position-absolute top-50 start-0 translate-middle-y"
            >
              <router-link
                :to="{
                  params: { uuid: photoData.prev_photo_uuid },
                  query: $route.query
                }"
                class="btn btn-light"
              >
                <i class="fa-solid fa-chevron-left"></i>
              </router-link>
            </div>
            <div
              v-if="photoData.next_photo_uuid"
              class="position-absolute top-50 end-0 translate-middle-y"
            >
              <router-link
                :to="{
                  params: { uuid: photoData.next_photo_uuid },
                  query: $route.query
                }"
                class="btn btn-light"
              >
                <i class="fa-solid fa-chevron-right"></i>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-3 mt-3">
        <div class="col-xl-7">
          <div class="card border border-light shadow-sm">
            <div class="card-body mx-3 mx-lg-1">

              <div class="row">
                <div class="col-lg-6">
                  <div class="d-flex justify-content-center justify-content-lg-start">
                    <div class="d-inline-block">
                      <h1
                        v-if="photoData.title"
                        class="h3"
                      >
                        {{ photoData.title }}
                      </h1>
                      <ul class="list-inline text-body-secondary mb-2">
                        <li class="list-inline-item">
                          <i class="fa-regular fa-calendar-days"></i>
                          {{ $t('portfolio.uploaded') }}
                          {{ getLocaleDateString(photoData.uploaded_at) }}
                        </li>
                        <li class="list-inline-item ms-3">
                          <i class="fa-regular fa-eye"></i>
                          {{ photoData.view_count }}
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
                  <div
                    v-if="userStore.isLoggedIn"
                    class="d-flex justify-content-center justify-content-lg-end"
                  >
                    <button
                      v-if="photoData.liked"
                      @click="dislikePhoto()"
                      type="button"
                      class="btn btn-brand"
                    >
                      <i class="fa-regular fa-heart"></i>
                      {{ photoData.like_count }}
                    </button>
                    <button
                      v-else
                      @click="likePhoto()"
                      type="button"
                      class="btn btn-outline-brand"
                    >
                      <i class="fa-regular fa-heart"></i>
                      {{ photoData.like_count }}
                    </button>

                    <div class="d-flex justify-content-end">
                      <div class="dropdown">
                        <button
                          type="button"
                          class="btn btn-light ms-2"
                          data-bs-toggle="dropdown"
                          data-bs-auto-close="true"
                          aria-expanded="false"
                        >
                          <i class="fa-solid fa-ellipsis"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end">
                          <li>
                            <FavoriteDropdownItem
                              :objFavorite="photoData.favorite"
                              contentType="photo"
                              :objectUUID="$route.params.uuid"
                              @updateFavorite="(status) => {
                                photoData.favorite = status
                              }"
                            />
                          </li>
                          <li>
                            <ReportDropdownItemModal
                              contentType="photo"
                              :objectUUID="$route.params.uuid"
                            />
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="row g-1 my-3">
                <div class="col-lg-6">
                  <div class="d-flex align-items-center justify-content-start">
                    <router-link
                      :to="{
                        name: 'OrganizerDetail',
                        params: { profile_url: photoData.author.profile_url }
                      }"
                    >
                      <UserAvatar
                        :src="photoData.author.avatar"
                        :width="32"
                        :height="32"
                      />
                    </router-link>
                    <router-link
                      :to="{
                        name: 'OrganizerDetail',
                        params: { profile_url: photoData.author.profile_url }
                      }"
                      class="text-decoration-none link-dark ms-2"
                    >
                      {{ photoData.author.name }}
                    </router-link>
                  </div>
                </div>
                <div class="col-lg-6">
                  <div
                    v-if="photoData.album"
                    class="d-flex align-items-center justify-content-start justify-content-lg-end"
                  >
                    <router-link
                      :to="{
                        name: 'AlbumDetail',
                        params: { uuid: photoData.album.uuid }
                      }"
                    >
                      <img
                        :src="photoData.album.thumbnail"
                        :width="32"
                        :height="32"
                        class="rounded-circle"
                      >
                    </router-link>
                    <router-link
                      :to="{
                        name: 'AlbumDetail',
                        params: { uuid: photoData.album.uuid }
                      }"
                      class="text-decoration-none link-dark ms-2"
                    >
                      {{ photoData.album.title }}
                    </router-link>
                  </div>
                </div>
              </div>

              <p
                v-if="photoData.description"
                class="card-text lead"
              >
                {{ photoData.description }}
              </p>

            </div>
          </div>

          <div
            v-if="photoData.device"
            class="card border border-light shadow-sm mt-2"
          >
            <div class="card-body mx-3 mx-lg-1">
              <div>
                <i class="fa-solid fa-camera"></i>
                {{ photoData.device }}
              </div>
              <div
                v-if="photoData.f_number
                  || photoData.exposure_time
                  || photoData.focal_length
                  || photoData.photographic_sensitivity"
                class="mt-2"
              >
                <span
                  v-if="photoData.f_number"
                  :class="{
                    'me-3': photoData.exposure_time
                      || photoData.focal_length
                      || photoData.photographic_sensitivity
                  }"
                >
                  f/{{ photoData.f_number }}
                </span>
                <span
                  v-if="photoData.exposure_time"
                  :class="{
                    'me-3': photoData.focal_length
                      || photoData.photographic_sensitivity
                  }"
                >
                  {{ photoData.exposure_time }}s
                </span>
                <span
                  v-if="photoData.focal_length"
                  :class="{ 'me-3': photoData.photographic_sensitivity }"
                >
                  {{ photoData.focal_length }}mm
                </span>
                <span v-if="photoData.photographic_sensitivity">
                  ISO {{ photoData.photographic_sensitivity }}
                </span>
              </div>
            </div>
          </div>

          <div
            v-if="photoData.tags.length > 0"
            class="card border border-light shadow-sm mt-2"
          >
            <div class="card-body mx-3 mx-lg-1">
              <div class="d-inline-block">
                <div class="row g-1">
                  <div
                    v-for="tag in photoData.tags"
                    :key="tag.uuid"
                    class="col"
                  >
                    <router-link
                      :to="{
                        name: 'TagDetail',
                        params: { uuid: tag.uuid },
                        query: { tab: 'photos' }
                      }"
                      class="btn btn-light btn-sm"
                    >
                      #{{ tag.name }}
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-xl-5">
          <div class="card border border-light shadow-sm">
            <div class="card-body mx-3 mx-lg-1">
              <CommentList
                contentType="photo"
                :objectUUID="$route.params.uuid"
              />
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.card-img {
  width: auto;
  max-width: 100%;
  height: 100%;
  max-height: 75vh;
}
</style>

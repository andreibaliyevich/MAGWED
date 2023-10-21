<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useUserStore } from '@/stores/user.js'
import CommentList from '@/components/comments/CommentList.vue'
import NotFound from '@/components/NotFound.vue'

const route = useRoute()
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
  favorite: null,
  rating: 0
})

const { getLocaleDateString } = useLocaleDateTime()

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
  try {
    const response = await axios.get(
      '/portfolio/photo/retrieve/'
        + route.params.uuid
        + '/'
    )
    photoData.value = response.data
    setTimeout(upPhotoViewCount, 3000)
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

const addPhotoToFavorites = async () => {
  try {
    const response = await axios.post('/social/favorite/', {
      'content_type': 'photo',
      'object_uuid': route.params.uuid
    })
    photoData.value.favorite = true
  } catch (error) {
    console.error(error)
  }
}

const removePhotoFromFavorites = async () => {
  try {
    const response = await axios.delete('/social/favorite/', {
      data: {
        'content_type': 'photo',
        'object_uuid': route.params.uuid
      }
    })
    photoData.value.favorite = false
  } catch (error) {
    console.error(error)
  }
}

watch(
  () => route.params.uuid,
  (newValue) => {
    if (route.name == 'PhotoDetail') {
      getPhotoData()
    }
  }
)

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

      <div class="d-flex justify-content-center">
        <img
          :src="photoData.image"
          class="card-img-top"
        >
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
                    <button
                      v-if="photoData.favorite"
                      @click="removePhotoFromFavorites()"
                      type="button"
                      class="btn btn-light ms-2"
                    >
                      <i class="fa-solid fa-bookmark"></i>
                      {{ $t('favorites.remove_from_favourites') }}
                    </button>
                    <button
                      v-else
                      @click="addPhotoToFavorites()"
                      type="button"
                      class="btn btn-light ms-2"
                    >
                      <i class="fa-regular fa-bookmark"></i>
                      {{ $t('favorites.add_to_favourites') }}
                    </button>
                  </div>
                </div>
              </div>

              <div class="row g-1 my-3">
                <div class="col-lg-6">
                  <div class="d-flex align-items-center justify-content-start">
                    <LocaleRouterLink
                      routeName="OrganizerDetail"
                      :routeParams="{ profile_url: photoData.author.profile_url }"
                    >
                      <UserAvatar
                        :src="photoData.author.avatar"
                        :width="32"
                        :height="32"
                      />
                    </LocaleRouterLink>
                    <LocaleRouterLink
                      routeName="OrganizerDetail"
                      :routeParams="{ profile_url: photoData.author.profile_url  }"
                      class="text-decoration-none link-dark ms-2"
                    >
                      {{ photoData.author.name }}
                    </LocaleRouterLink>
                  </div>
                </div>
                <div class="col-lg-6">
                  <div
                    v-if="photoData.album"
                    class="d-flex align-items-center justify-content-start justify-content-lg-end"
                  >
                    <LocaleRouterLink
                      routeName="AlbumDetail"
                      :routeParams="{ uuid: photoData.album.uuid }"
                    >
                      <img
                        :src="photoData.album.thumbnail"
                        :width="32"
                        :height="32"
                        class="rounded-circle"
                      >
                    </LocaleRouterLink>
                    <LocaleRouterLink
                      routeName="AlbumDetail"
                      :routeParams="{ uuid: photoData.album.uuid  }"
                      class="text-decoration-none link-dark ms-2"
                    >
                      {{ photoData.album.title }}
                    </LocaleRouterLink>
                  </div>
                </div>
              </div>

              <p
                v-if="photoData.description"
                class="card-text lead"
              >
                {{ photoData.description }}
              </p>

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

              <div
                v-if="photoData.tags.length > 0"
                class="d-inline-block mt-3"
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
.card-img-top {
  width: auto;
  max-width: 100%;
  height: 100%;
  max-height: 75vh;
}
</style>

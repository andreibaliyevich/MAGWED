<script setup>
import axios from 'axios'
import { useRoute } from 'vue-router'
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import CommentList from '@/components/comments/CommentList.vue'
import NotFound from '@/components/NotFound.vue'
import FavoriteDropdownItem from '@/components/FavoriteDropdownItem.vue'
import ReportDropdownItemModal from '@/components/ReportDropdownItemModal.vue'

const route = useRoute()
const userStore = useUserStore()

const albumDataLoading = ref(true)
const albumData = ref({
  author: {
    name: '',
    avatar: null,
    profile_url: null
  },
  image: null,
  title: '',
  description: '',
  tags: [],
  created_at: null,
  view_count: 0,
  like_count: 0,
  liked: null,
  rating: 0,
  favorite: null
})

const photoListLoading = ref(true)
const photoList = ref([])
const nextURL = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

const upViewCountTimeout = ref(null)
const errorStatus = ref(null)

const getPhotoList = async () => {
  try {
    const response = await axios.get('/portfolio/photo/list/', {
      params: {
        album: route.params.uuid
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

const upAlbumViewCount = async () => {
  try {
    const response = await axios.post(
      '/portfolio/album/up-view-count/'
        + route.params.uuid
        + '/'
    )
    albumData.value.view_count += 1
  } catch (error) {
    console.error(error)
  }
}

const getAlbumData = async () => {
  albumDataLoading.value = true
  try {
    const response = await axios.get(
      '/portfolio/album/retrieve/'
        + route.params.uuid
        + '/'
    )
    albumData.value = response.data
    getPhotoList()
    upViewCountTimeout.value = setTimeout(upAlbumViewCount, 3000)
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    albumDataLoading.value = false
  }
}

const likeAlbum = async () => {
  try {
    const response = await axios.post(
      '/portfolio/album/like/'
        + route.params.uuid
        + '/'
    )
    albumData.value.like_count += 1
    albumData.value.liked = true
  } catch (error) {
    console.error(error)
  }
}

const dislikeAlbum = async () => {
  try {
    const response = await axios.delete(
      '/portfolio/album/like/'
        + route.params.uuid
        + '/'
    )
    albumData.value.like_count -= 1
    albumData.value.liked = false
  } catch (error) {
    console.error(error)
  }
}

watch(
  () => route.params.uuid,
  (newValue) => {
    if (route.name === 'AlbumDetail') {
      getAlbumData()
    }
  }
)

onMounted(() => {
  getAlbumData()
})

onUnmounted(() => {
  clearTimeout(upViewCountTimeout.value)
})
</script>

<template>
  <div class="album-detail-view">
    <LoadingIndicator
      v-if="albumDataLoading"
      class="my-5"
    />
    <NotFound v-else-if="errorStatus === 404" />
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
                  <ul class="list-inline text-body-secondary mb-2">
                    <li class="list-inline-item">
                      <i class="fa-regular fa-calendar-days"></i>
                      {{ $t('portfolio.created') }}
                      {{ getLocaleDateString(albumData.created_at) }}
                    </li>
                    <li class="list-inline-item ms-3">
                      <i class="fa-regular fa-eye"></i>
                      {{ albumData.view_count }}
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
              <div
                v-if="userStore.isLoggedIn"
                class="d-flex justify-content-center justify-content-lg-end"
              >
                <button
                  v-if="albumData.liked"
                  @click="dislikeAlbum()"
                  type="button"
                  class="btn btn-brand"
                >
                  <i class="fa-regular fa-heart"></i>
                  {{ albumData.like_count }}
                </button>
                <button
                  v-else
                  @click="likeAlbum()"
                  type="button"
                  class="btn btn-outline-brand"
                >
                  <i class="fa-regular fa-heart"></i>
                  {{ albumData.like_count }}
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
                          :objFavorite="albumData.favorite"
                          contentType="album"
                          :objectUUID="$route.params.uuid"
                          @updateFavorite="(status) => {
                            albumData.favorite = status
                          }"
                        />
                      </li>
                      <li>
                        <ReportDropdownItemModal
                          contentType="album"
                          :objectUUID="$route.params.uuid"
                        />
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="d-flex align-items-center mb-3">
            <router-link
              :to="{
                name: 'OrganizerDetail',
                params: { profile_url: albumData.author.profile_url }
              }"
            >
              <UserAvatar
                :src="albumData.author.avatar"
                :width="32"
                :height="32"
              />
            </router-link>
            <router-link
              :to="{
                name: 'OrganizerDetail',
                params: { profile_url: albumData.author.profile_url  }
              }"
              class="text-decoration-none link-dark ms-2"
            >
              {{ albumData.author.name }}
            </router-link>
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
                v-for="tag in albumData.tags"
                :key="tag.uuid"
                class="col"
              >
                <router-link
                  :to="{
                    name: 'TagDetail',
                    params: { uuid: tag.uuid },
                    query: { tab: 'albums' }
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

      <div class="row g-3 mt-3">
        <div class="col-xl-7">
          <div
            v-if="photoList.length > 0"
            class="row g-3"
          >
            <div
              v-for="photoItem in photoList"
              :key="photoItem.uuid"
              class="col-12 col-md-6 col-lg-4 col-xl-4"
            >
              <div class="card border border-0 h-100">
                <router-link
                  :to="{
                    name: 'PhotoDetail',
                    params: { uuid: photoItem.uuid },
                    query: {
                      from: 'album',
                      album: $route.params.uuid
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
        <div class="col-xl-5">
          <CommentList
            contentType="album"
            :objectUUID="$route.params.uuid"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useUserStore } from '@/stores/user.js'
import CommentList from '@/components/comments/CommentList.vue'
import NotFound from '@/components/NotFound.vue'

const route = useRoute()
const userStore = useUserStore()

const albumDataLoading = ref(true)
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
  view_count: 0,
  like_count: 0,
  liked: null,
  favorite: null,
  rating: 0
})

const photoListLoading = ref(true)
const photoList = ref([])
const nextURL = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

const errorStatus = ref(null)

const getPhotoList = async () => {
  try {
    const response = await axios.get(
      '/portfolio/photo/list/'
        + '?album='
        + albumData.value.uuid
    )
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
    const response = await axios.post('/portfolio/album/up-view-count/', {
      'uuid': albumData.value.uuid
    })
    albumData.value.view_count += 1
  } catch (error) {
    console.error(error)
  }
}

const getAlbumData = async () => {
  try {
    const response = await axios.get(
      '/portfolio/album/retrieve/'
        + route.params.uuid
        + '/'
    )
    albumData.value = response.data
    getPhotoList()
    setTimeout(upAlbumViewCount, 3000)
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    albumDataLoading.value = false
  }
}

const likeAlbum = async () => {
  try {
    const response = await axios.post('/portfolio/album/like/', {
      'uuid': albumData.value.uuid
    })
    albumData.value.like_count += 1
    albumData.value.liked = true
  } catch (error) {
    console.error(error)
  }
}

const dislikeAlbum = async () => {
  try {
    const response = await axios.delete('/portfolio/album/like/', {
      data: {
        'uuid': albumData.value.uuid
      }
    })
    albumData.value.like_count -= 1
    albumData.value.liked = false
  } catch (error) {
    console.error(error)
  }
}

const addAlbumToFavorites = async () => {
  try {
    const response = await axios.post('/social/favorite/', {
      'content_type': 'album',
      'object_uuid': albumData.value.uuid
    })
    albumData.value.favorite = true
  } catch (error) {
    console.error(error)
  }
}

const removeAlbumFromFavorites = async () => {
  try {
    const response = await axios.delete('/social/favorite/', {
      data: {
        'content_type': 'album',
        'object_uuid': albumData.value.uuid
      }
    })
    albumData.value.favorite = false
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  getAlbumData()
})
</script>

<template>
  <div class="album-detail-view">
    <LoadingIndicator
      v-if="albumDataLoading"
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
                <button
                  v-if="albumData.favorite"
                  @click="removeAlbumFromFavorites()"
                  type="button"
                  class="btn btn-light ms-2"
                >
                  <i class="fa-solid fa-bookmark"></i>
                  {{ $t('favorites.remove_from_favourites') }}
                </button>
                <button
                  v-else
                  @click="addAlbumToFavorites()"
                  type="button"
                  class="btn btn-light ms-2"
                >
                  <i class="fa-regular fa-bookmark"></i>
                  {{ $t('favorites.add_to_favourites') }}
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
                </LocaleRouterLink>
              </div>
            </div>
          </div>
          <div
            v-else-if="!photoListLoading"
            class="lead d-flex justify-content-center py-3"
          >
            {{ $t('portfolio.no_photos') }}
          </div>
          <div v-if="nextURL" v-intersection="getMorePhotoList"></div>
          <LoadingIndicator v-if="photoListLoading" />
        </div>
        <div class="col-xl-5">
          <CommentList
            contentType="album"
            :objectUUID="albumData.uuid"
          />
        </div>
      </div>
    </div>
  </div>
</template>

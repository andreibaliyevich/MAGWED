<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const photosLoading = ref(true)
const photosMoreLoading = ref(false)
const photoList = ref([])
const nextURL = ref(null)

const getPhotos = async () => {
  let photoListURL = '/portfolio/photos/list/'
  if (route.query.tab == 'popular') {
    photoListURL += '?ordering=-rating'
  } else if (route.query.tab == 'fresh') {
    photoListURL += '?ordering=-uploaded_at'
  } else if (route.query.tab == 'editors') {
    photoListURL += '?editors_choice=true'
  } else {
    photoListURL += '?ordering=rating'
  }

  try {
    const response = await axios.get(photoListURL)
    photoList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    photosLoading.value = false
  }
}

const getMorePhotos = async () => {
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

watch(
  () => route.query.tab,
  (newValue) => {
    if (route.name == 'PhotoList') {
      getPhotos()
    }
  }
)

onMounted(() => {
  getPhotos()
})
</script>

<template>
  <div class="photo-list-view">
    <div class="container my-5">
      <h1 class="display-6 text-center mb-5">
        {{ $t('portfolio.photos') }}
      </h1>

      <ul class="nav nav-pills justify-content-center mb-3">
        <li
          :class="[
            'nav-item',
            this.$route.query.tab == 'popular' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="PhotoList"
            :routeQuery="{ tab: 'popular' }"
            :class="[
              'nav-link',
              this.$route.query.tab == 'popular' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.popular_photos') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            this.$route.query.tab == 'fresh' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="PhotoList"
            :routeQuery="{ tab: 'fresh' }"
            :class="[
              'nav-link',
              this.$route.query.tab == 'fresh' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.fresh_photos') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            this.$route.query.tab == 'editors' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="PhotoList"
            :routeQuery="{ tab: 'editors' }"
            :class="[
              'nav-link',
              this.$route.query.tab == 'editors' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.editors_choice') }}
          </LocaleRouterLink>
        </li>
      </ul>

      <LoadingIndicator v-if="photosLoading" />
      <div
        v-else-if="photoList.length > 0"
        class="row g-3"
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
              :routeQuery="{ from: this.$route.query.tab }"
              class="link-light"
            >
              <img
                :src="photoItem.thumbnail"
                class="card-img"
              >
              <div class="card-img-overlay">
                <div class="position-absolute top-0 start-0 ms-2 mt-2">
                  <div class="d-flex align-items-center">
                    <LocaleRouterLink
                      routeName="OrganizerDetail"
                      :routeParams="{ profile_url: photoItem.owner.profile_url }"
                    >
                      <UserAvatar
                        :src="photoItem.owner.avatar"
                        :width="32"
                        :height="32"
                      />
                    </LocaleRouterLink>
                    <LocaleRouterLink
                      routeName="OrganizerDetail"
                      :routeParams="{ profile_url: photoItem.owner.profile_url  }"
                      class="text-decoration-none link-light ms-2"
                    >
                      {{ photoItem.owner.name }}
                    </LocaleRouterLink>
                  </div>
                </div>
                <div class="position-absolute top-50 start-50 translate-middle">
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
        <div v-if="nextURL" v-intersection="getMorePhotos"></div>
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

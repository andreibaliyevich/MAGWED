<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const photoListLoading = ref(true)
const photoList = ref([])
const nextURL = ref(null)

const getPhotoList = async () => {
  photoListLoading.value = true
  photoList.value = []

  let params = new URLSearchParams()
  if (route.query.tab == 'popular') {
    params.append('ordering', '-rating')
  } else if (route.query.tab == 'fresh') {
    params.append('ordering', '-uploaded_at')
  } else if (route.query.tab == 'editors') {
    params.append('editors_choice', true)
  } else {
    params.append('ordering', 'rating')
  }

  try {
    const response = await axios.get('/portfolio/photo/list/', {
      params: params
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

watch(
  () => route.query.tab,
  (newValue) => {
    if (route.name == 'PhotoList') {
      getPhotoList()
    }
  }
)

onMounted(() => {
  getPhotoList()
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
            $route.query.tab == 'popular' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="PhotoList"
            :routeQuery="{ tab: 'popular' }"
            :class="[
              'nav-link',
              $route.query.tab == 'popular' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.popular_photos') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            $route.query.tab == 'fresh' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="PhotoList"
            :routeQuery="{ tab: 'fresh' }"
            :class="[
              'nav-link',
              $route.query.tab == 'fresh' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.fresh_photos') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            $route.query.tab == 'editors' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="PhotoList"
            :routeQuery="{ tab: 'editors' }"
            :class="[
              'nav-link',
              $route.query.tab == 'editors' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.editors_choice') }}
          </LocaleRouterLink>
        </li>
      </ul>

      <div
        v-if="photoList.length > 0"
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
              :routeQuery="{ from: $route.query.tab }"
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
                      :routeParams="{ profile_url: photoItem.author.profile_url }"
                    >
                      <UserAvatar
                        :src="photoItem.author.avatar"
                        :width="32"
                        :height="32"
                      />
                    </LocaleRouterLink>
                    <LocaleRouterLink
                      routeName="OrganizerDetail"
                      :routeParams="{ profile_url: photoItem.author.profile_url  }"
                      class="text-decoration-none link-light ms-2"
                    >
                      {{ photoItem.author.name }}
                    </LocaleRouterLink>
                  </div>
                </div>
                <div class="position-absolute top-50 start-50 translate-middle">
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
  </div>
</template>

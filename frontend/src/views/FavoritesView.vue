<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const favoritesLoading = ref(true)
const favoritesMoreLoading = ref(false)
const favoriteList = ref([])
const favoriteCount = ref(0)
const nextURL = ref(null)

const getFavorites = async () => {
  try {
    const response = await axios.get('/social/favorite/list/')
    favoriteList.value = response.data.results
    favoriteCount.value = response.data.count
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    favoritesLoading.value = false
  }
}

const getMoreFavorites = async () => {
  favoritesMoreLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    favoriteList.value = [...favoriteList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    favoritesMoreLoading.value = false
  }
}

onMounted(() => {
  getFavorites()
})
</script>

<template>
  <div class="favorites-view">
    <div class="container my-5">
      <h1 class="display-6 text-center mb-5">
        {{ $t('favorites.favorites') }} ({{ favoriteCount }})
      </h1>
      <LoadingIndicator v-if="favoritesLoading" />
      <div
        v-else-if="favoriteList.length > 0"
        class="row g-3"
      >
        <div
          v-for="favorite in favoriteList"
          :key="favorite.uuid"
          class="col-12 col-md-6 col-lg-4 col-xl-3"
        >
          <div
            v-if="favorite.content_type_model == 'article'"
            class="card border border-light shadow-sm h-100"
          >
            <LocaleRouterLink
              routeName="Blog"
              :routeParams="{ slug: favorite.content_object.slug }"
            >
              <img
                :src="favorite.content_object.thumbnail"
                :alt="favorite.content_object.translated_title"
                class="card-img-top"
              >
            </LocaleRouterLink>
            <div class="card-body">
              <LocaleRouterLink
                routeName="Blog"
                :routeParams="{ slug: favorite.content_object.slug }"
                class="text-decoration-none link-dark text-center"
              >
                <h5 class="card-title">
                  <i class="fa-regular fa-newspaper"></i>
                  {{ favorite.content_object.translated_title }}
                </h5>
              </LocaleRouterLink>
            </div>
          </div>
          <div
            v-else-if="favorite.content_type_model == 'album'"
            class="card border border-light shadow-sm h-100"
          >
            <LocaleRouterLink
              routeName="AlbumDetail"
              :routeParams="{ uuid: favorite.content_object.uuid }"
            >
              <img
                :src="favorite.content_object.thumbnail"
                :alt="favorite.content_object.title"
                class="card-img-top"
              >
            </LocaleRouterLink>
            <div class="card-body">
              <LocaleRouterLink
                routeName="AlbumDetail"
                :routeParams="{ uuid: favorite.content_object.uuid }"
                class="text-decoration-none link-dark text-center"
              >
                <h5 class="card-title">
                  <i class="fa-regular fa-images"></i>
                  {{ favorite.content_object.title }}
                </h5>
              </LocaleRouterLink>
            </div>
          </div>
          <div
            v-else-if="favorite.content_type_model == 'photo'"
            class="card border border-light shadow-sm h-100"
          >
            <LocaleRouterLink
              routeName="PhotoDetail"
              :routeParams="{ uuid: favorite.content_object.uuid }"
            >
              <img
                :src="favorite.content_object.thumbnail"
                :alt="favorite.content_object.title"
                class="card-img-top"
              >
            </LocaleRouterLink>
            <div class="card-body">
              <LocaleRouterLink
                routeName="PhotoDetail"
                :routeParams="{ uuid: favorite.content_object.uuid }"
                class="text-decoration-none link-dark text-center"
              >
                <h5 class="card-title">
                  <i class="fa-regular fa-image"></i>
                  {{ favorite.content_object.title }}
                </h5>
              </LocaleRouterLink>
            </div>
          </div>
        </div>
        <div v-if="nextURL" v-intersection="getMoreFavorites"></div>
        <LoadingIndicator v-if="favoritesMoreLoading" />
      </div>
      <div
        v-else
        class="lead fs-3 d-flex justify-content-center py-3"
      >
        {{ $t('favorites.no_favorites') }}
      </div>
    </div>
  </div>
</template>

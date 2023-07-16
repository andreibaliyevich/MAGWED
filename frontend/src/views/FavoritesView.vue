<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const favoriteListLoading = ref(false)
const favoriteList = ref([])
const favoriteCount = ref(0)
const nextURL = ref(null)

const getFavoriteList = async () => {
  favoriteListLoading.value = true

  let params = new URLSearchParams()
  if (route.query.type) {
    params.append('content_type__model', route.query.type)
  }

  try {
    const response = await axios.get('/social/favorite/list/', {
      params: params
    })
    favoriteList.value = response.data.results
    favoriteCount.value = response.data.count
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    favoriteListLoading.value = false
  }
}

const getMoreFavoriteList = async () => {
  favoriteListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    favoriteList.value = [...favoriteList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    favoriteListLoading.value = false
  }
}

watch(
  () => route.query.type,
  (newValue) => {
    if (route.name == 'Favorites') {
      getFavoriteList()
    }
  }
)

onMounted(() => {
  getFavoriteList()
})
</script>

<template>
  <div class="favorites-view">
    <div class="container my-5">
      <h1 class="display-6 text-center mb-5">
        {{ $t('favorites.favorites') }} ({{ favoriteCount }})
      </h1>

      <ul class="nav nav-pills justify-content-center mb-3">
        <li
          :class="[
            'nav-item',
            !this.$route.query.type ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="Favorites"
            :class="[
              'nav-link',
              !this.$route.query.type ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('favorites.all') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            this.$route.query.type == 'article' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="Favorites"
            :routeQuery="{ type: 'article' }"
            :class="[
              'nav-link',
              this.$route.query.type == 'article' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('favorites.articles') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            this.$route.query.type == 'album' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="Favorites"
            :routeQuery="{ type: 'album' }"
            :class="[
              'nav-link',
              this.$route.query.type == 'album' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('favorites.albums') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            this.$route.query.type == 'photo' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="Favorites"
            :routeQuery="{ type: 'photo' }"
            :class="[
              'nav-link',
              this.$route.query.type == 'photo' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('favorites.photos') }}
          </LocaleRouterLink>
        </li>
      </ul>

      <div
        v-if="favoriteList.length > 0"
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
      </div>
      <div
        v-else-if="!favoriteListLoading"
        class="lead fs-3 d-flex justify-content-center py-3"
      >
        {{ $t('favorites.no_favorites') }}
      </div>
      <div v-if="nextURL" v-intersection="getMoreFavoriteList"></div>
      <LoadingIndicator v-if="favoriteListLoading" />
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const albumsLoading = ref(true)
const albumsMoreLoading = ref(false)
const albumList = ref([])
const nextURL = ref(null)

const getAlbums = async () => {
  let albumListURL = '/portfolio/albums/list/'
  if (route.query.tab == 'popular') {
    albumListURL += '?ordering=-rating'
  } else if (route.query.tab == 'fresh') {
    albumListURL += '?ordering=-created_at'
  } else if (route.query.tab == 'editors') {
    albumListURL += '?editors_choice=true'
  } else {
    albumListURL += '?ordering=rating'
  }

  try {
    const response = await axios.get(albumListURL)
    albumList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    albumsLoading.value = false
  }
}

const getMoreAlbums = async () => {
  albumsMoreLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    albumList.value = [...albumList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    albumsMoreLoading.value = false
  }
}

watch(
  () => route.query.tab,
  (newValue) => {
    if (route.name == 'AlbumList') {
      getAlbums()
    }
  }
)

onMounted(() => {
  getAlbums()
})
</script>

<template>
  <div class="album-list-view">
    <div class="container my-5">
      <h1 class="display-6 text-center mb-5">
        {{ $t('portfolio.photo_albums') }}
      </h1>

      <ul class="nav nav-pills justify-content-center mb-3">
        <li
          :class="[
            'nav-item',
            this.$route.query.tab == 'popular' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="AlbumList"
            :routeQuery="{ tab: 'popular' }"
            :class="[
              'nav-link',
              this.$route.query.tab == 'popular' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.popular_albums') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            this.$route.query.tab == 'fresh' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="AlbumList"
            :routeQuery="{ tab: 'fresh' }"
            :class="[
              'nav-link',
              this.$route.query.tab == 'fresh' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.fresh_albums') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            this.$route.query.tab == 'editors' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="AlbumList"
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

      <LoadingIndicator v-if="albumsLoading" />
      <div
        v-else-if="albumList.length > 0"
        class="row g-3"
      >
        <div
          v-for="albumItem in albumList"
          :key="albumItem.uuid"
          class="col-12 col-sm-6 col-md-4 col-lg-3"
        >
          <div class="card border border-light shadow-sm h-100">
            <LocaleRouterLink
              routeName="AlbumDetail"
              :routeParams="{ uuid: albumItem.uuid }"
            >
              <img
                :src="albumItem.thumbnail"
                :alt="albumItem.title"
                class="card-img-top"
              >
            </LocaleRouterLink>
            <div class="card-body">
              <LocaleRouterLink
                routeName="AlbumDetail"
                :routeParams="{ uuid: albumItem.uuid }"
                class="text-decoration-none link-dark"
              >
                <h5 class="card-title">{{ albumItem.title }}</h5>
              </LocaleRouterLink>
              <div class="d-flex align-items-center">
                <LocaleRouterLink
                  routeName="OrganizerDetail"
                  :routeParams="{ profile_url: albumItem.owner.profile_url }"
                >
                  <UserAvatar
                    :src="albumItem.owner.avatar"
                    :width="32"
                    :height="32"
                  />
                </LocaleRouterLink>
                <LocaleRouterLink
                  routeName="OrganizerDetail"
                  :routeParams="{ profile_url: albumItem.owner.profile_url  }"
                  class="text-decoration-none link-dark ms-2"
                >
                  {{ albumItem.owner.name }}
                </LocaleRouterLink>
              </div>
              <div class="d-flex justify-content-between mt-1">
                <div>
                  <i class="fa-regular fa-eye"></i>
                  {{ albumItem.num_views }}
                </div>
                <div>
                  <i class="fa-regular fa-heart"></i>
                  {{ albumItem.likes_count }}
                </div>
                <div>
                  <i class="fa-regular fa-star"></i>
                  {{ albumItem.rating }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="nextURL" v-intersection="getMoreAlbums"></div>
        <LoadingIndicator v-if="albumsMoreLoading" />
      </div>
      <div
        v-else
        class="lead d-flex justify-content-center py-3"
      >
        {{ $t('portfolio.no_albums') }}
      </div>
    </div>
  </div>
</template>

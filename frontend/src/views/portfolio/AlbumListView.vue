<script setup>
import axios from 'axios'
import { useRoute } from 'vue-router'
import { ref, watch, onMounted } from 'vue'

const route = useRoute()

const albumListLoading = ref(true)
const albumList = ref([])
const nextURL = ref(null)

const getAlbumList = async () => {
  albumListLoading.value = true
  albumList.value = []

  let params = new URLSearchParams()
  if (route.query.tab === 'popular') {
    params.append('ordering', '-rating')
  } else if (route.query.tab === 'fresh') {
    params.append('ordering', '-created_at')
  } else if (route.query.tab === 'editors') {
    params.append('editors_choice', true)
  } else {
    params.append('ordering', 'rating')
  }

  try {
    const response = await axios.get('/portfolio/album/list/', {
      params: params
    })
    albumList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    albumListLoading.value = false
  }
}

const getMoreAlbumList = async () => {
  albumListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    albumList.value = [...albumList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    albumListLoading.value = false
  }
}

watch(
  () => route.query.tab,
  (newValue) => {
    if (route.name === 'AlbumList') {
      getAlbumList()
    }
  }
)

onMounted(() => {
  getAlbumList()
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
            $route.query.tab === 'popular'
              || $route.query.tab === undefined
              ? 'active'
              : null
          ]"
        >
          <router-link
            :to="{ query: { tab: 'popular' } }"
            :class="[
              'nav-link',
              $route.query.tab === 'popular'
                || $route.query.tab === undefined
                ? 'active'
                : 'text-dark'
            ]"
          >
            {{ $t('portfolio.popular_albums') }}
          </router-link>
        </li>
        <li
          :class="[
            'nav-item',
            $route.query.tab === 'fresh' ? 'active' : null
          ]"
        >
          <router-link
            :to="{ query: { tab: 'fresh' } }"
            :class="[
              'nav-link',
              $route.query.tab === 'fresh' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.fresh_albums') }}
          </router-link>
        </li>
        <li
          :class="[
            'nav-item',
            $route.query.tab === 'editors' ? 'active' : null
          ]"
        >
          <router-link
            :to="{ query: { tab: 'editors' } }"
            :class="[
              'nav-link',
              $route.query.tab === 'editors' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.editors_choice') }}
          </router-link>
        </li>
      </ul>

      <div
        v-if="albumList.length > 0"
        class="row g-3"
      >
        <div
          v-for="albumItem in albumList"
          :key="albumItem.uuid"
          class="col-12 col-md-6 col-lg-4 col-xl-3"
        >
          <div class="card border border-light shadow-sm h-100">
            <router-link
              :to="{
                name: 'AlbumDetail',
                params: { uuid: albumItem.uuid }
              }"
            >
              <img
                :src="albumItem.thumbnail"
                :alt="albumItem.title"
                class="card-img-top"
              >
            </router-link>
            <div class="card-body">
              <router-link
                :to="{
                  name: 'AlbumDetail',
                  params: { uuid: albumItem.uuid }
                }"
                class="text-decoration-none link-dark"
              >
                <h5 class="card-title">{{ albumItem.title }}</h5>
              </router-link>
              <div class="d-flex align-items-center">
                <router-link
                  :to="{
                    name: 'OrganizerDetail',
                    params: { profile_url: albumItem.author.profile_url }
                  }"
                >
                  <UserAvatar
                    :src="albumItem.author.avatar"
                    :width="32"
                    :height="32"
                  />
                </router-link>
                <router-link
                  :to="{
                    name: 'OrganizerDetail',
                    params: { profile_url: albumItem.author.profile_url }
                  }"
                  class="text-decoration-none link-dark ms-2"
                >
                  {{ albumItem.author.name }}
                </router-link>
              </div>
              <div class="d-flex justify-content-between mt-1">
                <div>
                  <i class="fa-regular fa-eye"></i>
                  {{ albumItem.view_count }}
                </div>
                <div>
                  <i class="fa-regular fa-heart"></i>
                  {{ albumItem.like_count }}
                </div>
                <div>
                  <i class="fa-regular fa-star"></i>
                  {{ albumItem.rating }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-else-if="!albumListLoading"
        class="lead d-flex justify-content-center py-3"
      >
        {{ $t('portfolio.no_albums') }}
      </div>
      <div
        v-if="nextURL"
        style="min-height: 1px; margin-bottom: 1px;"
        v-intersection="{
          'scrollArea': null,
          'callbackFunction': getMoreAlbumList,
          'functionArguments': []
        }"
      ></div>
      <LoadingIndicator v-if="albumListLoading" />
    </div>
  </div>
</template>

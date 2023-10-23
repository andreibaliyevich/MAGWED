<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const props = defineProps({
  tagUUID: {
    type: String,
    required: true
  }
})

const albumListLoading = ref(true)
const albumList = ref([])
const nextURL = ref(null)

const getAlbumList = async () => {
  try {
    const response = await axios.get('/portfolio/album/list/', {
      params: {
        tags: props.tagUUID
      }
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

onMounted(() => {
  getAlbumList()
})
</script>

<template>
  <div class="album-list">
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
                :routeParams="{ profile_url: albumItem.author.profile_url }"
              >
                <UserAvatar
                  :src="albumItem.author.avatar"
                  :width="32"
                  :height="32"
                />
              </LocaleRouterLink>
              <LocaleRouterLink
                routeName="OrganizerDetail"
                :routeParams="{ profile_url: albumItem.author.profile_url  }"
                class="text-decoration-none link-dark ms-2"
              >
                {{ albumItem.author.name }}
              </LocaleRouterLink>
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
</template>

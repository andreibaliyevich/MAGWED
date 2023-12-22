<script setup>
import axios from 'axios'
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import AlbumList from '@/components/tag/AlbumList.vue'
import ArticleList from '@/components/tag/ArticleList.vue'
import PhotoList from '@/components/tag/PhotoList.vue'
import NotFound from '@/components/NotFound.vue'

const route = useRoute()

const tagLoading = ref(true)
const tagData = ref({
  uuid: '',
  name: ''
})

const errorStatus = ref(null)

const getTagData = async () => {
  tagLoading.value = true
  try {
    const response = await axios.get(
      '/main/tag/'
        + route.params.uuid
        + '/'
    )
    tagData.value = response.data
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    tagLoading.value = false
  }
}

onMounted(() => {
  getTagData()
})
</script>

<template>
  <div class="tag-detail-view">
    <LoadingIndicator
      v-if="tagLoading"
      class="my-5"
    />
    <NotFound v-else-if="errorStatus == 404" />
    <div
      v-else
      class="container my-5"
    >
      <h1 class="display-6 text-center mb-5">
        #{{ tagData.name }}
      </h1>

      <ul class="nav nav-pills justify-content-center mb-3">
        <li
          :class="[
            'nav-item',
            $route.query.tab == 'photos' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="TagDetail"
            :routeParams="{ uuid: $route.params.uuid }"
            :routeQuery="{ tab: 'photos' }"
            :class="[
              'nav-link',
              $route.query.tab == 'photos' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.photos') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            $route.query.tab == 'albums' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="TagDetail"
            :routeParams="{ uuid: $route.params.uuid }"
            :routeQuery="{ tab: 'albums' }"
            :class="[
              'nav-link',
              $route.query.tab == 'albums' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('portfolio.photo_albums') }}
          </LocaleRouterLink>
        </li>
        <li
          :class="[
            'nav-item',
            $route.query.tab == 'articles' ? 'active' : null
          ]"
        >
          <LocaleRouterLink
            routeName="TagDetail"
            :routeParams="{ uuid: $route.params.uuid }"
            :routeQuery="{ tab: 'articles' }"
            :class="[
              'nav-link',
              $route.query.tab == 'articles' ? 'active' : 'text-dark'
            ]"
          >
            {{ $t('blog.articles') }}
          </LocaleRouterLink>
        </li>
      </ul>

      <div v-if="$route.query.tab == 'photos'">
        <PhotoList :tagUUID="$route.params.uuid" />
      </div>
      <div v-else-if="$route.query.tab == 'albums'">
        <AlbumList :tagUUID="$route.params.uuid" />
      </div>
      <div v-else-if="$route.query.tab == 'articles'">
        <ArticleList :tagUUID="$route.params.uuid" />
      </div>

    </div>
  </div>
</template>

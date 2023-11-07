<script setup>
import axios from 'axios'
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useUserStore } from '@/stores/user.js'
import CommentList from '@/components/comments/CommentList.vue'
import NotFound from '@/components/NotFound.vue'
import ReportDropdownItemModal from '@/components/ReportDropdownItemModal.vue'

const route = useRoute()
const { locale } = useI18n({ useScope: 'global' })
const userStore = useUserStore()

const articleLoading = ref(true)
const articleData = ref({
  uuid: '',
  author: {
    uuid: '',
    name: ''
  },
  categories: [],
  translated_title: '',
  image: null,
  translated_content: '',
  tags: [],
  published_at: null,
  view_count: 0,
  favorite: null
})

const { getLocaleDateString } = useLocaleDateTime()

const upViewCountTimeout = ref(null)
const errorStatus = ref(null)

const upArticleViewCount = async () => {
  try {
    const response = await axios.post(
      '/blog/article/up-view-count/'
        + route.params.slug
        + '/'
    )
    articleData.value.view_count += 1
  } catch (error) {
    console.error(error)
  }
}

const getArticleData = async () => {
  articleLoading.value = true
  try {
    const response = await axios.get(
      '/blog/article/retrieve/'
        + route.params.slug
        + '/'
    )
    articleData.value = response.data
    upViewCountTimeout.value = setTimeout(upArticleViewCount, 3000)
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    articleLoading.value = false
  }
}

const addArticleToFavorites = async () => {
  try {
    const response = await axios.post('/social/favorite/', {
      content_type: 'article',
      object_uuid: articleData.value.uuid
    })
    articleData.value.favorite = true
  } catch (error) {
    console.error(error)
  }
}

const removeArticleFromFavorites = async () => {
  try {
    const response = await axios.delete('/social/favorite/', {
      data: {
        content_type: 'article',
        object_uuid: articleData.value.uuid
      }
    })
    articleData.value.favorite = false
  } catch (error) {
    console.error(error)
  }
}

watch(locale, () => {
  getArticleData()
})

watch(
  () => route.params.slug,
  (newValue) => {
    if (route.name == 'ArticleDetail') {
      getArticleData()
    }
  }
)

onMounted(() => {
  getArticleData()
})

onUnmounted(() => {
  clearTimeout(upViewCountTimeout.value)
})
</script>

<template>
  <div class="article-detail-view">
    <LoadingIndicator v-if="articleLoading" />
    <NotFound v-else-if="errorStatus == 404" />
    <div v-else>
      <div class="d-flex justify-content-center mb-3">
        <img
          :src="articleData.image"
          class="card-img-top rounded-3"
        >
      </div>
      <h1 class="h3">{{ articleData.translated_title }}</h1>
      <div class="d-lg-flex align-items-lg-center text-center">
        <div class="row g-1">
          <div
            v-for="categoryValue in articleData.categories"
            :key="categoryValue"
            class="col"
          >
            <span class="badge text-bg-light">
              {{ $t(`category_choices.${categoryValue}`) }}
            </span>
          </div>
        </div>
        <div
          v-if="userStore.isLoggedIn"
          class="ms-lg-auto mt-2"
        >
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
                  <button
                    v-if="articleData.favorite"
                    @click="removeArticleFromFavorites()"
                    type="button"
                    class="dropdown-item btn btn-link"
                  >
                    <i class="fa-solid fa-star"></i>
                    {{ $t('favorites.remove_from_favourites') }}
                  </button>
                  <button
                    v-else
                    @click="addArticleToFavorites()"
                    type="button"
                    class="dropdown-item btn btn-link"
                  >
                    <i class="fa-regular fa-star"></i>
                    {{ $t('favorites.add_to_favourites') }}
                  </button>
                </li>
                <li>
                  <ReportDropdownItemModal
                    contentType="article"
                    :objectUUID="articleData.uuid"
                  />
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <ul class="list-inline text-body-secondary mt-2 mb-4">
        <li class="list-inline-item">
          {{ $t('blog.author') }}:
          <LocaleRouterLink
            routeName="ArticleList"
            :routeQuery="{ author: articleData.author.uuid }"
            class="text-decoration-none link-dark"
          >
            {{ articleData.author.name }}
          </LocaleRouterLink>
        </li>
        <li class="list-inline-item ms-3">
          <i class="fa-regular fa-calendar-days"></i>
          {{ getLocaleDateString(articleData.published_at) }}
        </li>
        <li class="list-inline-item ms-3">
          <i class="fa-regular fa-eye"></i>
          {{ articleData.view_count }}
        </li>
      </ul>
      <div v-html="articleData.translated_content"></div>
      <div
        v-if="articleData.tags.length > 0"
        class="d-inline-block my-3"
      >
        <div class="row g-1">
          <div
            v-for="tag in articleData.tags"
            :key="tag.uuid"
            class="col"
          >
            <LocaleRouterLink
              routeName="TagDetail"
              :routeParams="{ uuid: tag.uuid }"
              :routeQuery="{ tab: 'articles' }"
              class="btn btn-light btn-sm"
            >
              #{{ tag.name }}
            </LocaleRouterLink>
          </div>
        </div>
      </div>
      <CommentList
        contentType="article"
        :objectUUID="articleData.uuid"
      />
    </div>
  </div>
</template>

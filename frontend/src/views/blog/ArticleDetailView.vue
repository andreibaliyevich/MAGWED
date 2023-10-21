<script setup>
import axios from 'axios'
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import CommentList from '@/components/comments/CommentList.vue'
import NotFound from '@/components/NotFound.vue'

const route = useRoute()
const { locale } = useI18n({ useScope: 'global' })

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
  view_count: 0
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
      <div class="mb-1">
        <span
          v-for="category in articleData.categories"
          :key="category"
          class="badge text-bg-light ms-1"
        >
          {{ $t(`category_choices.${category}`) }}
        </span>
      </div>
      <ul class="list-inline text-body-secondary mt-2 mb-3">
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
            v-for="tagValue in articleData.tags"
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
      <CommentList
        contentType="article"
        :objectUUID="articleData.uuid"
      />
    </div>
  </div>
</template>

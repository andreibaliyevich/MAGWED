<script setup>
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ref, watch, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const route = useRoute()
const { locale } = useI18n({ useScope: 'global' })

const articleListLoading = ref(true)
const articleList = ref([])
const nextURL = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

const getArticleList = async () => {
  articleListLoading.value = true
  articleList.value = []

  let params = new URLSearchParams()
  if (route.query.author) {
    params.append('author', route.query.author)
  }
  if (route.query.category) {
    params.append('categories', route.query.category)
  }
  if (route.query.year) {
    params.append('published_at_year', route.query.year)
  }

  try {
    const response = await axios.get('/blog/article/list/', {
      params: params
    })
    articleList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    articleListLoading.value = false
  }
}

const getMoreArticleList = async () => {
  articleListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    articleList.value = [...articleList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    articleListLoading.value = false
  }
}

watch(locale, () => {
  getArticleList()
})

watch(
  () => route.query,
  (newValue) => {
    if (route.name == 'ArticleList') {
      getArticleList()
    }
  }
)

onMounted(() => {
  getArticleList()
})
</script>

<template>
  <div class="article-list-view">
    <h1 class="display-6 text-center mb-5">
      {{ $t('blog.articles') }}
    </h1>
    <div v-if="articleList.length > 0">
      <div
        v-for="article in articleList"
        :key="article.slug"
        class="card border border-light shadow-sm mb-3"
      >
        <div class="row g-0">
          <div class="col-md-4 d-flex align-items-center">
            <router-link
              :to="{
                name: 'ArticleDetail',
                params: { slug: article.slug }
              }"
            >
              <img
                :src="article.thumbnail"
                class="img-fluid rounded"
                :alt="article.translated_title"
              >
            </router-link>
          </div>
          <div class="col-md-8">
            <div class="card-body">
              <router-link
                :to="{
                  name: 'ArticleDetail',
                  params: { slug: article.slug }
                }"
                class="text-decoration-none link-dark"
              >
                <h5 class="card-title">{{ article.translated_title }}</h5>
              </router-link>
              <div class="mb-1">
                <span
                  v-for="category in article.categories"
                  :key="category"
                  class="badge text-bg-light ms-1"
                >
                  {{ $t(`category_choices.${category}`) }}
                </span>
              </div>
              <p class="card-text">{{ article.translated_description }}</p>
              <p class="card-text">
                <small class="text-body-secondary">
                  <i class="fa-regular fa-calendar-days"></i>
                  {{ getLocaleDateString(article.published_at) }}
                </small>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      v-else-if="!articleListLoading"
      class="lead fs-3 d-flex justify-content-center py-3"
    >
      {{ $t('blog.no_articles') }}
    </div>
    <div
      v-if="nextURL"
      style="min-height: 1px; margin-bottom: 1px;"
      v-intersection="{
        'scrollArea': null,
        'callbackFunction': getMoreArticleList,
        'functionArguments': []
      }"
    ></div>
    <LoadingIndicator v-if="articleListLoading" />
  </div>
</template>

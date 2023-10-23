<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const props = defineProps({
  tagUUID: {
    type: String,
    required: true
  }
})

const articleListLoading = ref(true)
const articleList = ref([])
const nextURL = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

const getArticleList = async () => {
  try {
    const response = await axios.get(
      '/blog/article/list/'
        + '?tags='
        + props.tagUUID
    )
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

onMounted(() => {
  getArticleList()
})
</script>

<template>
  <div class="article-list">
    <div
      v-if="articleList.length > 0"
      class="px-md-5 mx-md-5"
    >
      <div
        v-for="article in articleList"
        class="card border border-light shadow-sm mb-3"
      >
        <div class="row g-0">
          <div class="col-md-4 d-flex align-items-center">
            <LocaleRouterLink
              routeName="ArticleDetail"
              :routeParams="{ slug: article.slug }"
            >
              <img
                :src="article.thumbnail"
                class="img-fluid rounded"
                :alt="article.translated_title"
              >
            </LocaleRouterLink>
          </div>
          <div class="col-md-8">
            <div class="card-body">
              <LocaleRouterLink
                routeName="ArticleDetail"
                :routeParams="{ slug: article.slug }"
                class="text-decoration-none link-dark"
              >
                <h5 class="card-title">{{ article.translated_title }}</h5>
              </LocaleRouterLink>
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
      class="lead d-flex justify-content-center py-3"
    >
      {{ $t('portfolio.no_photos') }}
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

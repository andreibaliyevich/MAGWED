<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n({ useScope: 'global' })

const articlesLoading = ref(false)
const responseData = ref(false)

const getArticles = async () => {
  articlesLoading.value = true
  try {
    const response = await axios.get('/blog/articles/')
    responseData.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    articlesLoading.value = false
  }
}

watch(locale, () => {
  getArticles()
})

onMounted(() => {
  getArticles()
})
</script>

<template>
  <div class="article-list-view">
    <h3>{{ $t('blog.blog') }}</h3>
    <div v-if="responseData.count > 0" class="article-list">
      <div v-for="article in responseData.results">
        <div><strong>Slug:</strong> {{ article.slug }}</div>
        <div><strong>Title:</strong> {{ article.get_translated_title }}</div>
        <div><strong>Published at:</strong> {{ article.published_at }}</div>
      </div>
    </div>
    <h2 v-else style="color: red;">List is empty!</h2>
  </div>
</template>

<style>
.article-list-view {
  width: 500px;
  margin: 0 auto;
}
</style>

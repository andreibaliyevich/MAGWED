<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      responseData: {}
    }
  },
  methods: {
    async getOrganizerList() {
      try {
        const response = await axios.get('/' + this.$i18n.locale + '/blog/articles/')
        this.responseData = response.data
      } catch (error) {
        console.error(error)
      }
    }
  },
  watch: {
    '$i18n.locale'(newValue) {
      this.getOrganizerList()
    }
  },
  mounted() {
    this.getOrganizerList()
  }
}
</script>

<template>
  <div class="blog">
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
.blog {
  width: 500px;
  margin: 0 auto;
}
</style>

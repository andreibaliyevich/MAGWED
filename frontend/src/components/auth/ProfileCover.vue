<script setup>
import axios from 'axios'

import { useMainStore } from '@/stores/main.js'
const mainStore = useMainStore()
</script>

<script>
export default {
  data() {
    return {
      cover: null,
      isCoverLoading: false,
      status: null,
      errors: null
    }
  },
  methods: {
    openCoverInput() {
      this.$refs.coverInput.click()
    },
    getCover() {
      axios.get('/' + this.$i18n.locale + '/accounts/auth/cover/')
      .then((response) => {
        this.cover = response.data.cover
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
    },
    updateCover(event) {
      this.isCoverLoading = true
      const coverData = new FormData()
      coverData.append('cover', event.target.files[0], event.target.files[0].name)

      axios.put('/' + this.$i18n.locale + '/accounts/auth/cover/', coverData)
      .then((response) => {
        this.cover = response.data.cover
        this.$refs.coverInput.value = ''
        this.status = 'updated_cover'
        this.errors = null
        document.body.scrollTop = 0
        document.documentElement.scrollTop = 0
      })
      .catch((error) => {
        this.$refs.coverInput.value = ''
        this.status = null
        this.errors = error.response.data
      })
      .then(() => this.isCoverLoading = false)
    },
    removeCover(event) {
      if (confirm(this.$t('auth.profile.you_want_remove_cover'))) {
        axios.delete('/' + this.$i18n.locale + '/accounts/auth/cover/')
        .then((response) => {
          this.cover = null
          this.status = 'removed_cover'
          this.errors = null
        })
        .catch((error) => {
          this.status = null
          this.errors = error.response.data
        })
      }
    }
  },
  mounted() {
    this.getCover()
  }
}
</script>

<template>
  <div class="card mb-2">
    <div
      v-if="isCoverLoading"
      class="d-flex justify-content-center p-5"
    >
      <div
        class="spinner-border text-dark"
        role="status"
      >
        <span class="visually-hidden">
          Loading...
        </span>
      </div>
    </div>
    <div v-else>
      <img
        v-if="cover"
        :src="`${ mainStore.apiURL }${ cover }`"
        class="card-img-top"
      >
      <img
        v-else
        src="/cover.jpg"
        class="card-img-top"
      >
    </div>
    <div class="card-body text-center">
      <div v-if="status">
        <small
          v-if="status == 'updated_cover'"
          class="text-success"
        >
          {{ $t('auth.profile.cover_updated_successfully') }}
        </small>
        <small
          v-if="status == 'removed_cover'"
          class="text-success"
        >
          {{ $t('auth.profile.cover_removed_successfully') }}
        </small>
      </div>
      <div v-if="errors && errors.cover">
        <small
          v-for="error in errors.cover"
          class="text-danger"
        >
          {{ error }}
        </small>
      </div>
      <div class="d-flex justify-content-center">
        <input
          ref="coverInput"
          @change="updateCover"
          type="file"
          accept="image/*"
          class="visually-hidden"
        >
        <button
          @click="openCoverInput"
          type="button"
          class="btn btn-light-brand m-1"
        >
          {{ $t('auth.profile.upload_cover') }}
        </button>
        <button
          v-if="cover"
          @click="removeCover"
          type="button"
          class="btn btn-outline-dark m-1"
        >
          {{ $t('auth.profile.remove_cover') }}
        </button>
      </div>
      <small class="text-muted">
        {{ $t('form_help.input_img', { width: '1900', height: '1200' }) }}
      </small>
    </div>
  </div>
</template>

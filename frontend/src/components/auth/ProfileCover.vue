<script setup>
import axios from 'axios'

import { API_URL } from '@/config.js'
</script>

<script>
export default {
  data() {
    return {
      cover: null,
      coverLoading: false,
      status: null,
      errors: null
    }
  },
  methods: {
    getCover() {
      axios.get('/accounts/auth/cover/')
      .then((response) => {
        this.cover = response.data.cover
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
    },
    updateCover(filelist) {
      this.coverLoading = true
      const coverData = new FormData()
      coverData.append('cover', filelist[0], filelist[0].name)

      axios.put('/accounts/auth/cover/', coverData)
      .then((response) => {
        this.cover = response.data.cover
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
      .then(() => this.coverLoading = false)
    },
    removeCover() {
      if (confirm(this.$t('auth.profile.you_want_remove_cover'))) {
        axios.delete('/accounts/auth/cover/')
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
  <div class="profile-cover">
    <div class="card mb-2">
      <ActionProcessingIndicator
        v-if="coverLoading"
        :actionInfo="$t('auth.profile.uploading_cover')"
      />
      <div v-else>
        <img
          v-if="cover"
          :src="`${ API_URL }${ cover }`"
          class="card-img-top"
        >
        <img
          v-else
          src="/cover.jpg"
          class="card-img-top"
        >
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
            <FileInputButton
              @updateFile="updateCover"
              accept="image/*"
              buttonClass="btn btn-light-brand m-1"
            >
              {{ $t('auth.profile.upload_cover') }}
            </FileInputButton>
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
            {{ $t('form_help.input_img', { width: '1500', height: '500' }) }}
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

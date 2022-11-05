<script setup>
import axios from 'axios'

import { useMainStore } from '@/stores/main.js'
import { useUserStore } from '@/stores/user.js'
const mainStore = useMainStore()
const userStore = useUserStore()
</script>

<script>
export default {
  data() {
    return {
      avatarLoading: false,
      status: null,
      errors: null
    }
  },
  methods: {
    updateAvatar(filelist) {
      this.avatarLoading = true
      const avatarData = new FormData()
      avatarData.append('avatar', filelist[0], filelist[0].name)

      axios.put('/' + this.$i18n.locale + '/accounts/auth/avatar/', avatarData)
      .then((response) => {
        this.userStore.updateAvatar(response.data.avatar)
        window.localStorage.setItem('user', JSON.stringify({
          'token': this.userStore.token,
          'username': this.userStore.username,
          'email': this.userStore.email,
          'user_type': this.userStore.userType,
          'name': this.userStore.name,
          'avatar': response.data.avatar
        }))
        this.status = 'updated_avatar'
        this.errors = null
        document.body.scrollTop = 0
        document.documentElement.scrollTop = 0
      })
      .catch((error) => {
        this.$refs.avatarInput.value = ''
        this.status = null
        this.errors = error.response.data
      })
      .then(() => this.avatarLoading = false)
    },
    removeAvatar() {
      if (confirm(this.$t('auth.profile.you_want_remove_avatar'))) {
        axios.delete('/' + this.$i18n.locale + '/accounts/auth/avatar/')
        .then((response) => {
          this.userStore.updateAvatar(null)
          window.localStorage.setItem('user', JSON.stringify({
            'token': this.userStore.token,
            'username': this.userStore.username,
            'email': this.userStore.email,
            'user_type': this.userStore.userType,
            'name': this.userStore.name,
            'avatar': null
          }))
          this.status = 'removed_avatar'
          this.errors = null
        })
        .catch((error) => {
          this.status = null
          this.errors = error.response.data
        })
      }
    }
  }
}
</script>

<template>
  <div class="card mb-2">
    <ActionProcessingIndicator
      v-if="avatarLoading"
      :actionInfo="$t('auth.profile.uploading_avatar')"
    />
    <div
      v-else
      class="row d-flex align-items-center"
    >
      <div class="col-md-3">
        <img
          v-if="userStore.avatar"
          :src="`${ mainStore.apiURL }${ userStore.avatar }`"
          class="img-fluid rounded-start"
        >
        <img
          v-else
          src="/user-avatar.jpg"
          class="img-fluid rounded-start"
        >
      </div>
      <div class="col-md-9">
        <div class="card-body text-center">
          <div v-if="status">
            <small
              v-if="status == 'updated_avatar'"
              class="text-success"
            >
              {{ $t('auth.profile.avatar_updated_successfully') }}
            </small>
            <small
              v-if="status == 'removed_avatar'"
              class="text-success"
            >
              {{ $t('auth.profile.avatar_removed_successfully') }}
            </small>
          </div>
          <div v-if="errors && errors.avatar">
            <small
              v-for="error in errors.avatar"
              class="text-danger"
            >
              {{ error }}
            </small>
          </div>
          <div class="d-flex justify-content-center">
            <FileInputButton
              @updateFile="updateAvatar"
              accept="image/*"
            >
              {{ $t('auth.profile.upload_avatar') }}
            </FileInputButton>
            <button
              v-if="userStore.avatar"
              @click="removeAvatar"
              type="button"
              class="btn btn-outline-dark m-1"
            >
              {{ $t('auth.profile.remove_avatar') }}
            </button>
          </div>
          <small class="text-muted">
            {{ $t('form_help.input_img', { width: '512', height: '512' }) }}
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

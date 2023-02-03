<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUserStore } from '@/stores/user.js'

const { t } = useI18n({ useScope: 'global' })
const userStore = useUserStore()

const avatarLoading = ref(false)

const status = ref(null)
const errors = ref(null)

const updateAvatar = async (filelist) => {
  avatarLoading.value = true

  const avatarData = new FormData()
  avatarData.append('avatar', filelist[0], filelist[0].name)

  try {
    const response = await axios.put('/accounts/auth/avatar/', avatarData)
    userStore.updateAvatar(response.data.avatar)
    window.localStorage.setItem('user', JSON.stringify({
      'id': userStore.id,
      'username': userStore.username,
      'email': userStore.email,
      'user_type': userStore.userType,
      'name': userStore.name,
      'avatar': response.data.avatar,
      'token': userStore.token
    }))
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    avatarLoading.value = false
  }
}

const removeAvatar = async () => {
  if (confirm(t('auth.profile.you_want_remove_avatar'))) {
    avatarLoading.value = true
    try {
      const response = await axios.delete('/accounts/auth/avatar/')
      userStore.updateAvatar(null)
      window.localStorage.setItem('user', JSON.stringify({
        'username': userStore.username,
        'email': userStore.email,
        'user_type': userStore.userType,
        'name': userStore.name,
        'avatar': null,
        'token': userStore.token
      }))
      status.value = response.status
      errors.value = null
    } catch (error) {
      status.value = null
      errors.value = error.response.data
    } finally {
      avatarLoading.value = false
    }
  }
}
</script>

<template>
  <div class="profile-avatar">
    <div class="card mb-2">
      <LoadingIndicator
        v-if="avatarLoading"
        :actionInfo="$t('auth.profile.uploading_avatar')"
      />
      <div
        v-else
        class="row d-flex align-items-center"
      >
        <div class="col-md-3">
          <UserAvatar
            :src="userStore.avatar"
            :width="128"
            :height="128"
            imgClass="img-fluid rounded-start"
          />
        </div>
        <div class="col-md-9">
          <div class="card-body text-center">
            <small
              v-if="status == 200"
              class="text-success"
            >
              {{ $t('auth.profile.avatar_updated_successfully') }}
            </small>
            <small
              v-else-if="status == 204"
              class="text-success"
            >
              {{ $t('auth.profile.avatar_removed_successfully') }}
            </small>
            <small
              v-if="errors && errors.avatar"
              v-for="error in errors.avatar"
              class="text-danger"
            >
              {{ error }}
            </small>
            <div class="d-flex justify-content-center">
              <FileInputButton
                @updateFile="updateAvatar"
                buttonClass="btn btn-light-brand m-1"
                accept="image/*"
              >
                {{ $t('auth.profile.upload_avatar') }}
              </FileInputButton>
              <button
                v-if="userStore.avatar"
                @click="removeAvatar()"
                class="btn btn-outline-dark m-1"
                type="button"
              >
                {{ $t('auth.profile.remove_avatar') }}
              </button>
            </div>
            <small class="text-muted">
              {{ $t('form_help.input_img', { width: '500', height: '500' }) }}
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

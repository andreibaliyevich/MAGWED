<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n({ useScope: 'global' })

const coverLoading = ref(true)
const cover = ref(null)

const status = ref(null)
const errors = ref(null)

const getCover = async () => {
  try {
    const response = await axios.get('/accounts/auth/cover/')
    cover.value = response.data.cover
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    coverLoading.value = false
  }
}

const updateCover = async (filelist) => {
  coverLoading.value = true

  const coverData = new FormData()
  coverData.append('cover', filelist[0], filelist[0].name)

  try {
    const response = await axios.put('/accounts/auth/cover/', coverData)
    cover.value = response.data.cover
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    coverLoading.value = false
  }
}

const removeCover = async () => {
  coverLoading.value = true

  if (confirm(t('auth.profile.you_want_remove_cover'))) {
    try {
      const response = await axios.delete('/accounts/auth/cover/')
      cover.value = null
      status.value = response.status
      errors.value = null
    } catch (error) {
      status.value = null
      errors.value = error.response.data
    } finally {
      coverLoading.value = false
    }
  }
}

onMounted(() => {
  getCover()
})
</script>

<template>
  <div class="profile-cover">
    <div class="card mb-2">
      <LoadingIndicator
        v-if="coverLoading"
        :actionInfo="$t('auth.profile.uploading_cover')"
      />
      <div v-else>
        <img
          v-if="cover"
          :src="cover"
          class="card-img-top"
        >
        <img
          v-else
          src="/cover.jpg"
          class="card-img-top"
        >
        <div class="card-body text-center">
          <small
            v-if="status == 200"
            class="text-success"
          >
            {{ $t('auth.profile.cover_updated_successfully') }}
          </small>
          <small
            v-else-if="status == 204"
            class="text-success"
          >
            {{ $t('auth.profile.cover_removed_successfully') }}
          </small>
          <small
            v-if="errors && errors.cover"
            v-for="error in errors.cover"
            class="text-danger"
          >
            {{ error }}
          </small>
          <div class="d-flex justify-content-center">
            <FileInputButton
              @updateFile="updateCover"
              buttonClass="btn btn-light-brand m-1"
              accept="image/*"
            >
              {{ $t('auth.profile.upload_cover') }}
            </FileInputButton>
            <button
              v-if="cover"
              @click="removeCover()"
              class="btn btn-outline-dark m-1"
              type="button"
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

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

  let formData = new FormData()
  formData.append('cover', filelist[0], filelist[0].name)

  try {
    const response = await axios.put('/accounts/auth/cover/', formData)
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

onMounted(() => {
  getCover()
})
</script>

<template>
  <div class="profile-cover">
    <div class="card mb-2">
      <LoadingIndicator
        v-if="coverLoading"
        :actionInfo="$t('user.uploading_cover')"
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
            {{ $t('user.cover_updated_successfully') }}
          </small>
          <small
            v-else-if="status == 204"
            class="text-success"
          >
            {{ $t('user.cover_removed_successfully') }}
          </small>
          <div
            v-if="errors?.cover"
            class="text-danger"
          >
            <small v-for="error in errors.cover">
              {{ error }}
            </small>
          </div>
          <div class="d-flex justify-content-center">
            <FileInputButton
              @selectedFiles="updateCover"
              buttonClass="btn btn-soft-brand m-1"
              accept="image/*"
            >
              {{ $t('user.upload_cover') }}
            </FileInputButton>
            <button
              v-if="cover"
              class="btn btn-outline-dark m-1"
              type="button"
              data-bs-toggle="modal"
              data-bs-target="#remove_cover_modal_choice"
            >
              {{ $t('user.remove_cover') }}
            </button>
          </div>
          <small class="text-muted">
            {{ $t('form_help.input_img', { width: '1500', height: '500' }) }}
          </small>
        </div>
      </div>
    </div>
    <Teleport to="body">
      <div
        id="remove_cover_modal_choice"
        class="modal fade"
        role="dialog"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div
          class="modal-dialog modal-dialog-centered"
          role="document"
        >
          <div class="modal-content rounded-3 shadow">
            <div class="modal-body p-4 text-center">
              <h5 class="mb-0">{{ $t('user.you_want_remove_cover') }}</h5>
              <p class="mb-0">{{ $t('user.cover_will_be_set_default') }}</p>
            </div>
            <div class="modal-footer flex-nowrap p-0">
              <button
                @click="removeCover()"
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0 border-end"
                type="button"
                data-bs-dismiss="modal"
              >
                <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
              </button>
              <button
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0"
                type="button"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.no_cancel') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

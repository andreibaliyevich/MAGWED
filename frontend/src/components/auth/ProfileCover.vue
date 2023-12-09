<script setup>
import axios from 'axios'
import 'cropperjs/dist/cropper.css'
import Cropper from 'cropperjs'
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n({ useScope: 'global' })

const coverLoading = ref(true)
const cover = ref(null)

const coverCropperModal = ref(null)
const coverCropperModalBootstrap = ref(null)

const coverImg = ref(null)
const coverCropper = ref(null)
const coverCropperReady = ref(false)

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

const loadCoverImg = async (filelist) => {
  const reader = new FileReader()
  reader.readAsDataURL(filelist[0])
  reader.onload = () => {
    coverImg.value.src = reader.result
    coverImg.value.alt = filelist[0].name
    coverCropperModalBootstrap.value.show()
  }
}

const updateCover = async (filelist) => {
  coverLoading.value = true

  const croppedCanvas = coverCropper.value.getCroppedCanvas({
    width: 1500,
    height: 500
  })
  const canvasBlob = await new Promise((resolve) => {
    croppedCanvas.toBlob((blob) => {
      resolve(blob)
    })
  })

  let formData = new FormData()
  formData.append('cover', canvasBlob, coverImg.value.alt)

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
    coverCropperModalBootstrap.value.hide()
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
  coverImg.value.addEventListener('ready', () => {
    coverCropperReady.value = true
  })
  coverCropperModal.value.addEventListener('shown.bs.modal', () => {
    coverCropper.value = new Cropper(coverImg.value, {
      viewMode: 1,
      dragMode: 'crop',
      aspectRatio: 3 / 1,
      zoomable: false
    })
  })
  coverCropperModal.value.addEventListener('hidden.bs.modal', () => {
    coverCropper.value.destroy()
    coverCropper.value = null
    coverImg.value.src = ''
    coverImg.value.alt = ''
    coverCropperReady.value = false
  })
  coverCropperModalBootstrap.value = new bootstrap.Modal(
    coverCropperModal.value
  )
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
              @selectedFiles="loadCoverImg"
              buttonClass="btn btn-soft-brand m-1"
              accept="image/*"
            >
              {{ $t('user.update_cover') }}
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
        ref="coverCropperModal"
        id="cover_cropper_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="cover_cropper_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="cover_cropper_modal_label"
                class="modal-title"
              >
                {{ $t('user.updating_cover') }}
              </h5>
              <button
                class="btn-close"
                type="button"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form
                @submit.prevent="updateCover()"
                id="cover_modal_form"
              >
                <div class="d-flex justify-content-center">
                  <img
                    ref="coverImg"
                    src=""
                    alt=""
                    class="d-block mw-100 max-vh-75"
                  >
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button
                class="btn btn-light"
                type="button"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.cancel') }}
              </button>
              <SubmitButton
                :loadingStatus="coverLoading"
                buttonClass="btn btn-brand"
                form="cover_modal_form"
                :disabled="!coverCropperReady"
              >
                {{ $t('btn.update') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>

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

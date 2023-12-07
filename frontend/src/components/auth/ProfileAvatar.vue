<script setup>
import axios from 'axios'
import 'cropperjs/dist/cropper.css'
import Cropper from 'cropperjs'
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUserStore } from '@/stores/user.js'

const { t } = useI18n({ useScope: 'global' })
const userStore = useUserStore()

const avatarLoading = ref(false)

const avatarCropperModal = ref(null)
const avatarCropperModalBootstrap = ref(null)

const avatarImg = ref(null)
const avatarCropper = ref(null)

const status = ref(null)
const errors = ref(null)

const loadAvatarImg = async (filelist) => {
  const reader = new FileReader()
  reader.readAsDataURL(filelist[0])
  reader.onload = () => {
    avatarImg.value.src = reader.result
    avatarImg.value.alt = filelist[0].name
    avatarCropperModalBootstrap.value.show()
  }
}

const updateAvatar = async () => {
  avatarLoading.value = true

  const croppedCanvas = avatarCropper.value.getCroppedCanvas({
    width: 500,
    height: 500
  })
  const canvasBlob = await new Promise((resolve) => {
    croppedCanvas.toBlob((blob) => {
      resolve(blob)
    })
  })

  let formData = new FormData()
  formData.append('avatar', canvasBlob, avatarImg.value.alt)

  try {
    const response = await axios.put('/accounts/auth/avatar/', formData)
    userStore.updateAvatar(response.data.avatar)
    window.localStorage.setItem('user', JSON.stringify({
      uuid: userStore.uuid,
      username: userStore.username,
      email: userStore.email,
      user_type: userStore.userType,
      name: userStore.name,
      avatar: response.data.avatar,
      token: userStore.token
    }))
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    avatarLoading.value = false
    avatarCropperModalBootstrap.value.hide()
  }
}

const removeAvatar = async () => {
  avatarLoading.value = true
  try {
    const response = await axios.delete('/accounts/auth/avatar/')
    userStore.updateAvatar(null)
    window.localStorage.setItem('user', JSON.stringify({
      uuid: userStore.uuid,
      username: userStore.username,
      email: userStore.email,
      user_type: userStore.userType,
      name: userStore.name,
      avatar: null,
      token: userStore.token
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

onMounted(() => {
  avatarCropperModal.value.addEventListener('shown.bs.modal', () => {
    avatarCropper.value = new Cropper(avatarImg.value, {
      viewMode: 1,
      dragMode: 'crop',
      aspectRatio: 1 / 1,
      zoomable: false
    })
  })
  avatarCropperModal.value.addEventListener('hidden.bs.modal', () => {
    avatarCropper.value.destroy()
    avatarCropper.value = null
    avatarImg.value.src = ''
    avatarImg.value.alt = ''
  })
  avatarCropperModalBootstrap.value = new bootstrap.Modal(
    avatarCropperModal.value
  )
})
</script>

<template>
  <div class="profile-avatar">
    <div class="card mb-2">
      <div class="row d-flex align-items-center">
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
              {{ $t('user.avatar_updated_successfully') }}
            </small>
            <small
              v-else-if="status == 204"
              class="text-success"
            >
              {{ $t('user.avatar_removed_successfully') }}
            </small>
            <div
              v-if="errors?.avatar"
              class="text-danger"
            >
              <small v-for="error in errors.avatar">
                {{ error }}
              </small>
            </div>
            <div class="d-flex justify-content-center">
              <FileInputButton
                @selectedFiles="loadAvatarImg"
                buttonClass="btn btn-soft-brand m-1"
                accept="image/*"
              >
                {{ $t('user.update_avatar') }}
              </FileInputButton>
              <button
                v-if="userStore.avatar"
                class="btn btn-outline-dark m-1"
                type="button"
                data-bs-toggle="modal"
                data-bs-target="#remove_avatar_modal_choice"
              >
                {{ $t('user.remove_avatar') }}
              </button>
            </div>
            <small class="text-muted">
              {{ $t('form_help.input_img', { width: '500', height: '500' }) }}
            </small>
          </div>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <div
        ref="avatarCropperModal"
        id="avatar_cropper_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="avatar_cropper_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="avatar_cropper_modal_label"
                class="modal-title"
              >
                {{ $t('user.updating_avatar') }}
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
                @submit.prevent="updateAvatar()"
                id="avatar_modal_form"
              >
                <div class="d-flex justify-content-center">
                  <img
                    ref="avatarImg"
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
                :loadingStatus="avatarLoading"
                buttonClass="btn btn-brand"
                form="avatar_modal_form"
              >
                {{ $t('btn.update') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>

      <div
        id="remove_avatar_modal_choice"
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
              <h5 class="mb-0">{{ $t('user.you_want_remove_avatar') }}</h5>
              <p class="mb-0">{{ $t('user.avatar_will_be_set_default') }}</p>
            </div>
            <div class="modal-footer flex-nowrap p-0">
              <button
                @click="removeAvatar()"
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

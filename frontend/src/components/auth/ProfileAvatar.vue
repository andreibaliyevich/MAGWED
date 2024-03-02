<script setup>
import axios from 'axios'
import 'cropperjs/dist/cropper.css'
import Cropper from 'cropperjs'
import { ref, watch } from 'vue'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()

const avatarProcessing = ref(false)
const avatarReady = ref(false)
const avatarUpdateDialog = ref(false)
const avatarRemoveDialog = ref(false)
const avatarImg = ref(null)
const avatarCropper = ref(null)

const status = ref(null)
const errors = ref(null)

const loadAvatarImg = async (filelist) => {
  avatarUpdateDialog.value = true
  const reader = new FileReader()
  reader.readAsDataURL(filelist[0])
  reader.onload = () => {
    avatarImg.value.src = reader.result
    avatarImg.value.alt = filelist[0].name
    avatarReady.value = true
  }
}

const updateAvatar = async () => {
  avatarProcessing.value = true

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
    avatarProcessing.value = false
    avatarUpdateDialog.value = false
  }
}

const removeAvatar = async () => {
  avatarProcessing.value = true
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
    avatarProcessing.value = false
    avatarRemoveDialog.value = false
  }
}

watch(avatarReady, (newValue) => {
  if (newValue) {
    avatarCropper.value = new Cropper(avatarImg.value, {
      viewMode: 1,
      dragMode: 'crop',
      aspectRatio: 1 / 1,
      zoomable: false
    })
  }
})

watch(avatarUpdateDialog, (newValue) => {
  if (!newValue && avatarReady) {
    avatarCropper.value.destroy()
    avatarCropper.value = null
    avatarImg.value.src = ''
    avatarImg.value.alt = ''
    avatarReady.value = false
  }
})
</script>

<template>
  <v-card class="my-3">
    <v-row class="d-flex align-center">
      <v-col
        :cols="12"
        :sm="3"
      >
        <v-img
          :src="userStore.avatar ? userStore.avatar : '/user-avatar.png'"
          aspect-ratio="1/1"
        ></v-img>
      </v-col>

      <v-col
        :cols="12"
        :sm="9"
      >
        <div class="text-center">
          <small
            v-if="status === 200"
            class="text-success"
          >
            {{ $t('user.avatar_updated_successfully') }}
          </small>
          <small
            v-else-if="status === 204"
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

          <div class="d-flex justify-space-evenly py-1">
            <FileInputButton
              @selectedFiles="loadAvatarImg"
              accept="image/*"
              variant="flat"
              color="primary"
              class="text-none"
            >
              {{ $t('user.update_avatar') }}
            </FileInputButton>
            <v-btn
              @click="avatarRemoveDialog = true"
              :disabled="!userStore.avatar"
              variant="outlined"
              class="text-none"
            >
              {{ $t('user.remove_avatar') }}
            </v-btn>
          </div>

          <small class="text-grey-darken-1">
            {{ $t('form_help.input_img', { width: '500', height: '500' }) }}
          </small>
        </div>
      </v-col>
    </v-row>

    <v-dialog
      v-model="avatarUpdateDialog"
      width="auto"
      persistent
    >
      <v-card>
        <div class="d-flex justify-center align-center">
          <v-icon
            v-if="!avatarReady"
            icon="mdi-account-circle"
            role="img"
            color="secondary"
            :size="150"
          ></v-icon>
          <img
            ref="avatarImg"
            src=""
            alt=""
            class="mw-100 max-vh-75"
          >
        </div>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            @click="avatarUpdateDialog = false"
            class="text-none"
          >
            {{ $t('btn.cancel') }}
          </v-btn>
          <v-btn
            @click="updateAvatar()"
            :loading="avatarProcessing"
            :disabled="!avatarReady"
            variant="flat"
            color="primary"
            class="text-none"
          >
            {{ $t('btn.update') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="avatarRemoveDialog"
      width="auto"
      persistent
    >
      <v-card>
        <v-card-title>
          {{ $t('user.you_want_remove_avatar') }}
        </v-card-title>
        <v-card-text>
          {{ $t('user.avatar_will_be_set_default') }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="avatarRemoveDialog = false">
            {{ $t('btn.no_cancel') }}
          </v-btn>
          <v-btn
            @click="removeAvatar()"
            :loading="avatarProcessing"
          >
            <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n({ useScope: 'global' })

const passwordUpdating = ref(false)
const currentPassword = ref('')
const newPassword = ref('')
const newPassword2 = ref('')

const status = ref(null)
const errors = ref(null)

const changePassword = async () => {
  passwordUpdating.value = true
  try {
    const response = await axios.post('/accounts/auth/password/change/', {
      current_password: currentPassword.value,
      new_password: newPassword.value,
      new_password2: newPassword2.value
    })
    if (response.status === 204) {
      currentPassword.value = ''
      newPassword.value = ''
      newPassword2.value = ''
      status.value = t('auth.passwordchange.success')
      errors.value = null
    }
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    passwordUpdating.value = false
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0
  }
}
</script>

<template>
  <div class="password-change-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">
        {{ $t('auth.passwordchange.password_change') }}
      </h1>

      <div v-if="status">
        <div
          class="alert alert-success d-flex align-items-center alert-dismissible fade show"
          role="alert"
        >
          <i class="fa-solid fa-circle-check"></i>
          <div class="ms-3">{{ status }}</div>
          <button
            @click="status = null"
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
          ></button>
        </div>
      </div>

      <form @submit.prevent="changePassword()">
        <div class="mb-3">
          <BaseInput
            v-if="errors && errors.current_password"
            v-model="currentPassword"
            :label="$t('auth.passwordchange.current_password')"
            :errors="errors.current_password"
            id="id_current_password"
            name="current_password"
            type="password"
          />
          <BaseInput
            v-else
            v-model="currentPassword"
            :label="$t('auth.passwordchange.current_password')"
            id="id_current_password"
            name="current_password"
            type="password"
          />
        </div>
        <div class="mb-3">
          <BaseInput
            v-if="errors && errors.new_password"
            v-model="newPassword"
            :label="$t('auth.password.new_password')"
            :errors="errors.new_password"
            id="id_new_password"
            name="new_password"
            type="password"
          />
          <BaseInput
            v-else
            v-model="newPassword"
            :label="$t('auth.password.new_password')"
            id="id_new_password"
            name="new_password"
            type="password"
          />
        </div>
        <ul class="fs-6">
          <li>{{ $t('auth.password.advice1') }}</li>
          <li>{{ $t('auth.password.advice2') }}</li>
          <li>{{ $t('auth.password.advice3') }}</li>
          <li>{{ $t('auth.password.advice4') }}</li>
        </ul>
        <div class="mb-3">
          <BaseInput
            v-if="errors && errors.new_password2"
            v-model="newPassword2"
            :label="$t('auth.password.new_password2')"
            :errors="errors.new_password2"
            id="id_new_password2"
            name="new_password2"
            type="password"
          />
          <BaseInput
            v-else
            v-model="newPassword2"
            :label="$t('auth.password.new_password2')"
            id="id_new_password2"
            name="new_password2"
            type="password"
          />
        </div>
        <SubmitButton
          :loadingStatus="passwordUpdating"
          buttonClass="btn btn-brand btn-lg"
        >
          {{ $t('auth.password.change_password') }}
        </SubmitButton>
      </form>
    </div>
  </div>
</template>

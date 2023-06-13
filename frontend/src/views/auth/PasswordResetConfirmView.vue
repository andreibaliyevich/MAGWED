<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const loadingStatus = ref(false)
const newPassword = ref('')
const newPassword2 = ref('')

const status = ref(null)
const errors = ref(null)

const confirmPasswordReset = async () => {
  loadingStatus.value = true
  try {
    const response = await axios.post(
      '/accounts/auth/password/reset/confirm/',
      {
        uid: route.params.uid,
        token: route.params.token,
        new_password: newPassword.value,
        new_password2: newPassword2.value
      }
    )
    if (response.status === 204) {
      newPassword.value = ''
      newPassword2.value = ''
      status.value = 204
      errors.value = null
    }
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    loadingStatus.value = false
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0
  }
}
</script>

<template>
  <div class="password-reset-confirm-view">
    <h1 class="display-6 text-center mb-4">
      {{ $t('auth.passwordresetconfirm.password_reset_confirm') }}
    </h1>

    <div v-if="status == 204">
      <p class="lead fs-3 text-muted">
        {{ $t('auth.passwordresetconfirm.success1') }}
      </p>
      <p class="lead fs-5">
        {{ $t('auth.passwordresetconfirm.success2') }}<br>
        {{ $t('auth.passwordresetconfirm.success3') }}
      </p>
      <div class="fs-6 text-center">
        <LocaleRouterLink
          routeName="Login"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.log_in') }}
        </LocaleRouterLink>
      </div>
    </div>

    <div v-else-if="errors && (errors.detail || errors.uid || errors.token)">
      <p class="lead fs-3 text-danger">
        {{ $t('auth.passwordresetconfirm.error') }}
      </p>
      <p
        v-if="errors.detail"
        class="lead fs-5"
      >
        {{ errors.detail }}
      </p>
      <p
        v-if="errors.uid"
        v-for="error in errors.uid"
        class="lead fs-5"
      >
        {{ error }}
      </p>
      <p
        v-if="errors.token"
        v-for="error in errors.token"
        class="lead fs-5"
      >
        {{ error }}
      </p>
      <div class="fs-6 text-center">
        <LocaleRouterLink
          routeName="PasswordReset"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.password.reset_password') }}
        </LocaleRouterLink>
      </div>
    </div>

    <form
      v-else
      @submit.prevent="confirmPasswordReset()"
    >
      <div class="mb-3">
        <BaseInput
          v-model="newPassword"
          type="password"
          id="id_new_password"
          name="new_password"
          :label="$t('auth.password.new_password')"
          :errors="errors?.new_password ? errors.new_password : []"
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
          v-model="newPassword2"
          type="password"
          id="id_new_password2"
          name="new_password2"
          :label="$t('auth.password.new_password2')"
          :errors="errors?.new_password2 ? errors.new_password2 : []"
        />
      </div>
      <SubmitButton
        :loadingStatus="loadingStatus"
        buttonClass="btn btn-brand btn-lg w-100"
      >
        {{ $t('auth.passwordresetconfirm.confirm_password_reset') }}
      </SubmitButton>
    </form>
  </div>
</template>

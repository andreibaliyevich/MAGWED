<script setup>
import axios from 'axios'
import { ref } from 'vue'

const loadingStatus = ref(false)
const email = ref('')

const status = ref(null)
const errors = ref(null)

const resetPassword = async () => {
  loadingStatus.value = true
  try {
    const response = await axios.post('/accounts/auth/password/reset/', {
      email: email.value
    })
    if (response.status === 204) {
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
  <div class="password-reset-view">
    <h1 class="display-6 text-center">
      {{ $t('auth.passwordreset.password_reset') }}
    </h1>

    <div
      v-if="status == 204"
      class="mt-4"
    >
      <p class="lead fs-3 text-muted">
        {{ $t('auth.passwordreset.success1') }}
      </p>
      <p class="lead fs-5">
        {{ $t('auth.passwordreset.success2') }}<br>
        {{ $t('auth.passwordreset.success3') }}
      </p>
    </div>

    <form
      v-else
      @submit.prevent="resetPassword()"
      :class="{ 'mt-4': !loadingStatus }"
    >
      <p class="fs-6">{{ $t('auth.passwordreset.help') }}</p>
      <ul class="fs-6">
        <li>{{ $t('auth.passwordreset.step1') }}</li>
        <li>{{ $t('auth.passwordreset.step2') }}</li>
        <li>{{ $t('auth.passwordreset.step3') }}</li>
      </ul>

      <BaseInput
        v-if="errors && errors.email"
        v-model="email"
        :label="$t('auth.passwordreset.email')"
        :errors="errors.email"
        id="id_email"
        name="email"
        type="email"
        maxlength="254"
      />
      <BaseInput
        v-else
        v-model="email"
        :label="$t('auth.passwordreset.email')"
        id="id_email"
        name="email"
        type="email"
        maxlength="254"
      />

      <SubmitButton
        :loadingStatus="loadingStatus"
        buttonClass="btn btn-brand btn-lg w-100 mt-3"
      >
        {{ $t('auth.password.reset_password') }}
      </SubmitButton>

      <hr class="my-4">
      <div class="fs-6 text-center">
        <LocaleRouterLink
          routeName="Login"
          class="link-primary text-decoration-none"
        >
          <i class="fa-solid fa-angle-left"></i>
          {{ $t('auth.passwordreset.back_to_login') }}
        </LocaleRouterLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      email: '',
      actionProcessing: false,
      status: null,
      errors: null
    }
  },
  methods: {
    resetPassword() {
      this.actionProcessing = true
      axios.post('/accounts/auth/password/reset/', {
        email: this.email
      })
      .then((response) => {
        if (response.status === 204) {
          this.status = '204'
          this.errors = null
        }
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
      .then(() => {
        this.actionProcessing = false
        document.body.scrollTop = 0
        document.documentElement.scrollTop = 0
      })
    }
  }
}
</script>

<template>
  <div class="password-reset-view">
    <h1 class="display-6 text-center">
      {{ $t('auth.passwordreset.password_reset') }}
    </h1>

    <ActionProcessingIndicator v-if="actionProcessing" />

    <div
      v-if="status == '204'"
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
      @submit.prevent="resetPassword"
      :class="{ 'mt-4': !actionProcessing }"
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

      <button
        type="submit"
        class="btn btn-brand btn-lg w-100 mt-3"
      >
        {{ $t('auth.password.reset_password') }}
      </button>

      <hr class="my-4">
      <div class="fs-6 text-center">
        <LocaleRouterLink
          toName="Login"
          class="link-primary text-decoration-none"
        >
          <i class="fa-solid fa-angle-left"></i>
          {{ $t('auth.passwordreset.back_to_login') }}
        </LocaleRouterLink>
      </div>
    </form>
  </div>
</template>

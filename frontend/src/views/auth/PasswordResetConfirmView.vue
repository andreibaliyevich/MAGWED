<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      newPassword: '',
      newPassword2: '',
      status: null,
      errors: null
    }
  },
  methods: {
    confirmPasswordReset() {
      axios.post('/accounts/auth/password/reset/confirm/', {
        uid: this.$route.params.uid,
        token: this.$route.params.token,
        new_password: this.newPassword,
        new_password2: this.newPassword2
      })
      .then((response) => {
        if (response.status === 204) {
          this.newPassword = ''
          this.newPassword2 = ''
          this.status = '204'
          this.errors = null
        }
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
        console.log(this.errors)
      })
      .then(() => {
        document.body.scrollTop = 0
        document.documentElement.scrollTop = 0
      })
    }
  }
}
</script>

<template>
  <div class="password-reset-confirm-view">
    <h1 class="display-6 text-center mb-4">
      {{ $t('auth.passwordresetconfirm.password_reset_confirm') }}
    </h1>

    <div v-if="status == '204'">
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
      @submit.prevent="confirmPasswordReset"
    >
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
      <button
        type="submit"
        class="btn btn-brand btn-lg w-100"
      >
        {{ $t('auth.passwordresetconfirm.confirm_password_reset') }}
      </button>
    </form>
  </div>
</template>

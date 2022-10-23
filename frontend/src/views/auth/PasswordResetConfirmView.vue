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
      axios.post('/' + this.$i18n.locale + '/accounts/auth/password/reset/confirm/', {
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
          toName="Login"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.signin') }}
        </LocaleRouterLink>
      </div>
    </div>

    <div v-else-if="errors">
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
          toName="PasswordReset"
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
      <div
        v-if="errors && errors.new_password"
        class="form-floating mb-3"
      >
        <input
          v-model="newPassword"
          id="id_new_password"
          name="new_password"
          type="password"
          required=""
          :placeholder="$t('auth.password.new_password')"
          class="form-control is-invalid"

        >
        <label for="id_new_password">
          {{ $t('auth.password.new_password') }}
        </label>
        <div
          v-for="error in errors.new_password"
          class="invalid-feedback"
        >
          {{ error }}
        </div>
      </div>
      <div
        v-else
        class="form-floating mb-3"
      >
        <input
          v-model="newPassword"
          id="id_new_password"
          name="new_password"
          type="password"
          required=""
          :placeholder="$t('auth.password.new_password')"
          class="form-control"
        >
        <label for="id_new_password">
          {{ $t('auth.password.new_password') }}
        </label>
      </div>

      <ul class="fs-6">
        <li>{{ $t('auth.password.advice1') }}</li>
        <li>{{ $t('auth.password.advice2') }}</li>
        <li>{{ $t('auth.password.advice3') }}</li>
        <li>{{ $t('auth.password.advice4') }}</li>
      </ul>

      <div
        v-if="errors && errors.new_password2"
        class="form-floating mb-3"
      >
        <input
          v-model="newPassword2"
          id="id_new_password2"
          name="new_password2"
          type="password"
          required=""
          :placeholder="$t('auth.password.new_password2')"
          class="form-control is-invalid"
        >
        <label for="id_new_password2">
          {{ $t('auth.password.new_password2') }}
        </label>
        <div
          v-for="error in errors.new_password2"
          class="invalid-feedback"
        >
          {{ error }}
        </div>
      </div>
      <div
        v-else
        class="form-floating mb-3"
      >
        <input
          v-model="newPassword2"
          id="id_new_password2"
          name="new_password2"
          type="password"
          required=""
          :placeholder="$t('auth.password.new_password2')"
          class="form-control"
        >
        <label for="id_new_password2">
          {{ $t('auth.password.new_password2') }}
        </label>
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

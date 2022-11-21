<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      errors: null
    }
  },
  methods: {
    login() {
      axios.post('/accounts/auth/login/', {
        username: this.username,
        password: this.password
      })
      .then(({ data }) => {
        window.localStorage.setItem('user', JSON.stringify(data))
        if (this.$route.query.redirect) {
          window.location.assign(`${ this.$route.query.redirect }`)
        } else {
          window.location.assign(`/${ this.$i18n.locale }`)
        }
      })
      .catch((error) => {
        this.errors = error.response.data
      })
    }
  }
}
</script>

<template>
  <div class="login-view">
    <h1 class="display-6 text-center mb-4">{{ $t('auth.login.login') }}</h1>

    <div v-if="errors && errors.non_field_errors">
      <div
        class="alert alert-danger d-flex align-items-center alert-dismissible fade show"
        role="alert"
      >
        <i class="fa-solid fa-circle-exclamation"></i>
        <div
          v-for="error in errors.non_field_errors"
          class="ms-3"
        >
          {{ error }}
        </div>
        <button
          @click="errors = null"
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </div>
    </div>

    <form @submit.prevent="login">
      <p class="fs-6 text-muted">
        {{ $t('auth.login.have_account') }}
        <LocaleRouterLink
          toName="Registration"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.signup') }}
        </LocaleRouterLink>
      </p>

      <div
        v-if="errors && errors.username"
        class="form-floating mb-3"
      >
        <input
          v-model="username"
          id="id_username"
          name="username"
          type="text"
          required=""
          :placeholder="$t('auth.login.username_email')"
          class="form-control is-invalid"
        >
        <label for="id_username">{{ $t('auth.login.username_email') }}</label>
        <div
          v-for="error in errors.username"
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
          v-model="username"
          id="id_username"
          name="username"
          type="text"
          required=""
          :placeholder="$t('auth.login.username_email')"
          class="form-control"
        >
        <label for="id_username">{{ $t('auth.login.username_email') }}</label>
      </div>

      <div
        v-if="errors && errors.password"
        class="form-floating mb-3"
      >
        <input
          v-model="password"
          id="id_password"
          name="password"
          type="password"
          required=""
          :placeholder="$t('auth.password.password')"
          class="form-control is-invalid"
        >
        <label for="id_password">{{ $t('auth.password.password') }}</label>
        <div
          v-for="error in errors.password"
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
          v-model="password"
          id="id_password"
          name="password"
          type="password"
          required=""
          :placeholder="$t('auth.password.password')"
          class="form-control"
        >
        <label for="id_password">{{ $t('auth.password.password') }}</label>
      </div>

      <button
        type="submit"
        class="btn btn-brand btn-lg w-100"
      >
        {{ $t('auth.signin') }}
      </button>
      <hr class="my-4">
      <div class="fs-6 text-muted">
        {{ $t('auth.login.forgot_your_password') }}
        <LocaleRouterLink
          toName="PasswordReset"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.password.reset_password') }}
        </LocaleRouterLink>
      </div>
    </form>
  </div>
</template>

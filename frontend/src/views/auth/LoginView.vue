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
          routeName="Registration"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.signup') }}
        </LocaleRouterLink>
      </p>

      <div class="row g-3 mb-3">
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.username"
            v-model="username"
            :label="$t('auth.login.username_email')"
            :errors="errors.username"
            id="id_username"
            name="username"
            type="text"
          />
          <BaseInput
            v-else
            v-model="username"
            :label="$t('auth.login.username_email')"
            id="id_username"
            name="username"
            type="text"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.password"
            v-model="password"
            :label="$t('auth.password.password')"
            :errors="errors.password"
            id="id_password"
            name="password"
            type="password"
          />
          <BaseInput
            v-else
            v-model="password"
            :label="$t('auth.password.password')"
            id="id_password"
            name="password"
            type="password"
          />
        </div>
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
          routeName="PasswordReset"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.password.reset_password') }}
        </LocaleRouterLink>
      </div>
    </form>
  </div>
</template>

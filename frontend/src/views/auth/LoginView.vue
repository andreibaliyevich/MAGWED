<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const { locale } = useI18n({ useScope: 'global' })

const loadingStatus = ref(false)

const username = ref('')
const password = ref('')

const errors = ref(null)

const login = async () => {
  loadingStatus.value = true
  try {
    const response = await axios.post('/accounts/auth/login/', {
      username: username.value,
      password: password.value
    })
    window.localStorage.setItem('user', JSON.stringify(response.data))
    if (route.query.redirect) {
      window.location.assign(`${ route.query.redirect }`)
    } else {
      window.location.assign(`/${ locale.value }`)
    }
  } catch (error) {
    errors.value = error.response.data
  } finally {
    loadingStatus.value = false
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
    <form @submit.prevent="login()">
      <p class="fs-6 text-muted">
        {{ $t('auth.login.have_account') }}
        <LocaleRouterLink
          routeName="Registration"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.register') }}
        </LocaleRouterLink>
      </p>
      <div class="row g-3 mb-3">
        <div class="col-md-12">
          <BaseInput
            v-model="username"
            type="text"
            id="id_username"
            name="username"
            :label="$t('auth.login.username_email')"
            :errors="errors?.username ? errors.username : []"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-model="password"
            type="password"
            id="id_password"
            name="password"
            :label="$t('auth.password.password')"
            :errors="errors?.password ? errors.password : []"
          />
        </div>
      </div>
      <SubmitButton
        :loadingStatus="loadingStatus"
        buttonClass="btn btn-brand btn-lg w-100"
      >
        {{ $t('auth.log_in') }}
      </SubmitButton>
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

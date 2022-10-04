<script setup>
import axios from 'axios'

import LocaleRouterLink from '@/components/UI/LocaleRouterLink.vue'
</script>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: '',
      userType: '',
      name: '',
      isLoading: false,
      status: null,
      errors: null
    }
  },
  methods: {
    registration() {
      this.isLoading = true
      axios.post('/' + this.$i18n.locale + '/accounts/auth/registration/', {
        username: this.username,
        email: this.email,
        password: this.password,
        password2: this.password2,
        user_type: this.userType,
        name: this.name
      })
      .then((response) => {
        if (response.status === 201) {
          this.status = '201'
          this.errors = null
        }
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
      .then(() => {
        this.isLoading = false
        document.body.scrollTop = 0
        document.documentElement.scrollTop = 0
      })
    }
  }
}
</script>

<template>
  <div class="registration-view">
    <h1 class="display-6 text-center mb-4">
      {{ $t('auth.registration.registration') }}
    </h1>

    <div
      v-if="isLoading"
      class="d-flex justify-content-center mb-3"
    >
      <div
        class="spinner-border"
        role="status"
      >
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-if="status == '201'">
      <p class="lead fs-3 text-muted">{{ $t('auth.registration.success1') }}</p>
      <p class="lead fs-5">
        {{ $t('auth.registration.success2') }}<br>
        {{ $t('auth.registration.success3') }}
      </p>
    </div>

    <form
      v-else
      @submit.prevent="registration"
    >
      <p class="fs-6 text-muted">
        {{ $t('auth.registration.have_account') }}
        <LocaleRouterLink
          :toName="'Login'"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.signin') }}
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
          :placeholder="$t('auth.registration.username')"
          class="form-control is-invalid"
        >
        <label for="id_username">{{ $t('auth.registration.username') }}</label>
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
          :placeholder="$t('auth.registration.username')"
          class="form-control"
        >
        <label for="id_username">{{ $t('auth.registration.username') }}</label>
      </div>

      <div
        v-if="errors && errors.email"
        class="form-floating mb-3"
      >
        <input
          v-model="email"
          id="id_email"
          name="email"
          type="email"
          maxlength="254"
          required=""
          :placeholder="$t('auth.registration.email')"
          class="form-control is-invalid"
        >
        <label for="id_email">{{ $t('auth.registration.email') }}</label>
        <div
          v-for="error in errors.email"
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
          v-model="email"
          id="id_email"
          name="email"
          type="email"
          maxlength="254"
          required=""
          :placeholder="$t('auth.registration.email')"
          class="form-control"
        >
        <label for="id_email">{{ $t('auth.registration.email') }}</label>
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

      <div
        v-if="errors && errors.password2"
        class="form-floating mb-3"
      >
        <input
          v-model="password2"
          id="id_password2"
          name="password2"
          type="password"
          required=""
          :placeholder="$t('auth.registration.password2')"
          class="form-control is-invalid"
        >
        <label for="id_password">{{ $t('auth.registration.password2') }}</label>
        <div
          v-for="error in errors.password2"
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
          v-model="password2"
          id="id_password2"
          name="password2"
          type="password"
          required=""
          :placeholder="$t('auth.registration.password2')"
          class="form-control"
        >
        <label for="id_password">{{ $t('auth.registration.password2') }}</label>
      </div>

      <div
        v-if="errors && errors.user_type"
        class="form-floating mb-3"
      >
        <select
          v-model="userType"
          id="id_user_type"
          name="user_type"
          required=""
          class="form-select is-invalid"
        >
          <option
            disabled
            value=""
          >
            {{ $t('auth.registration.please_select_user_type') }}
          </option>
          <option value="2">{{ $t('auth.registration.customer') }}</option>
          <option value="3">{{ $t('auth.registration.organizer') }}</option>
        </select>
        <label for="id_user_type">
          {{ $t('auth.registration.user_type') }}
        </label>
        <div
          v-for="error in errors.user_type"
          class="invalid-feedback"
        >
          {{ error }}
        </div>
      </div>
      <div
        v-else
        class="form-floating mb-3"
      >
        <select
          v-model="userType"
          id="id_user_type"
          name="user_type"
          required=""
          class="form-select"
        >
          <option
            disabled
            value=""
          >
            {{ $t('auth.registration.please_select_user_type') }}
          </option>
          <option value="2">{{ $t('auth.registration.customer') }}</option>
          <option value="3">{{ $t('auth.registration.organizer') }}</option>
        </select>
        <label for="id_user_type">
          {{ $t('auth.registration.user_type') }}
        </label>
      </div>

      <div
        v-if="errors && errors.name"
        class="form-floating mb-3"
      >
        <input
          v-model="name"
          id="id_name"
          name="name"
          type="text"
          required=""
          :placeholder="$t('auth.registration.name')"
          class="form-control is-invalid"
        >
        <label for="id_username">{{ $t('auth.registration.name') }}</label>
        <div
          v-for="error in errors.name"
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
          v-model="name"
          id="id_name"
          name="name"
          type="text"
          required=""
          :placeholder="$t('auth.registration.name')"
          class="form-control"
        >
        <label for="id_username">{{ $t('auth.registration.name') }}</label>
      </div>

      <button
        type="submit"
        class="btn btn-brand btn-lg w-100"
      >
        {{ $t('auth.signup') }}
      </button>
      <hr class="my-4">
      <div class="fs-6 text-muted">
        {{ $t('auth.registration.help') }}
      </div>
    </form>
  </div>
</template>

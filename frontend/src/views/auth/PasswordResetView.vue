<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      email: '',
      status: null,
      errors: null
    }
  },
  methods: {
    resetPassword() {
      axios.post('/' + this.$i18n.locale + '/accounts/auth/password/reset/', {
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
        document.body.scrollTop = 0
        document.documentElement.scrollTop = 0
      })
    }
  }
}
</script>

<template>
  <div class="container">
    <h1 class="display-6 mb-5">{{ $t('auth.password.password_reset') }}</h1>

    <div v-if="status" id="status">
      <div class="alert alert-success d-flex align-items-center alert-dismissible fade show" role="alert">
        <i class="fa-solid fa-circle-check"></i>
        <div v-if="status == '204'" class="ms-3">{{ $t('auth.password.success.reset') }}</div>
        <button @click="status = null" type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    </div>

    <form @submit.prevent="resetPassword" class="px-md-5">
      <p class="font-size-md">{{ $t('auth.password.reset_help') }}</p>
      <ul class="fs-6">
        <li>{{ $t('auth.password.step1') }}</li>
        <li>{{ $t('auth.password.step2') }}</li>
        <li>{{ $t('auth.password.step3') }}</li>
      </ul>
      <div class="mb-3">
        <label for="id_current_password" class="form-label">{{ $t('auth.password.email') }}</label>
        <div v-if="errors && errors.email">
          <input v-model="email" id="id_email" name="email" type="email" maxlength="254" required="" class="form-control is-invalid">
          <div v-for="error in errors.email" class="invalid-feedback">{{ error }}</div>
        </div>
        <input v-else v-model="email" id="id_email" name="email" type="email" maxlength="254" required="" class="form-control">
      </div>
      <div class="col-12">
        <button type="submit" class="btn btn-primary">{{ $t('auth.password.reset_password') }}</button>
      </div>
    </form>
  </div>
</template>

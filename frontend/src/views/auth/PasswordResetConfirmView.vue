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
    <h1 class="display-6 mb-5">{{ $t('auth.password.password_reset_confirmation') }}</h1>

    <div v-if="status" id="status">
      <div class="alert alert-success d-flex align-items-center alert-dismissible fade show" role="alert">
        <i class="fa-solid fa-circle-check"></i>
        <div v-if="status == '204'" class="ms-3">{{ $t('auth.password.success.reset_confirm') }}</div>
        <button @click="status = null" type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    </div>

    <form @submit.prevent="confirmPasswordReset" class="px-md-5">
      <div class="mb-3">
        <label for="id_new_password" class="form-label">{{ $t('auth.password.new_password') }}</label>
        <div v-if="errors && errors.new_password">
          <input v-model="newPassword" id="id_new_password" name="new_password" type="password" required="" class="form-control is-invalid">
          <div v-for="error in errors.new_password" class="invalid-feedback">{{ error }}</div>
        </div>
        <input v-else v-model="newPassword" id="id_new_password" name="new_password" type="password" required="" class="form-control">
      </div>
      <ul class="fs-6">
        <li>{{ $t('auth.password.advice1') }}</li>
        <li>{{ $t('auth.password.advice2') }}</li>
        <li>{{ $t('auth.password.advice3') }}</li>
        <li>{{ $t('auth.password.advice4') }}</li>
      </ul>
      <div class="mb-3">
        <label for="id_new_password2" class="form-label">{{ $t('auth.password.new_password2') }}</label>
        <div v-if="errors && errors.new_password2">
          <input v-model="newPassword2" id="id_new_password2" name="new_password2" type="password" required="" class="form-control is-invalid">
          <div v-for="error in errors.new_password2" class="invalid-feedback">{{ error }}</div>
        </div>
        <input v-else v-model="newPassword2" id="id_new_password2" name="new_password2" type="password" required="" class="form-control">
      </div>
      <div class="col-12">
        <button type="submit" class="btn btn-primary">{{ $t('auth.password.confirm_password_reset') }}</button>
      </div>
    </form>
  </div>
</template>

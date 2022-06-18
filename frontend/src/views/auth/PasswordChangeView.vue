<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      currentPassword: '',
      newPassword: '',
      newPassword2: '',
      status: null,
      errors: null
    }
  },
  methods: {
    changePassword() {
      axios.post('/' + this.$i18n.locale + '/accounts/auth/password/change/', {
        current_password: this.currentPassword,
        new_password: this.newPassword,
        new_password2: this.newPassword2
      })
      .then((response) => {
        if (response.status === 204) {
          this.currentPassword = ''
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
  <div class="password-change">
    <h1 class="display-6 mb-5">{{ $t('auth.passwordchange.password_change') }}</h1>

    <div v-if="status" id="status">
      <div class="alert alert-success d-flex align-items-center alert-dismissible fade show" role="alert">
        <i class="fa-solid fa-circle-check"></i>
        <div v-if="status == '204'" class="ms-3">{{ $t('auth.passwordchange.password_updated_successfully') }}</div>
        <button @click="status = null" type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    </div>

    <form @submit.prevent="changePassword" class="px-md-5">
      <div class="mb-3">
        <label for="id_current_password" class="form-label">{{ $t('auth.passwordchange.current_password') }}</label>
        <div v-if="errors && errors.current_password">
          <input v-model="currentPassword" id="id_current_password" name="current_password" type="password" required="" class="form-control is-invalid">
          <div v-for="error in errors.current_password" class="invalid-feedback">{{ error }}</div>
        </div>
        <input v-else v-model="currentPassword" id="id_current_password" name="current_password" type="password" required="" class="form-control">
      </div>
      <div class="mb-3">
        <label for="id_new_password" class="form-label">{{ $t('auth.passwordchange.new_password') }}</label>
        <div v-if="errors && errors.new_password">
          <input v-model="newPassword" id="id_new_password" name="new_password" type="password" required="" class="form-control is-invalid">
          <div v-for="error in errors.new_password" class="invalid-feedback">{{ error }}</div>
        </div>
        <input v-else v-model="newPassword" id="id_new_password" name="new_password" type="password" required="" class="form-control">
      </div>
      <ul class="fs-6">
        <li>{{ $t('auth.passwordchange.advice1') }}</li>
        <li>{{ $t('auth.passwordchange.advice2') }}</li>
        <li>{{ $t('auth.passwordchange.advice3') }}</li>
        <li>{{ $t('auth.passwordchange.advice4') }}</li>
      </ul>
      <div class="mb-3">
        <label for="id_new_password2" class="form-label">{{ $t('auth.passwordchange.new_password2') }}</label>
        <div v-if="errors && errors.new_password2">
          <input v-model="newPassword2" id="id_new_password2" name="new_password2" type="password" required="" class="form-control is-invalid">
          <div v-for="error in errors.new_password2" class="invalid-feedback">{{ error }}</div>
        </div>
        <input v-else v-model="newPassword2" id="id_new_password2" name="new_password2" type="password" required="" class="form-control">
      </div>
      <div class="col-12">
        <button type="submit" class="btn btn-primary">{{ $t('auth.passwordchange.change') }}</button>
      </div>
    </form>
  </div>
</template>

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
      axios.post('/accounts/auth/password/change/', {
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
  <div class="password-change-view">
    <h1 class="display-6 mb-5">
      {{ $t('auth.passwordchange.password_change') }}
    </h1>

    <div v-if="status == '204'">
      <div
        class="alert alert-success d-flex align-items-center alert-dismissible fade show"
        role="alert"
      >
        <i class="fa-solid fa-circle-check"></i>
        <div class="ms-3">{{ $t('auth.passwordchange.success') }}</div>
        <button
          @click="status = null"
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </div>
    </div>

    <form
      @submit.prevent="changePassword"
      class="px-md-5"
    >
      <div class="mb-3">
        <BaseInput
          v-if="errors && errors.current_password"
          v-model="currentPassword"
          :label="$t('auth.passwordchange.current_password')"
          :errors="errors.current_password"
          id="id_current_password"
          name="current_password"
          type="password"
        />
        <BaseInput
          v-else
          v-model="currentPassword"
          :label="$t('auth.passwordchange.current_password')"
          id="id_current_password"
          name="current_password"
          type="password"
        />
      </div>
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
        class="btn btn-primary"
      >
        {{ $t('auth.password.change_password') }}
      </button>
    </form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'

const loadingStatus = ref(false)
const email = ref('')

const status = ref(null)
const errors = ref(null)

const resetPassword = async () => {
  loadingStatus.value = true
  try {
    const response = await axios.post('/accounts/auth/password/reset/', {
      email: email.value
    })
    if (response.status === 204) {
      status.value = 204
      errors.value = null
    }
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    loadingStatus.value = false
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0
  }
}
</script>

<template>
  <div class="mx-10">
    <h1 class="text-h4 text-md-h3 text-center mb-4">
      {{ $t('auth.passwordreset.password_reset') }}
    </h1>

    <v-alert
      v-if="status === 204"
      type="success"
      variant="tonal"
      :title="$t('auth.passwordreset.success1')"
    >
      <p class="text-body-1 text-grey-darken-1">
        {{ $t('auth.passwordreset.success2') }}<br>
        {{ $t('auth.passwordreset.success3') }}
      </p>
    </v-alert>

    <div v-else>
      <p class="text-body-1 text-grey-darken-1 mb-5">
        {{ $t('auth.passwordreset.help') }}
      </p>
      <p class="text-body-1 text-grey-darken-1">
        {{ $t('auth.passwordreset.help') }}
      </p>
      <v-list class="text-body-1 text-grey-darken-1">
        <v-list-item>
          1. {{ $t('auth.passwordreset.step1') }}
        </v-list-item>
        <v-list-item>
          2. {{ $t('auth.passwordreset.step2') }}
        </v-list-item>
        <v-list-item>
          3. {{ $t('auth.passwordreset.step3') }}
        </v-list-item>
      </v-list>

      <v-form @submit.prevent="resetPassword()">
        <v-text-field
          v-model="email"
          :readonly="loadingStatus"
          variant="filled"
          type="email"
          maxlength="254"
          :label="$t('auth.passwordreset.email')"
          :error-messages="errors?.email ? errors.email : []"
        ></v-text-field>
        <v-btn
          :loading="loadingStatus"
          type="submit"
          variant="flat"
          color="primary"
          size="x-large"
          block
        >
          {{ $t('auth.password.reset_password') }}
        </v-btn>
      </v-form>

      <v-divider class="my-5"></v-divider>
      <v-btn
        :to="{ name: 'Login' }"
        variant="text"
        prepend-icon="mdi-chevron-left"
        class="text-none"
      >
        {{ $t('auth.passwordreset.back_to_login') }}
      </v-btn>
    </div>
  </div>
</template>

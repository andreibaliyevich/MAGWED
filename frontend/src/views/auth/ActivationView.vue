<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      status: null,
      errors: null
    }
  },
  mounted() {
    axios.post('/accounts/auth/activation/', {
      uid: this.$route.params.uid,
      token: this.$route.params.token
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
  }
}
</script>

<template>
  <div class="activation-view">
    <h1 class="display-6 text-center mb-4">
      {{ $t('auth.activation.activation') }}
    </h1>

    <div v-if="status == '204'">
      <p class="lead fs-3 text-muted">{{ $t('auth.activation.success1') }}</p>
      <p class="lead fs-5">
        {{ $t('auth.activation.success2') }}<br>
        {{ $t('auth.activation.success3') }}
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
      <p class="lead fs-3 text-danger">{{ $t('auth.activation.error') }}</p>
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
          toName="Registration"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.signup') }}
        </LocaleRouterLink>
      </div>
    </div>
  </div>
</template>

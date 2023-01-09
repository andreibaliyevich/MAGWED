<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const loadingStatus = ref(true)

const status = ref(null)
const errors = ref(null)

onMounted(async () => {
  try {
    const response = await axios.post('/accounts/auth/activation/', {
      uid: route.params.uid,
      token: route.params.token
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
  }
})
</script>

<template>
  <div class="activation-view">
    <h1 class="display-6 text-center mb-4">
      {{ $t('auth.activation.activation') }}
    </h1>

    <LoadingIndicator v-if="loadingStatus" />
    <div v-else>
      <div v-if="status == 204">
        <p class="lead fs-3 text-muted">{{ $t('auth.activation.success1') }}</p>
        <p class="lead fs-5">
          {{ $t('auth.activation.success2') }}<br>
          {{ $t('auth.activation.success3') }}
        </p>
        <div class="fs-6 text-center">
          <LocaleRouterLink
            routeName="Login"
            class="link-primary text-decoration-none"
          >
            {{ $t('auth.log_in') }}
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
            routeName="Registration"
            class="link-primary text-decoration-none"
          >
            {{ $t('auth.register') }}
          </LocaleRouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

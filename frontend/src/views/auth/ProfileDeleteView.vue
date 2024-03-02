<script setup>
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { useUserStore } from '@/stores/user.js'

const router = useRouter()
const { locale } = useI18n({ useScope: 'global' })
const userStore = useUserStore()

const profileDeleting = ref(false)
const currentPassword = ref('')
const errors = ref(null)

const deletingProfile = async () => {
  profileDeleting.value = true
  try {
    const response = await axios.delete('/accounts/auth/profile/', {
      data: {
        current_password: currentPassword.value
      }
    })
    errors.value = null
    window.localStorage.removeItem('user')
    userStore.$reset()
    router.push({
      name: 'Home',
      params: { locale: locale.value }
    })
  } catch (error) {
    errors.value = error.response.data
  } finally {
    profileDeleting.value = false
  }
}
</script>

<template>
  <div class="mx-md-10 mb-10">
    <h1 class="text-h4 text-md-h3 text-center my-5">
      {{ $t('auth.profile_delete.profile_delete') }}
    </h1>

    <p class="text-body-1 mb-5">
      {{ $t('auth.profile_delete.advice1') }}<br>
      {{ $t('auth.profile_delete.advice2') }}
    </p>

    <v-form @submit.prevent="deletingProfile()">
      <v-text-field
        v-model="currentPassword"
        :readonly="profileDeleting"
        type="password"
        variant="filled"
        :label="$t('auth.profile_delete.password_confirmation')"
        :error-messages="errors?.current_password ? errors.current_password : []"
      ></v-text-field>
      <v-btn
        :loading="profileDeleting"
        type="submit"
        variant="flat"
        color="primary"
        size="x-large"
        class="text-none mt-3"
      >
        {{ $t('auth.profile_delete.delete_profile') }}
      </v-btn>
    </v-form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
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
        'current_password': currentPassword.value
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
  <div class="profile-delete-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">{{ $t('auth.profile_delete.profile_delete') }}</h1>
      <p class="lead fs-5">
        {{ $t('auth.profile_delete.advice1') }}<br>
        {{ $t('auth.profile_delete.advice2') }}
      </p>
      <form @submit.prevent="deletingProfile()">
        <div class="mb-3">
          <BaseInput
            v-model="currentPassword"
            type="password"
            id="id_current_password"
            name="current_password"
            :label="$t('auth.profile_delete.password_confirmation')"
            :errors="errors?.current_password ? errors.current_password : []"
          />
        </div>
        <SubmitButton
          :loadingStatus="profileDeleting"
          buttonClass="btn btn-brand btn-lg"
        >
          {{ $t('auth.profile_delete.delete_profile') }}
        </SubmitButton>
      </form>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'

const { t } = useI18n({ useScope: 'global' })

const passwordUpdating = ref(false)

const currentPassword = ref('')
const newPassword = ref('')
const newPassword2 = ref('')

const status = ref(null)
const errors = ref(null)

const changePassword = async () => {
  passwordUpdating.value = true
  try {
    const response = await axios.post('/accounts/auth/password/change/', {
      current_password: currentPassword.value,
      new_password: newPassword.value,
      new_password2: newPassword2.value
    })
    currentPassword.value = ''
    newPassword.value = ''
    newPassword2.value = ''
    // status.value = t('auth.passwordchange.success')
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    passwordUpdating.value = false
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0
  }
}
</script>

<template>
  <div class="mx-md-10">
    <h1 class="text-h4 text-md-h3 text-center my-5">
      {{ $t('auth.passwordchange.password_change') }}
    </h1>
  </div>
</template>

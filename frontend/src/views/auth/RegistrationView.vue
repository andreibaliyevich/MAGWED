<script setup>
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { ref, watch, onMounted } from 'vue'

const { t, locale } = useI18n({ useScope: 'global' })

const loadingStatus = ref(false)
const userTypeOptions = ref([])

const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const userType = ref('')
const name = ref('')

const status = ref(null)
const errors = ref(null)

const setUserTypeOptions = () => {
  userTypeOptions.value = [
    { value: 2, text: t('auth.registration.customer') },
    { value: 3, text: t('auth.registration.organizer') }
  ]
}

const registration = async () => {
  loadingStatus.value = true
  try {
    const response = await axios.post('/accounts/auth/registration/', {
      username: username.value,
      email: email.value,
      password: password.value,
      password2: password2.value,
      user_type: userType.value,
      name: name.value
    })
    if (response.status === 201) {
      status.value = 201
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

watch(locale, () => {
  setUserTypeOptions()
})

onMounted(() => {
  setUserTypeOptions()
})
</script>

<template>
  <div class="registration-view">
    <h1 class="display-6 text-center">
      {{ $t('auth.registration.registration') }}
    </h1>
    <div
      v-if="status == 201"
      class="mt-4"
    >
      <p class="lead fs-3 text-muted">{{ $t('auth.registration.success1') }}</p>
      <p class="lead fs-5">
        {{ $t('auth.registration.success2') }}<br>
        {{ $t('auth.registration.success3') }}
      </p>
    </div>
    <form
      v-else
      @submit.prevent="registration()"
      class="mt-4"
    >
      <p class="fs-6 text-muted">
        {{ $t('auth.registration.have_account') }}
        <router-link
          :to="{ name: 'Login' }"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.log_in') }}
        </router-link>
      </p>
      <div class="row g-3 mb-3">
        <div class="col-md-12">
          <BaseInput
            v-model="username"
            type="text"
            id="id_username"
            name="username"
            :label="$t('auth.registration.username')"
            :errors="errors?.username ? errors.username : []"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-model="email"
            type="email"
            maxlength="254"
            id="id_email"
            name="email"
            :label="$t('auth.registration.email')"
            :errors="errors?.email ? errors.email : []"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-model="password"
            type="password"
            id="id_password"
            name="password"
            :label="$t('auth.password.password')"
            :errors="errors?.password ? errors.password : []"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-model="password2"
            type="password"
            id="id_password2"
            name="password2"
            :label="$t('auth.registration.password2')"
            :errors="errors?.password2 ? errors.password2 : []"
          />
        </div>
        <div class="col-md-12">
          <BaseSelect
            v-model="userType"
            :options="userTypeOptions"
            id="id_user_type"
            name="user_type"
            :label="$t('auth.registration.user_type')"
            :errors="errors?.user_type ? errors.user_type : []"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-model="name"
            type="text"
            id="id_name"
            name="name"
            :label="$t('auth.registration.name')"
            :errors="errors?.name ? errors.name : []"
          />
        </div>
      </div>
      <SubmitButton
        :loadingStatus="loadingStatus"
        buttonClass="btn btn-brand btn-lg w-100"
      >
        {{ $t('auth.register') }}
      </SubmitButton>
      <hr class="my-4">
      <div class="fs-6 text-muted">
        {{ $t('auth.registration.help') }}
      </div>
    </form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useOptionsOfCountries } from '@/composables/optionsOfCountries.js'
import { useOptionsOfCities } from '@/composables/optionsOfCities.js'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()

const profileLoading = ref(true)
const profileUpdating = ref(false)

const name = ref('')
const country = ref(null)
const city = ref(null)
const phone = ref('')

const { countriesOptions } = useOptionsOfCountries()
const { citiesOptions } = useOptionsOfCities(country)

const errors = ref(null)

const getProfileData = async () => {
  try {
    const response = await axios.get('/accounts/auth/profile/')
    name.value = response.data.name
    country.value = response.data.country
    city.value = response.data.city
    phone.value = response.data.phone
  } catch (error) {
    console.error(error)
  } finally {
    profileLoading.value = false
  }
}

const updateProfile = async () => {
  profileUpdating.value = true

  if (!country.value) {
    country.value = null
  }
  if (!city.value) {
    city.value = null
  }

  try {
    const response = await axios.put('/accounts/auth/profile/', {
      'name': name.value,
      'country': country.value,
      'city': city.value,
      'phone': phone.value
    })
    userStore.updateName(name.value)
    window.localStorage.setItem('user', JSON.stringify({
      'uuid': userStore.uuid,
      'username': userStore.username,
      'email': userStore.email,
      'user_type': userStore.userType,
      'name': name.value,
      'avatar': userStore.avatar,
      'token': userStore.token
    }))
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  } finally {
    profileUpdating.value = false
  }
}

watch(citiesOptions, (newValue, oldValue) => {
  if (oldValue.length) {
    city.value = null
  }
})

onMounted(() => {
  getProfileData()
})
</script>

<template>
  <div class="admin-profile-form">
    <LoadingIndicator v-if="profileLoading" />
    <form
      v-else
      @submit.prevent="updateProfile()"
      class="row g-3 mt-3"
    >
      <div class="col-md-12">
        <BaseInput
          v-if="errors && errors.name"
          v-model="name"
          :label="$t('auth.profile.name')"
          :errors="errors.name"
          id="id_name"
          name="name"
          type="text"
        />
        <BaseInput
          v-else
          v-model="name"
          :label="$t('auth.profile.name')"
          id="id_name"
          name="name"
          type="text"
        />
      </div>
      <div class="col-md-6">
        <BaseSelect
          v-if="errors && errors.country"
          v-model="country"
          :label="$t('auth.profile.country')"
          :options="countriesOptions"
          :errors="errors.country"
          id="id_country"
          name="country"
        />
        <BaseSelect
          v-else
          v-model="country"
          :label="$t('auth.profile.country')"
          :options="countriesOptions"
          id="id_country"
          name="country"
        />
      </div>
      <div class="col-md-6">
        <BaseSelect
          v-if="errors && errors.city"
          v-model="city"
          :label="$t('auth.profile.city')"
          :options="citiesOptions"
          :errors="errors.city"
          id="id_city"
          name="city"
        />
        <BaseSelect
          v-else
          v-model="city"
          :label="$t('auth.profile.city')"
          :options="citiesOptions"
          id="id_city"
          name="city"
        />
      </div>
      <div class="col-md-12">
        <BaseInput
          v-if="errors && errors.phone"
          v-model="phone"
          :label="$t('auth.profile.phone')"
          :errors="errors.phone"
          id="id_phone"
          name="phone"
          type="tel"
          maxlength="21"
        />
        <BaseInput
          v-else
          v-model="phone"
          :label="$t('auth.profile.phone')"
          id="id_phone"
          name="phone"
          type="tel"
          maxlength="21"
        />
      </div>
      <div class="col-12">
        <SubmitButton
          :loadingStatus="profileUpdating"
          buttonClass="btn btn-brand btn-lg"
        >
          {{ $t('auth.profile.update_profile') }}
        </SubmitButton>
      </div>
    </form>
  </div>
</template>

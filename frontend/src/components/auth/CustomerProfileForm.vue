<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import {
  useOptionsOfCountriesAndCities
} from '@/composables/optionsOfCountriesAndCities.js'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()

const profileLoading = ref(true)
const profileUpdating = ref(false)

const name = ref('')
const country = ref(null)
const city = ref(null)
const phone = ref('')
const dateOfWedding = ref(null)

const {
  countriesOptions,
  citiesOptions
} = useOptionsOfCountriesAndCities(country)

const errors = ref(null)

const getProfileData = async () => {
  try {
    const response = await axios.get('/accounts/auth/profile/')
    name.value = response.data.user.name
    country.value = response.data.user.country
    city.value = response.data.user.city
    phone.value = response.data.user.phone
    dateOfWedding.value = response.data.date_of_wedding
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
      'user': {
        'name': name.value,
        'country': country.value,
        'city': city.value,
        'phone': phone.value
      },
      'date_of_wedding': dateOfWedding.value
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
  <div class="customer-profile-form">
    <LoadingIndicator v-if="profileLoading" />
    <form
      v-else
      @submit.prevent="updateProfile()"
      class="row g-3 mt-3"
    >
      <div class="col-md-12">
        <BaseInput
          v-if="errors && errors.user && errors.user.name"
          v-model="name"
          :label="$t('auth.profile.name')"
          :errors="errors.user.name"
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
          v-if="errors && errors.user && errors.user.country"
          v-model="country"
          :label="$t('auth.profile.country')"
          :options="countriesOptions"
          :errors="errors.user.country"
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
          v-if="errors && errors.user && errors.user.city"
          v-model="city"
          :label="$t('auth.profile.city')"
          :options="citiesOptions"
          :errors="errors.user.city"
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
          v-if="errors && errors.user && errors.user.phone"
          v-model="phone"
          :label="$t('auth.profile.phone')"
          :errors="errors.user.phone"
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
      <div class="col-md-12">
        <BaseInput
          v-if="errors && errors.date_of_wedding"
          v-model="dateOfWedding"
          :label="$t('auth.profile.date_of_wedding')"
          :errors="errors.date_of_wedding"
          id="id_date_of_wedding"
          name="date_of_wedding"
          type="date"
        />
        <BaseInput
          v-else
          v-model="dateOfWedding"
          :label="$t('auth.profile.date_of_wedding')"
          id="id_date_of_wedding"
          name="date_of_wedding"
          type="date"
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

<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useOptionsOfCountries } from '@/composables/optionsOfCountries.js'
import { useOptionsOfCities } from '@/composables/optionsOfCities.js'

const userStore = useUserStore()

const profileLoading = ref(true)
const profileUpdating = ref(false)

const name = ref('')
const country = ref(null)
const city = ref(null)
const phone = ref('')
const dateOfWedding = ref(null)

const { countryOptions } = useOptionsOfCountries()
const { cityOptions } = useOptionsOfCities(country)

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
      user: {
        name: name.value,
        country: country.value,
        city: city.value,
        phone: phone.value
      },
      date_of_wedding: dateOfWedding.value
    })
    userStore.updateName(name.value)
    window.localStorage.setItem('user', JSON.stringify({
      uuid: userStore.uuid,
      username: userStore.username,
      email: userStore.email,
      user_type: userStore.userType,
      name: name.value,
      avatar: userStore.avatar,
      token: userStore.token
    }))
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  } finally {
    profileUpdating.value = false
  }
}

watch(country, (newValue, oldValue) => {
  if (oldValue) {
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
          v-model="name"
          type="text"
          maxlength="255"
          id="id_name"
          name="name"
          :label="$t('user.name')"
          :errors="errors?.user?.name ? errors.user.name : []"
        />
      </div>
      <div class="col-md-6">
        <BaseSelect
          v-model="country"
          :options="countryOptions"
          id="id_country"
          name="country"
          :label="$t('user.country')"
          :errors="errors?.user?.country ? errors.user.country : []"
        />
      </div>
      <div class="col-md-6">
        <BaseSelect
          v-model="city"
          :options="cityOptions"
          id="id_city"
          name="city"
          :label="$t('user.city')"
          :errors="errors?.user?.city ? errors.user.city : []"
        />
      </div>
      <div class="col-md-12">
        <BaseInput
          v-model="phone"
          type="tel"
          maxlength="21"
          id="id_phone"
          name="phone"
          :label="$t('user.phone')"
          :errors="errors?.user?.phone ? errors.user.phone : []"
        />
      </div>
      <div class="col-md-12">
        <BaseInput
          v-model="dateOfWedding"
          type="date"
          id="id_date_of_wedding"
          name="date_of_wedding"
          :label="$t('user.date_of_wedding')"
          :errors="errors?.date_of_wedding ? errors.date_of_wedding : []"
        />
      </div>
      <div class="col-12">
        <SubmitButton
          :loadingStatus="profileUpdating"
          buttonClass="btn btn-brand btn-lg"
        >
          {{ $t('user.update_profile') }}
        </SubmitButton>
      </div>
    </form>
  </div>
</template>

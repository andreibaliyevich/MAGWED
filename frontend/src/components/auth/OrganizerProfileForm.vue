<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useOptionsOfRoleTypes } from '@/composables/optionsOfRoleTypes.js'
import { useOptionsOfCountries } from '@/composables/optionsOfCountries.js'
import { useOptionsOfCities } from '@/composables/optionsOfCities.js'
import { useOptionsOfCitiesExtra } from '@/composables/optionsOfCitiesExtra.js'
import { useOptionsOfLanguages } from '@/composables/optionsOfLanguages.js'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()

const profileLoading = ref(true)
const profileUpdating = ref(false)

const name = ref('')
const country = ref(null)
const city = ref(null)
const phone = ref('')
const roles = ref([])
const description = ref('')
const countries = ref([])
const cities = ref([])
const languages = ref([])
const costWork = ref(0.00)
const numberHours = ref(0)
const profileURL = ref('')
const rating = ref(0.0)
const proTime = ref(null)

const { roleTypesOptions } = useOptionsOfRoleTypes()
const { countriesOptions } = useOptionsOfCountries()
const { citiesOptions } = useOptionsOfCities(country)
const { citiesExtraOptions } = useOptionsOfCitiesExtra(countries)
const { languagesOptions } = useOptionsOfLanguages()

const errors = ref(null)

const getProfileData = async () => {
  try {
    const response = await axios.get('/accounts/auth/profile/')
    name.value = response.data.user.name
    country.value = response.data.user.country
    city.value = response.data.user.city
    phone.value = response.data.user.phone
    roles.value = response.data.roles
    description.value = response.data.description
    countries.value = response.data.countries
    cities.value = response.data.cities
    languages.value = response.data.languages
    costWork.value = response.data.cost_work
    numberHours.value = response.data.number_hours
    profileURL.value = response.data.profile_url
    rating.value = response.data.rating
    proTime.value = response.data.pro_time
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
      'roles': roles.value,
      'description': description.value,
      'countries': countries.value,
      'cities': cities.value,
      'languages': languages.value,
      'cost_work': costWork.value,
      'number_hours': numberHours.value,
      'profile_url': profileURL.value
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

watch(citiesExtraOptions, (newValue, oldValue) => {
  if (newValue.length < oldValue.length) {
    let newCitiesValues = []
    newValue.forEach(element => newCitiesValues.push(element.value))
    cities.value = cities.value.filter((element) => {
      return newCitiesValues.includes(element)
    })
  }
})

onMounted(() => {
  getProfileData()
})
</script>

<template>
  <div class="organizer-profile-form">
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
          id="id_name"
          name="name"
          type="text"
          :label="$t('auth.profile.name')"
          :errors="errors.user.name"
        />
        <BaseInput
          v-else
          v-model="name"
          id="id_name"
          name="name"
          type="text"
          :label="$t('auth.profile.name')"
        />
      </div>
      <div class="col-md-6">
        <BaseSelect
          v-if="errors && errors.user && errors.user.country"
          v-model="country"
          :options="countriesOptions"
          id="id_country"
          name="country"
          :label="$t('auth.profile.country')"
          :errors="errors.user.country"
        />
        <BaseSelect
          v-else
          v-model="country"
          :options="countriesOptions"
          id="id_country"
          name="country"
          :label="$t('auth.profile.country')"
        />
      </div>
      <div class="col-md-6">
        <BaseSelect
          v-if="errors && errors.user && errors.user.city"
          v-model="city"
          :options="citiesOptions"
          id="id_city"
          name="city"
          :label="$t('auth.profile.city')"
          :errors="errors.user.city"
        />
        <BaseSelect
          v-else
          v-model="city"
          :options="citiesOptions"
          id="id_city"
          name="city"
          :label="$t('auth.profile.city')"
        />
      </div>
      <div class="col-md-12">
        <BaseInput
          v-if="errors && errors.user && errors.user.phone"
          v-model="phone"
          id="id_phone"
          name="phone"
          type="tel"
          maxlength="21"
          :label="$t('auth.profile.phone')"
          :errors="errors.user.phone"
        />
        <BaseInput
          v-else
          v-model="phone"
          id="id_phone"
          name="phone"
          type="tel"
          maxlength="21"
          :label="$t('auth.profile.phone')"
        />
      </div>
      <div class="col-md-12">
        <InputMultipleSelect
          v-if="errors && errors.roles"
          v-model="roles"
          :options="roleTypesOptions"
          id="id_roles"
          name="roles"
          :label="$t('auth.profile.roles')"
          :errors="errors.roles"
        />
        <InputMultipleSelect
          v-else
          v-model="roles"
          :options="roleTypesOptions"
          id="id_roles"
          name="roles"
          :label="$t('auth.profile.roles')"
        />
      </div>
      <div class="col-md-12">
        <BaseTextarea
          v-if="errors && errors.description"
          v-model="description"
          id="id_description"
          name="description"
          :label="$t('auth.profile.description')"
          :errors="errors.description"
        />
        <BaseTextarea
          v-else
          v-model="description"
          id="id_description"
          name="description"
          :label="$t('auth.profile.description')"
        />
      </div>
      <div class="col-md-12">
        <InputMultipleSelect
          v-if="errors && errors.countries"
          v-model="countries"
          :options="countriesOptions"
          id="id_countries"
          name="countries"
          :label="$t('auth.profile.countries')"
          :errors="errors.countries"
        />
        <InputMultipleSelect
          v-else
          v-model="countries"
          :options="countriesOptions"
          id="id_countries"
          name="countries"
          :label="$t('auth.profile.countries')"
        />
      </div>
      <div class="col-md-12">
        <InputMultipleSelect
          v-if="errors && errors.cities"
          v-model="cities"
          :options="citiesExtraOptions"
          id="id_cities"
          name="cities"
          :label="$t('auth.profile.cities')"
          :errors="errors.cities"
        />
        <InputMultipleSelect
          v-else
          v-model="cities"
          :options="citiesExtraOptions"
          id="id_cities"
          name="cities"
          :label="$t('auth.profile.cities')"
        />
      </div>
      <div class="col-md-12">
        <InputMultipleSelect
          v-if="errors && errors.languages"
          v-model="languages"
          :options="languagesOptions"
          id="id_languages"
          name="languages"
          :label="$t('auth.profile.languages')"
          :errors="errors.languages"
        />
        <InputMultipleSelect
          v-else
          v-model="languages"
          :options="languagesOptions"
          id="id_languages"
          name="languages"
          :label="$t('auth.profile.languages')"
        />
      </div>
      <div class="col-md-6">
        <BaseInput
          v-if="errors && errors.cost_work"
          v-model="costWork"
          id="id_cost_work"
          name="cost_work"
          type="number"
          min="0.00"
          step="0.01"
          required=""
          :label="$t('auth.profile.cost_work')"
          :errors="errors.cost_work"
        />
        <BaseInput
          v-else
          v-model="costWork"
          id="id_cost_work"
          name="cost_work"
          type="number"
          min="0.00"
          step="0.01"
          required=""
          :label="$t('auth.profile.cost_work')"
        />
        <div class="form-text">{{ $t('form_help.cost_work') }}</div>
      </div>
      <div class="col-md-6">
        <BaseInput
          v-if="errors && errors.number_hours"
          v-model="numberHours"
          id="id_number_hours"
          name="number_hours"
          type="number"
          min="0"
          required=""
          :label="$t('auth.profile.number_hours')"
          :errors="errors.number_hours"
        />
        <BaseInput
          v-else
          v-model="numberHours"
          id="id_number_hours"
          name="number_hours"
          type="number"
          min="0"
          required=""
          :label="$t('auth.profile.number_hours')"
        />
      </div>
      <div class="col-md-12">
        <BaseInput
          v-if="errors && errors.profile_url"
          v-model="profileURL"
          id="id_profile_url"
          name="profile_url"
          type="text"
          maxlength="64"
          required=""
          :label="$t('auth.profile.profile_url')"
          :errors="errors.profile_url"
        />
        <BaseInput
          v-else
          v-model="profileURL"
          id="id_profile_url"
          name="profile_url"
          type="text"
          maxlength="64"
          required=""
          :label="$t('auth.profile.profile_url')"
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

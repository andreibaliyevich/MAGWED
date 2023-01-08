<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useOptionsOfRoleType } from '@/composables/optionsOfRoleType.js'
import {
  useOptionsOfCountriesAndCities
} from '@/composables/optionsOfCountriesAndCities.js'
import { useOptionsOfCitiesExtra } from '@/composables/optionsOfCitiesExtra.js'
import { useOptionsOfLanguages } from '@/composables/optionsOfLanguages.js'
import { useUserStore } from '@/stores/user.js'

const user = useUserStore()

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

const { roleTypeOptions } = useOptionsOfRoleType()
const {
  countriesOptions,
  citiesOptions
} = useOptionsOfCountriesAndCities(country)
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
    user.updateName(name.value)
    window.localStorage.setItem('user', JSON.stringify({
      'token': user.token,
      'username': user.username,
      'email': user.email,
      'user_type': user.userType,
      'name': name.value,
      'avatar': user.avatar
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
        <MultipleSelect
          v-if="errors && errors.roles"
          v-model="roles"
          :label="$t('auth.profile.roles')"
          :options="roleTypeOptions"
          :errors="errors.roles"
          id="id_roles"
          name="roles"
        />
        <MultipleSelect
          v-else
          v-model="roles"
          :label="$t('auth.profile.roles')"
          :options="roleTypeOptions"
          id="id_roles"
          name="roles"
        />
      </div>
      <div class="col-md-12">
        <BaseTextarea
          v-if="errors && errors.description"
          v-model="description"
          :label="$t('auth.profile.description')"
          :errors="errors.description"
          id="id_description"
          name="description"
        />
        <BaseTextarea
          v-else
          v-model="description"
          :label="$t('auth.profile.description')"
          id="id_description"
          name="description"
        />
      </div>
      <div class="col-md-12">
        <MultipleSelect
          v-if="errors && errors.countries"
          v-model="countries"
          :label="$t('auth.profile.countries')"
          :options="countriesOptions"
          :errors="errors.countries"
          id="id_countries"
          name="countries"
        />
        <MultipleSelect
          v-else
          v-model="countries"
          :label="$t('auth.profile.countries')"
          :options="countriesOptions"
          id="id_countries"
          name="countries"
        />
      </div>
      <div class="col-md-12">
        <MultipleSelect
          v-if="errors && errors.cities"
          v-model="cities"
          :label="$t('auth.profile.cities')"
          :options="citiesExtraOptions"
          :errors="errors.cities"
          id="id_cities"
          name="cities"
        />
        <MultipleSelect
          v-else
          v-model="cities"
          :label="$t('auth.profile.cities')"
          :options="citiesExtraOptions"
          id="id_cities"
          name="cities"
        />
      </div>
      <div class="col-md-12">
        <MultipleSelect
          v-if="errors && errors.languages"
          v-model="languages"
          :label="$t('auth.profile.languages')"
          :options="languagesOptions"
          :errors="errors.languages"
          id="id_languages"
          name="languages"
        />
        <MultipleSelect
          v-else
          v-model="languages"
          :label="$t('auth.profile.languages')"
          :options="languagesOptions"
          id="id_languages"
          name="languages"
        />
      </div>
      <div class="col-md-6">
        <BaseInput
          v-if="errors && errors.cost_work"
          v-model="costWork"
          :label="$t('auth.profile.cost_work')"
          :errors="errors.cost_work"
          id="id_cost_work"
          name="cost_work"
          type="number"
          min="0.00"
          step="0.01"
          required=""
        />
        <BaseInput
          v-else
          v-model="costWork"
          :label="$t('auth.profile.cost_work')"
          id="id_cost_work"
          name="cost_work"
          type="number"
          min="0.00"
          step="0.01"
          required=""
        />
        <div class="form-text">{{ $t('form_help.cost_work') }}</div>
      </div>
      <div class="col-md-6">
        <BaseInput
          v-if="errors && errors.number_hours"
          v-model="numberHours"
          :label="$t('auth.profile.number_hours')"
          :errors="errors.number_hours"
          id="id_number_hours"
          name="number_hours"
          type="number"
          min="0"
          required=""
        />
        <BaseInput
          v-else
          v-model="numberHours"
          :label="$t('auth.profile.number_hours')"
          id="id_number_hours"
          name="number_hours"
          type="number"
          min="0"
          required=""
        />
      </div>
      <div class="col-md-12">
        <BaseInput
          v-if="errors && errors.profile_url"
          v-model="profileURL"
          :label="$t('auth.profile.profile_url')"
          :errors="errors.profile_url"
          id="id_profile_url"
          name="profile_url"
          type="text"
          maxlength="64"
          required=""
        />
        <BaseInput
          v-else
          v-model="profileURL"
          :label="$t('auth.profile.profile_url')"
          id="id_profile_url"
          name="profile_url"
          type="text"
          maxlength="64"
          required=""
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

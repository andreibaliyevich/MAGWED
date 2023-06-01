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
const website = ref('')
const profileURL = ref('')
const rating = ref(0.0)
const proTime = ref(null)

const { roleTypeOptions } = useOptionsOfRoleTypes()
const { countryOptions } = useOptionsOfCountries()
const { cityOptions } = useOptionsOfCities(country)
const { cityOptionsExtra } = useOptionsOfCitiesExtra(countries)
const { languageOptions } = useOptionsOfLanguages()

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
    website.value = response.data.website
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
      'website': website.value,
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

watch(country, (newValue, oldValue) => {
  if (oldValue) {
    city.value = null
  }
})

watch(cityOptionsExtra, (newValue, oldValue) => {
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
          v-model="name"
          type="text"
          id="id_name"
          name="name"
          :label="$t('profile.name')"
          :errors="errors?.user?.name ? errors.user.name : []"
        />
      </div>
      <div class="col-md-6">
        <BaseSelect
          v-model="country"
          :options="countryOptions"
          id="id_country"
          name="country"
          :label="$t('profile.country')"
          :errors="errors?.user?.country ? errors.user.country : []"
        />
      </div>
      <div class="col-md-6">
        <BaseSelect
          v-model="city"
          :options="cityOptions"
          id="id_city"
          name="city"
          :label="$t('profile.city')"
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
          :label="$t('profile.phone')"
          :errors="errors?.user?.phone ? errors.user.phone : []"
        />
      </div>
      <div class="col-md-12">
        <SearchListInputMultipleSelect
          v-model="roles"
          :options="roleTypeOptions"
          id="id_roles"
          name="roles"
          :label="$t('profile.roles')"
          :errors="errors?.roles ? errors.roles : []"
        />
      </div>
      <div class="col-md-12">
        <BaseTextarea
          v-model="description"
          id="id_description"
          name="description"
          :label="$t('profile.description')"
          :errors="errors?.description ? errors.description : []"
        />
      </div>
      <div class="col-md-12">
        <SearchListInputMultipleSelect
          v-model="countries"
          :options="countryOptions"
          id="id_countries"
          name="countries"
          :label="$t('profile.countries')"
          :errors="errors?.countries ? errors.countries : []"
        />
      </div>
      <div class="col-md-12">
        <SearchListInputMultipleSelect
          v-model="cities"
          :options="cityOptionsExtra"
          id="id_cities"
          name="cities"
          :label="$t('profile.cities')"
          :errors="errors?.cities ? errors.cities : []"
        />
      </div>
      <div class="col-md-12">
        <SearchListInputMultipleSelect
          v-model="languages"
          :options="languageOptions"
          id="id_languages"
          name="languages"
          :label="$t('profile.languages')"
          :errors="errors?.languages ? errors.languages : []"
        />
      </div>
      <div class="col-md-6">
        <BaseInput
          v-model="costWork"
          type="number"
          min="0.00"
          step="0.01"
          required=""
          id="id_cost_work"
          name="cost_work"
          :label="$t('profile.cost_work')"
          :errors="errors?.cost_work ? errors.cost_work : []"
        />
        <div class="form-text">{{ $t('form_help.cost_work') }}</div>
      </div>
      <div class="col-md-6">
        <BaseInput
          v-model="numberHours"
          type="number"
          min="0"
          required=""
          id="id_number_hours"
          name="number_hours"
          :label="$t('profile.number_hours')"
          :errors="errors?.number_hours ? errors.number_hours : []"
        />
      </div>
      <div class="col-md-12">
        <BaseInput
          v-model="website"
          type="url"
          maxlength="200"
          required=""
          id="id_website"
          name="website"
          :label="$t('profile.website')"
          :errors="errors?.website ? errors.website : []"
        />
      </div>
      <div class="col-md-12">
        <BaseInput
          v-model="profileURL"
          type="text"
          maxlength="64"
          required=""
          id="id_profile_url"
          name="profile_url"
          :label="$t('profile.profile_url')"
          :errors="errors?.profile_url ? errors.profile_url : []"
        />
      </div>
      <div class="col-12">
        <SubmitButton
          :loadingStatus="profileUpdating"
          buttonClass="btn btn-brand btn-lg"
        >
          {{ $t('profile.update_profile') }}
        </SubmitButton>
      </div>
    </form>
  </div>
</template>

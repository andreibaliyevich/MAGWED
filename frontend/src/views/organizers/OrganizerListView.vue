<script setup>
import axios from 'axios'
import { ref, computed, watch, onMounted } from 'vue'
import { useCurrency } from '@/composables/currency.js'
import { useOptionsOfRoleTypes } from '@/composables/optionsOfRoleTypes.js'
import { useOptionsOfCountries } from '@/composables/optionsOfCountries.js'
import { useOptionsOfCitiesExtra } from '@/composables/optionsOfCitiesExtra.js'
import { useOptionsOfLanguages } from '@/composables/optionsOfLanguages.js'
import { useCurrencyStore } from '@/stores/currency.js'

const currencyStore = useCurrencyStore()

const organizersLoading = ref(true)
const organizerList = ref([])
const nextURL = ref(null)

const roles = ref([])
const countries = ref([])
const cities = ref([])
const languages = ref([])
const costWorkMin = ref(80)
const costWorkMax = ref(150)

const { getValueInCurrency } = useCurrency()
const { roleTypesOptions } = useOptionsOfRoleTypes()
const { countriesOptions } = useOptionsOfCountries()
const { citiesExtraOptions } = useOptionsOfCitiesExtra(countries)
const { languagesOptions } = useOptionsOfLanguages()

const errors = ref(null)

const getOrganizers = async () => {
  organizersLoading.value = true
  
  let params = new URLSearchParams()
  roles.value.forEach((element) => params.append('roles', element))
  countries.value.forEach((element) => params.append('countries', element))
  cities.value.forEach((element) => params.append('cities', element))
  languages.value.forEach((element) => params.append('languages', element))
  if (costWorkMin.value !== null) {
    params.append('cost_work_min', costWorkMin.value)
  }
  if (costWorkMax.value !== null) {
    params.append('cost_work_max', costWorkMax.value)
  }

  try {
    const response = await axios.get('/accounts/organizers/', {
      params: params
    })
    organizerList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    organizersLoading.value = false
  }
}

const getMoreOrganizers = async () => {
  organizersLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    organizerList.value = [...organizerList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    organizersLoading.value = false
  }
}

watch(roles, () => getOrganizers())
watch(countries, () => getOrganizers())
watch(cities, () => getOrganizers())
watch(languages, () => getOrganizers())
watch(costWorkMin, () => getOrganizers())
watch(costWorkMax, () => getOrganizers())

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
  getOrganizers()
})
</script>

<template>
  <div class="organizer-list-view">
    <div class="container my-5">
      <div class="row g-5">
        <div class="col-lg-3 border border-light rounded-3 shadow-sm pt-3 pb-5">
          <CheckboxMultipleSelect
            v-model="roles"
            :options="roleTypesOptions"
            id="id_roles"
            name="roles"
            :label="$t('auth.profile.roles')"
            :errors="errors?.roles ? errors.roles : []"
          />
          <br>
          <CheckboxMultipleSelect
            v-model="countries"
            :options="countriesOptions"
            id="id_countries"
            name="countries"
            :label="$t('auth.profile.countries')"
            :errors="errors?.countries ? errors.countries : []"
          />
          <br v-if="countries.length > 0">
          <CheckboxMultipleSelect
            v-if="countries.length > 0"
            v-model="cities"
            :options="citiesExtraOptions"
            id="id_cities"
            name="cities"
            :label="$t('auth.profile.cities')"
            :errors="errors?.cities ? errors.cities : []"
          />
          <br>
          <CheckboxMultipleSelect
            v-model="languages"
            :options="languagesOptions"
            id="id_languages"
            name="languages"
            :label="$t('auth.profile.languages')"
            :errors="errors?.languages ? errors.languages : []"
          />
          <br>
          <NumberRangeInput
            v-model:minValue="costWorkMin"
            v-model:maxValue="costWorkMax"
            :min="80"
            :max="150"
            id="id_cost_work"
            name="cost_work"
            :label="$t('auth.profile.cost_work')"
            :minLabel="currencyStore.currencyText"
            :maxLabel="currencyStore.currencyText"
            :errors="errors?.cost_work ? errors.cost_work : []"
          />
        </div>
        <div class="col-lg-9">
          <div
            v-if="organizerList.length > 0"
            class="row"
          >
            <div
              v-for="organizer in organizerList"
              :key="organizer.user.uuid"
              class="col-12 col-sm-6 col-xl-4 text-center"
            >
              <UserAvatarExtended
                :src="organizer.user.avatar"
                :width="180"
                :height="180"
                :online="organizer.user.online"
              />
              <h2 class="fw-normal">{{ organizer.user.name }}</h2>
              <p>{{ currencyStore.currencyText }}{{ getValueInCurrency(organizer.cost_work) }}</p>
              <p><a class="btn btn-secondary" href="#">View details »</a></p>
            </div>
          </div>
          <div
            v-else
            class="lead fs-3 d-flex justify-content-center py-3"
          >
            {{ $t('organizer_list.no_organizers_available') }}
          </div>
          <div v-if="nextURL" v-intersection="getMoreOrganizers"></div>
          <LoadingIndicator v-if="organizersLoading" />
        </div>
      </div>
    </div>
  </div>
</template>

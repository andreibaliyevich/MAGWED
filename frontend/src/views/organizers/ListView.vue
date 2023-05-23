<script setup>
import axios from 'axios'
import { ref, computed, watch, onMounted } from 'vue'
import { useCurrencyConversion } from '@/composables/currencyConversion.js'
import { useOptionsOfRoleTypes } from '@/composables/optionsOfRoleTypes.js'
import { useOptionsOfCountries } from '@/composables/optionsOfCountries.js'
import { useOptionsOfCitiesExtra } from '@/composables/optionsOfCitiesExtra.js'
import { useOptionsOfLanguages } from '@/composables/optionsOfLanguages.js'
import { useCurrencyStore } from '@/stores/currency.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'

const currencyStore = useCurrencyStore()
const connectionBusStore = useConnectionBusStore()

const organizersLoading = ref(true)
const organizersMoreLoading = ref(false)
const organizerList = ref([])
const nextURL = ref(null)

const roles = ref([])
const countries = ref([])
const cities = ref([])
const languages = ref([])
const costWorkMin = ref(0)
const costWorkMax = ref(0)
const costWorkMinInCurrency = ref(0)
const costWorkMaxInCurrency = ref(0)

const { roleTypeOptions } = useOptionsOfRoleTypes()
const { countryOptions } = useOptionsOfCountries()
const { cityOptionsExtra } = useOptionsOfCitiesExtra(countries)
const { languageOptions } = useOptionsOfLanguages()
const { convertToCurrency } = useCurrencyConversion()

const filterSidebarButton = ref(null)

const costWorkMinBorder = computed(() => {
  return Math.floor(costWorkMin.value * currencyStore.conversionRate)
})
const costWorkMaxBorder = computed(() => {
  return Math.ceil(costWorkMax.value * currencyStore.conversionRate)
})

const getOrganizers = async () => {
  organizersLoading.value = true
  try {
    const response = await axios.get('/accounts/organizers/')
    organizerList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    organizersLoading.value = false
  }
}

const getFilteredOrganizers = async () => {
  organizersLoading.value = true

  let params = new URLSearchParams()
  roles.value.forEach((element) => params.append('roles', element))
  countries.value.forEach((element) => params.append('countries', element))
  cities.value.forEach((element) => params.append('cities', element))
  languages.value.forEach((element) => params.append('languages', element))
  if (costWorkMinInCurrency.value) {
    params.append('cost_work_min', Math.round(
      costWorkMinInCurrency.value / currencyStore.conversionRate
    ))
  }
  if (costWorkMaxInCurrency.value) {
    params.append('cost_work_max', Math.round(
      costWorkMaxInCurrency.value / currencyStore.conversionRate
    ))
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
    if (window.innerWidth < 992) {
      filterSidebarButton.value.click()
    }
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const getMoreOrganizers = async () => {
  organizersMoreLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    organizerList.value = [...organizerList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    organizersMoreLoading.value = false
  }
}

const getCostWorkMinMax = async () => {
  try {
    const response = await axios.get('/accounts/organizers/cost-work-min-max/')
    costWorkMin.value = response.data.cost_work_min
    costWorkMax.value = response.data.cost_work_max
    costWorkMinInCurrency.value = Math.floor(
      response.data.cost_work_min * currencyStore.conversionRate
    )
    costWorkMaxInCurrency.value = Math.ceil(
      response.data.cost_work_max * currencyStore.conversionRate
    )
  } catch (error) {
    console.error(error)
  }
}

const resetParamsAndGetOrganizers = () => {
  roles.value = []
  countries.value = []
  cities.value = []
  languages.value = []
  costWorkMinInCurrency.value = Math.floor(
    costWorkMin.value * currencyStore.conversionRate
  )
  costWorkMaxInCurrency.value = Math.ceil(
    costWorkMax.value * currencyStore.conversionRate
  )
  getOrganizers()
  if (window.innerWidth < 992) {
    filterSidebarButton.value.click()
  }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const updateUserStatus = (mutation, state) => {
  organizerList.value.forEach((element) => {
    if (element.user.uuid == state.user_uuid) {
      element.user.online = state.online
    }
  })
}

watch(cityOptionsExtra, (newValue, oldValue) => {
  if (newValue.length < oldValue.length) {
    let newCitiesValues = []
    newValue.forEach(element => newCitiesValues.push(element.value))
    cities.value = cities.value.filter((element) => {
      return newCitiesValues.includes(element)
    })
  }
})

watch(
  () => currencyStore.conversionRate,
  (newValue, oldValue) => {
    costWorkMinInCurrency.value = Math.round(
      costWorkMinInCurrency.value * newValue / oldValue
    )
    costWorkMaxInCurrency.value = Math.round(
      costWorkMaxInCurrency.value * newValue / oldValue
    )
  }
)

onMounted(() => {
  getOrganizers()
  getCostWorkMinMax()
  connectionBusStore.$subscribe(updateUserStatus)
})
</script>

<template>
  <div class="organizer-list-view">
    <div class="container my-5">
      <h1 class="display-6 text-center mb-5">
        {{ $t('nav.organizers') }}
      </h1>
      <div class="row">
        <div class="col-lg-3">
          <div class="border border-light rounded shadow-sm">
            <button
              ref="filterSidebarButton"
              type="button"
              class="btn btn-light border w-100 d-lg-none"
              data-bs-toggle="collapse"
              data-bs-target="#filter-sidebar"
              aria-expanded="false"
              aria-controls="filter-sidebar"
            >
              {{ $t('organizer_list.filters') }}
              <i class="fa-solid fa-caret-down ms-1"></i>
            </button>
            <div id="filter-sidebar" class="collapse px-3 d-lg-block">
              <br>
              <CheckboxMultipleSelect
                v-model="roles"
                :options="roleTypeOptions"
                id="id_roles"
                name="roles"
                :label="$t('profile.roles')"
              />
              <br>
              <CheckboxMultipleSelect
                v-model="countries"
                :options="countryOptions"
                id="id_countries"
                name="countries"
                :label="$t('profile.countries')"
              />
              <br v-if="countries.length > 0">
              <CheckboxMultipleSelect
                v-if="countries.length > 0"
                v-model="cities"
                :options="cityOptionsExtra"
                id="id_cities"
                name="cities"
                :label="$t('profile.cities')"
              />
              <br>
              <CheckboxMultipleSelect
                v-model="languages"
                :options="languageOptions"
                id="id_languages"
                name="languages"
                :label="$t('profile.languages')"
              />
              <br>
              <NumberRangeInput
                v-model:minValue="costWorkMinInCurrency"
                v-model:maxValue="costWorkMaxInCurrency"
                :min="costWorkMinBorder"
                :max="costWorkMaxBorder"
                id="id_cost_work"
                name="cost_work"
                :label="$t('profile.cost_work')"
                :minLabel="currencyStore.currencyText"
                :maxLabel="currencyStore.currencyText"
              />
              <br>
              <div class="d-flex justify-content-end">
                <button
                  @click="resetParamsAndGetOrganizers()"
                  type="button"
                  class="btn btn-light btn-sm"
                  :disabled="
                    !roles.length
                    && !countries.length
                    && !cities.length
                    && !languages.length
                    && (costWorkMinInCurrency == costWorkMinBorder)
                    && (costWorkMaxInCurrency == costWorkMaxBorder)
                  "
                >
                  {{ $t('organizer_list.reset') }}
                </button>
                <button
                  @click="getFilteredOrganizers()"
                  type="button"
                  class="btn btn-brand btn-sm ms-1"
                  :disabled="
                    !roles.length
                    && !countries.length
                    && !cities.length
                    && !languages.length
                    && (costWorkMinInCurrency == costWorkMinBorder)
                    && (costWorkMaxInCurrency == costWorkMaxBorder)
                  "
                >
                  {{ $t('organizer_list.show') }}
                </button>
              </div>
              <br>
            </div>
          </div>
        </div>
        <div class="col-lg-9 mt-5 mt-lg-0">
          <LoadingIndicator v-if="organizersLoading" />
          <div
            v-else-if="organizerList.length > 0"
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
              <p>{{ currencyStore.currencyText }}{{ convertToCurrency(organizer.cost_work) }}</p>
              <p>
                <LocaleRouterLink
                  routeName="OrganizerDetail"
                  :routeParams="{ profile_url: organizer.user.profile_url }"
                  class="btn btn-secondary"
                >
                  View details »
                </LocaleRouterLink>
              </p>
            </div>
            <div v-if="nextURL" v-intersection="getMoreOrganizers"></div>
            <LoadingIndicator v-if="organizersMoreLoading" />
          </div>
          <div
            v-else
            class="lead fs-3 d-flex justify-content-center py-3"
          >
            {{ $t('organizer_list.no_organizers_available') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

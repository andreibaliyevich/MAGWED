<script setup>
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCurrencyConversion } from '@/composables/currencyConversion.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useCurrencyStore } from '@/stores/currency.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import NotFound from '@/components/NotFound.vue'

const route = useRoute()
const currencyStore = useCurrencyStore()
const connectionBusStore = useConnectionBusStore()

const organizerLoading = ref(true)
const organizerData = ref({
  user: {
      uuid: '',
      email: '',
      name: '',
      avatar: null,
      country: null,
      city: null,
      phone: '',
      online: false
  },
  roles: [],
  cover: null,
  description: '',
  countries: [],
  cities: [],
  languages: [],
  cost_work: 0.0,
  number_hours: 0,
  website: '',
  rating: 0.0
})

const errorStatus = ref(null)

const { convertToCurrency } = useCurrencyConversion()
const { getLocaleDateString } = useLocaleDateTime()

const organizerWebsiteShort = computed(() => {
  return organizerData.value.website.split('://')[1]
})

const getOrganizerData = async () => {
  organizerLoading.value = true
  try {
    const response = await axios.get(
      '/accounts/organizers/'
      + route.params.profile_url
      + '/'
    )
    organizerData.value = response.data
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    organizerLoading.value = false
  }
}

const updateUserStatus = (mutation, state) => {
  if (organizerData.value.user.uuid == state.user_uuid) {
    organizerData.value.user.online = state.online
  }
}

onMounted(() => {
  getOrganizerData()
  connectionBusStore.$subscribe(updateUserStatus)
})
</script>

<template>
  <div class="organizer-detail-view">
    <LoadingIndicator
      v-if="organizerLoading"
      class="my-5"
    />
    <NotFound v-else-if="errorStatus == 404" />
    <div
      v-else
      class="container my-5"
    >
      <div class="card">
        <img
          v-if="organizerData.cover"
          :src="organizerData.cover"
          class="card-img-top"
        >
        <img
          v-else
          src="/cover.jpg"
          class="card-img-top"
        >
        <div class="d-lg-flex align-items-start text-center mx-3 mx-lg-5 mb-3">
          <div class="position-relative" style="margin-top: -5rem;">
            <UserAvatarExtended
              :src="organizerData.user.avatar"
              :width="180"
              :height="180"
              :online="organizerData.user.online"
              class="border border-light border-3"
            />
          </div>
          <div class="d-sm-inline-block mt-3 ms-lg-3">
            <h1 class="h3">{{ organizerData.user.name }}</h1>
            <div class="row g-1">
              <div
                v-for="roleValue in organizerData.roles"
                :key="roleValue"
                class="col"
              >
                <span class="badge text-bg-light">
                  {{ $t(`roles.${roleValue}`) }}
                </span>
              </div>
            </div>
          </div>
          <div class="d-flex justify-content-center mt-3 ms-lg-auto">
            <button
              type="button"
              class="btn btn-outline-brand"
            >
              <i class="fa-solid fa-user-plus"></i>
              Follow
            </button>
            <button
              type="button"
              class="btn btn-light ms-2"
            >
              <i class="fa-solid fa-pen"></i>
              Write
            </button>
          </div>
        </div>
        <ul class="list-inline text-center text-lg-start mx-3 mx-lg-5 mb-3">
          <li class="list-inline-item me-3">
            <i class="fa-regular fa-calendar-plus me-1"></i>
            {{ $t('profile.joined_on') }}
            {{ getLocaleDateString(organizerData.user.date_joined) }}
          </li>
          <li
            v-if="organizerData.user.city"
            class="list-inline-item me-3"
          >
            <i class="fa-solid fa-location-dot me-1"></i>
            {{ $t(`cities.${organizerData.user.city}`) }},
            {{ $t(`countries.${organizerData.user.country}`) }}
          </li>
          <li
            v-if="organizerData.user.phone"
            class="list-inline-item me-3"
          >
            <i class="fa-solid fa-phone me-1"></i>
            <a
              :href="`tel:${organizerData.user.phone}`"
              class="text-decoration-none link-dark"
            >
              {{ organizerData.user.phone }}
            </a>
          </li>
          <li
            v-if="organizerData.website"
            class="list-inline-item"
          >
            <i class="fa-solid fa-globe me-1"></i>
            <a
              :href="organizerData.website"
              target="_blank"
              class="text-decoration-none link-dark"
            >
              {{ organizerWebsiteShort }}
            </a>
          </li>
        </ul>
      </div>
      <div class="card mt-3 py-3 px-3 px-lg-5">
        <p
          v-if="organizerData.description"
          class="lead"
        >
          {{ organizerData.description }}
        </p>
        <ul class="list-group list-group-flush">
          <li
            v-if="organizerData.countries.length"
            class="list-group-item"
          >
            <i class="fa-solid fa-earth-europe"></i>
            {{ $t('profile.countries') }}:
            <span
              v-for="countryValue in organizerData.countries"
              :key="countryValue"
              class="badge text-bg-light fw-normal ms-1"
            >
              {{ $t(`countries.${countryValue}`) }}
            </span>
          </li>
          <li
            v-if="organizerData.cities.length"
            class="list-group-item"
          >
            <i class="fa-solid fa-city"></i>
            {{ $t('profile.cities') }}:
            <span
              v-for="cityValue in organizerData.cities"
              :key="cityValue"
              class="badge text-bg-light fw-normal ms-1"
            >
              {{ $t(`cities.${cityValue}`) }}
            </span>
          </li>
          <li
            v-if="organizerData.languages.length"
            class="list-group-item"
          >
            <i class="fa-solid fa-language"></i>
            {{ $t('profile.languages') }}:
            <span
              v-for="languageValue in organizerData.languages"
              :key="languageValue"
              class="badge text-bg-light fw-normal ms-1"
            >
              {{ $t(`languages.${languageValue}`) }}
            </span>
          </li>
          <li
            v-if="organizerData.cost_work"
            class="list-group-item"
          >
            <i class="fa-solid fa-money-bills"></i>
            {{ $t('profile.cost_work') }}:
            {{ currencyStore.currencyText }}{{ convertToCurrency(organizerData.cost_work) }}
          </li>
          <li
            v-if="organizerData.number_hours"
            class="list-group-item"
          >
            <i class="fa-solid fa-clock"></i>
            {{ $t('profile.number_hours') }}:
            {{ organizerData.number_hours }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCurrencyConversion } from '@/composables/currencyConversion.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'

const route = useRoute()
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
  rating: 0.0
})

const { convertToCurrency } = useCurrencyConversion()
const { getLocaleDateString } = useLocaleDateTime()

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
    console.error(error)
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
  <div class="organizer-list-view">
    <LoadingIndicator
      v-if="organizerLoading"
      class="my-5"
    />
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
          <div class="d-sm-inline-block mt-3 ms-sm-3">
            <h1 class="h3">{{ organizerData.user.name }}</h1>
            <div class="row g-1">
              <div
                v-for="roleValue in organizerData.roles"
                :key="roleValue"
                class="col"
              >
                <span
                  v-if="roleValue==1"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.photographer') }}
                </span>
                <span
                  v-else-if="roleValue==2"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.videographer') }}
                </span>
                <span
                  v-else-if="roleValue==3"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.leading') }}
                </span>
                <span
                  v-else-if="roleValue==4"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.musician') }}
                </span>
                <span
                  v-else-if="roleValue==5"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.dj') }}
                </span>
                <span
                  v-else-if="roleValue==6"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.agency') }}
                </span>
                <span
                  v-else-if="roleValue==7"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.salon') }}
                </span>
                <span
                  v-else-if="roleValue==8"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.confectionery') }}
                </span>
                <span
                  v-else-if="roleValue==9"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.decorator') }}
                </span>
                <span
                  v-else-if="roleValue==10"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.visagiste') }}
                </span>
                <span
                  v-else-if="roleValue==11"
                  class="badge text-bg-light"
                >
                  {{ $t('roles.hairdresser') }}
                </span>
              </div>
            </div>
          </div>
          <div class="d-flex justify-content-center mt-3 ms-sm-auto">
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
        <ul class="list-inline text-lg-start text-center mx-3 mx-lg-5 mb-3">
          <li class="list-inline-item">
            <i class="fa-regular fa-calendar-plus"></i>
            {{ getLocaleDateString(organizerData.user.date_joined) }}
          </li>
          <li
            v-if="organizerData.user.city"
            class="list-inline-item"
          >
            <i class="fa-solid fa-location-dot me-1"></i>
            {{ organizerData.user.city.name_local }} ({{ organizerData.user.city.name }}),
            {{ organizerData.user.country.name_local }} ({{ organizerData.user.country.name }})
          </li>
          <li
            v-if="organizerData.user.phone"
            class="list-inline-item"
          >
            <i class="fa-solid fa-phone me-1"></i>
            <a
              :href="`tel:${organizerData.user.phone}`"
              class="text-decoration-none link-dark"
            >
              {{ organizerData.user.phone }}
            </a>
          </li>
        </ul>
      </div>
      <div class="card mt-3 py-3 px-5">
        <p
          v-if="organizerData.description"
          class="lead"
        >
          {{ organizerData.description }}
        </p>
        <ul class="list-group list-group-flush">
          <li
            v-if="organizerData.cost_work"
            class="list-group-item"
          >
            {{ $t('auth.profile.cost_work') }}: {{ organizerData.cost_work }}
          </li>
          <li
            v-if="organizerData.number_hours"
            class="list-group-item"
          >
            {{ $t('auth.profile.number_hours') }}: {{ organizerData.number_hours }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

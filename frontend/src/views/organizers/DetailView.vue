<script setup>
import axios from 'axios'
import { useRoute } from 'vue-router'
import { ref, computed, watch, onMounted } from 'vue'
import { useCurrencyStore } from '@/stores/currency.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import AlbumList from '@/components/organizers/AlbumList.vue'
import PhotoList from '@/components/organizers/PhotoList.vue'
import ReviewList from '@/components/organizers/ReviewList.vue'
import NotFound from '@/components/NotFound.vue'

const route = useRoute()
const currencyStore = useCurrencyStore()
const userStore = useUserStore()
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
    date_joined: null,
    status: null,
    following: null
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

const messageSending = ref(false)
const textContent = ref('')

const mediaDataTab = ref('photos')

const { getLocaleDateString, getLocaleDateTimeString } = useLocaleDateTime()

const errors = ref(null)
const errorStatus = ref(null)

const writeMessageModal = ref(null)
const writeMessageModalBootstrap = ref(null)

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
  if (organizerData.value.user.uuid === state.user_uuid) {
    organizerData.value.user.status = state.status
  }
}

const followUser = async () => {
  try {
    const response = await axios.post(
      '/social/follow/user/'
        + organizerData.value.user.uuid
        + '/'
    )
    organizerData.value.user.following = true
  } catch (error) {
    console.error(error)
  }
}

const unfollowUser = async () => {
  try {
    const response = await axios.delete(
      '/social/follow/user/'
        + organizerData.value.user.uuid
        + '/'
    )
    organizerData.value.user.following = false
  } catch (error) {
    console.error(error)
  }
}

const writeMessage = async () => {
  messageSending.value = true
  try {
    const response = await axios.post(
      '/messenger/message/write/'
        + organizerData.value.user.uuid
        + '/',
      { content: textContent.value }
    )
    writeMessageModalBootstrap.value.hide()
  } catch (error) {
    errors.value = error.response.data
  } finally {
    messageSending.value = false
  }
}

watch(
  () => route.params.profile_url,
  (newValue) => {
    if (route.name === 'OrganizerDetail') {
      getOrganizerData()
    }
  }
)

onMounted(() => {
  getOrganizerData()
  connectionBusStore.$subscribe(updateUserStatus)
  writeMessageModal.value.addEventListener('hidden.bs.modal', () => {
    textContent.value = ''
  })
  writeMessageModalBootstrap.value = new bootstrap.Modal(
    writeMessageModal.value
  )
})
</script>

<template>
  <div class="organizer-detail-view">
    <LoadingIndicator
      v-if="organizerLoading"
      class="my-5"
    />
    <NotFound v-else-if="errorStatus === 404" />
    <div
      v-else
      class="container my-5"
    >
      <div class="card border border-light shadow-sm">
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
        <div class="d-lg-flex align-items-lg-start text-center mx-3 mx-lg-5 mb-3">
          <div class="position-relative" style="margin-top: -5rem;">
            <UserAvatar
              :src="organizerData.user.avatar"
              :width="180"
              :height="180"
              class="border border-light border-3"
            />
          </div>
          <div class="d-inline-block mt-3 ms-lg-3">
            <h1 class="h3">{{ organizerData.user.name }}</h1>
            <span
              v-if="organizerData.user.status === 'online'"
              class="text-dark"
            >
              <i class="fa-solid fa-circle fa-xs text-success"></i>
              {{ $t('user.online') }}
            </span>
            <span
              v-else
              class="text-secondary"
            >
              <i class="fa-solid fa-circle fa-xs"></i>
              {{ $t('user.last_visit') }}
              {{ getLocaleDateTimeString(organizerData.user.status) }}
            </span>
            <div class="row g-1 mt-1">
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
          <div
            v-if="userStore.isLoggedIn && userStore.uuid != organizerData.user.uuid"
            class="d-flex justify-content-center mt-3 ms-lg-auto"
          >
            <button
              v-if="organizerData.user.following"
              @click="unfollowUser()"
              type="button"
              class="btn btn-brand"
            >
              <i class="fa-solid fa-user-minus"></i>
              {{ $t('follow.unfollow') }}
            </button>
            <button
              v-else
              @click="followUser()"
              type="button"
              class="btn btn-outline-brand"
            >
              <i class="fa-solid fa-user-plus"></i>
              {{ $t('follow.follow') }}
            </button>
            <button
              type="button"
              class="btn btn-light ms-2"
              data-bs-toggle="modal"
              data-bs-target="#write_message_modal"
            >
              <i class="fa-solid fa-pen"></i>
              {{ $t('messenger.write') }}
            </button>
          </div>
        </div>
        <ul class="list-inline text-center text-lg-start mx-3 mx-lg-5 mb-4">
          <li class="list-inline-item">
            <i class="fa-regular fa-calendar-plus me-1"></i>
            {{ $t('user.joined_on') }}
            {{ getLocaleDateString(organizerData.user.date_joined) }}
          </li>
          <li
            v-if="organizerData.user.city"
            class="list-inline-item ms-3"
          >
            <i class="fa-solid fa-location-dot me-1"></i>
            {{ $t(`cities.${organizerData.user.city}`) }},
            {{ $t(`countries.${organizerData.user.country}`) }}
          </li>
          <li
            v-else-if="organizerData.user.country"
            class="list-inline-item ms-3"
          >
            <i class="fa-solid fa-location-dot me-1"></i>
            {{ $t(`countries.${organizerData.user.country}`) }}
          </li>
          <li
            v-if="organizerData.user.phone"
            class="list-inline-item ms-3"
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
            class="list-inline-item ms-3"
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

      <div class="card border border-light shadow-sm mt-3 py-4 px-3 px-lg-5">
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
            {{ $t('user.countries') }}:
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
            {{ $t('user.cities') }}:
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
            {{ $t('user.languages') }}:
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
            {{ $t('user.cost_work') }}:
            {{ currencyStore.currencyText }}{{ currencyStore.convertCurrency(organizerData.cost_work) }}
          </li>
          <li
            v-if="organizerData.number_hours"
            class="list-group-item"
          >
            <i class="fa-solid fa-clock"></i>
            {{ $t('user.number_hours') }}:
            {{ organizerData.number_hours }}
          </li>
        </ul>
      </div>

      <div class="d-flex justify-content-center mt-5">
        <div
          role="group"
          class="btn-group"
          aria-label="Media Data Tab"
        >
          <input
            v-model="mediaDataTab"
            value="photos"
            id="id_radio_tab_photos"
            name="radio_tab"
            type="radio"
            class="btn-check"
          >
          <label
            for="id_radio_tab_photos"
            class="btn btn-outline-dark"
          >
            {{ $t('portfolio.photos') }}
          </label>

          <input
            v-model="mediaDataTab"
            value="albums"
            id="id_radio_tab_albums"
            name="radio_tab"
            type="radio"
            class="btn-check"
          >
          <label
            for="id_radio_tab_albums"
            class="btn btn-outline-dark"
          >
            {{ $t('portfolio.photo_albums') }}
          </label>

          <input
            v-model="mediaDataTab"
            value="reviews"
            id="id_radio_tab_reviews"
            name="radio_tab"
            type="radio"
            class="btn-check"
          >
          <label
            for="id_radio_tab_reviews"
            class="btn btn-outline-dark"
          >
            {{ $t('reviews.reviews') }}
          </label>
        </div>
      </div>

      <div v-if="mediaDataTab === 'photos'">
        <PhotoList :userUUID="organizerData.user.uuid" />
      </div>
      <div v-else-if="mediaDataTab === 'albums'">
        <AlbumList :userUUID="organizerData.user.uuid" />
      </div>
      <div v-else-if="mediaDataTab === 'reviews'">
        <ReviewList :userUUID="organizerData.user.uuid" />
      </div>

    </div>

    <Teleport to="body">
      <div
        ref="writeMessageModal"
        id="write_message_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="write_message_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="write_message_modal_label"
                class="modal-title"
              >
                {{ $t('messenger.new_message') }}
              </h5>
              <button
                class="btn-close"
                type="button"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form
                @submit.prevent="writeMessage()"
                id="write_message_modal_form"
              >
                <BaseTextarea
                  v-model="textContent"
                  id="id_content"
                  name="content"
                  :label="$t('messenger.content')"
                  :errors="
                    errors?.content
                    ? errors.content
                    : []
                  "
                />
              </form>
            </div>
            <div class="modal-footer">
              <button
                class="btn btn-light"
                type="button"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.cancel') }}
              </button>
              <SubmitButton
                :loadingStatus="messageSending"
                buttonClass="btn btn-brand"
                form="write_message_modal_form"
                :disabled="!textContent"
              >
                {{ $t('btn.send') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

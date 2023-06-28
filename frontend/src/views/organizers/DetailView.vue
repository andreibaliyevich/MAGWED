<script setup>
import axios from 'axios'
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCurrencyConversion } from '@/composables/currencyConversion.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useCurrencyStore } from '@/stores/currency.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import WriteReview from '@/components/organizers/WriteReview.vue'
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
    online: null,
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

const mediaDataTab = ref('photos')
const mediaDataLoading = ref(true)
const mediaDataMoreLoading = ref(false)
const mediaDataList = ref([])
const nextURL = ref(null)

const errorStatus = ref(null)

const { convertToCurrency } = useCurrencyConversion()
const { getLocaleDateString, getLocaleDateTimeString } = useLocaleDateTime()

const organizerWebsiteShort = computed(() => {
  return organizerData.value.website.split('://')[1]
})

const getOrganizerPhotos = async () => {
  mediaDataList.value = []
  try {
    const response = await axios.get(
      '/portfolio/photos/list/'
        + '?owner='
        + organizerData.value.user.uuid
        + '&album_is_null=true'
    )
    mediaDataList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    mediaDataLoading.value = false
  }
}

const getOrganizerAlbums = async () => {
  mediaDataList.value = []
  try {
    const response = await axios.get(
      '/portfolio/albums/list/'
        + '?owner='
        + organizerData.value.user.uuid
    )
    mediaDataList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    mediaDataLoading.value = false
  }
}

const getOrganizerReviews = async () => {
  mediaDataList.value = []
  try {
    const response = await axios.get(
      '/social/reviews/'
        + '?user='
        + organizerData.value.user.uuid
    )
    mediaDataList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    mediaDataLoading.value = false
  }
}

const getMoreOrganizerMedia = async () => {
  mediaDataMoreLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    mediaDataList.value = [...mediaDataList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    mediaDataMoreLoading.value = false
  }
}

const getOrganizerData = async () => {
  try {
    const response = await axios.get(
      '/accounts/organizers/'
        + route.params.profile_url
        + '/'
    )
    organizerData.value = response.data
    getOrganizerPhotos()
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

const followUser = async () => {
  try {
    const response = await axios.post('/social/follow/', {
      'uuid': organizerData.value.user.uuid
    })
    organizerData.value.user.following = true
  } catch (error) {
    console.error(error)
  }
}

const unfollowUser = async () => {
  try {
    const response = await axios.delete('/social/follow/', {
      data: {
        'uuid': organizerData.value.user.uuid
      }
    })
    organizerData.value.user.following = false
  } catch (error) {
    console.error(error)
  }
}

watch(mediaDataTab, (newValue) => {
  if (newValue == 'photos') {
    getOrganizerPhotos()
  } else if (newValue == 'albums') {
    getOrganizerAlbums()
  }
   else if (newValue == 'reviews') {
    getOrganizerReviews()
  }
})

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
          <div class="d-inline-block mt-3 ms-lg-3">
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
              Unfollow
            </button>
            <button
              v-else
              @click="followUser()"
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
        <ul class="list-inline text-center text-lg-start mx-3 mx-lg-5 mb-4">
          <li class="list-inline-item">
            <i class="fa-regular fa-calendar-plus me-1"></i>
            {{ $t('profile.joined_on') }}
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

      <div class="d-flex justify-content-center mt-5">
        <div
          role="group"
          class="btn-group"
          aria-label="Basic radio toggle button group"
        >
          <input
            v-model="mediaDataTab"
            id="id_radio_tab_photos"
            name="radio_tab_photos"
            type="radio"
            value="photos"
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
            id="id_radio_tab_albums"
            name="radio_tab_albums"
            type="radio"
            value="albums"
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
            id="id_radio_tab_reviews"
            name="radio_tab_reviews"
            type="radio"
            value="reviews"
            class="btn-check"
          >
          <label
            for="id_radio_tab_reviews"
            class="btn btn-outline-dark"
          >
            {{ $t('organizers.reviews') }}
          </label>
        </div>
      </div>

      <LoadingIndicator v-if="mediaDataLoading" />

      <div v-else-if="mediaDataTab == 'photos'">
        <div
          v-if="mediaDataList.length > 0"
          class="row g-3 mt-3"
        >
          <div
            v-for="mediaDataItem in mediaDataList"
            :key="mediaDataItem.uuid"
            class="col-12 col-md-6 col-lg-4 col-xl-3"
          >
            <div class="card border border-0 h-100">
              <LocaleRouterLink
                routeName="PhotoDetail"
                :routeParams="{ uuid: mediaDataItem.uuid }"
                :routeQuery="{ from: this.$route.query.filter }"
                class="link-light"
              >
                <img
                  :src="mediaDataItem.thumbnail"
                  class="card-img"
                >
                <div class="card-img-overlay">
                  <div class="position-absolute top-0 start-50 translate-middle-x mt-2">
                    <h5 class="card-title text-center">{{ mediaDataItem.title }}</h5>
                  </div>
                  <div class="position-absolute bottom-0 start-0 ms-2 mb-2">
                    <i class="fa-regular fa-eye"></i>
                    {{ mediaDataItem.num_views }}
                  </div>
                  <div class="position-absolute bottom-0 start-50 translate-middle-x mb-2">
                    <i class="fa-regular fa-heart"></i>
                    {{ mediaDataItem.likes_count }}
                  </div>
                  <div class="position-absolute bottom-0 end-0 me-2 mb-2">
                    <i class="fa-regular fa-star"></i>
                    {{ mediaDataItem.rating }}
                  </div>
                </div>
              </LocaleRouterLink>
            </div>
          </div>
          <div v-if="nextURL" v-intersection="getMoreOrganizerMedia"></div>
          <LoadingIndicator v-if="mediaDataMoreLoading" />
        </div>
        <div
          v-else
          class="lead d-flex justify-content-center py-3"
        >
          {{ $t('portfolio.no_photos') }}
        </div>
      </div>

      <div v-else-if="mediaDataTab == 'albums'">
        <div
          v-if="mediaDataList.length > 0"
          class="row g-3 mt-3"
        >
          <div
            v-for="mediaDataItem in mediaDataList"
            :key="mediaDataItem.uuid"
            class="col-12 col-md-6 col-lg-4 col-xl-3"
          >
            <div class="card border border-light shadow-sm h-100">
              <LocaleRouterLink
                routeName="AlbumDetail"
                :routeParams="{ uuid: mediaDataItem.uuid }"
              >
                <img
                  :src="mediaDataItem.thumbnail"
                  :alt="mediaDataItem.title"
                  class="card-img-top"
                >
              </LocaleRouterLink>
              <div class="card-body">
                <LocaleRouterLink
                  routeName="AlbumDetail"
                  :routeParams="{ uuid: mediaDataItem.uuid }"
                  class="text-decoration-none link-dark"
                >
                  <h5 class="card-title">{{ mediaDataItem.title }}</h5>
                </LocaleRouterLink>
                <div class="d-flex justify-content-between mt-1">
                  <div>
                    <i class="fa-regular fa-eye"></i>
                    {{ mediaDataItem.num_views }}
                  </div>
                  <div>
                    <i class="fa-regular fa-heart"></i>
                    {{ mediaDataItem.likes_count }}
                  </div>
                  <div>
                    <i class="fa-regular fa-star"></i>
                    {{ mediaDataItem.rating }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="nextURL" v-intersection="getMoreOrganizerMedia"></div>
          <LoadingIndicator v-if="mediaDataMoreLoading" />
        </div>
        <div
          v-else
          class="lead d-flex justify-content-center py-3"
        >
          {{ $t('portfolio.no_albums') }}
        </div>
      </div>

      <div v-else-if="mediaDataTab == 'reviews'">
        <div class="row flex-lg-row-reverse g-5 mt-3">
          <div class="col-lg-6">
            <WriteReview
              v-if="userStore.isLoggedIn"
              :userUUID="organizerData.user.uuid"
              @reviewCreated="(review) => mediaDataList.unshift(review)"
            />
            <div
              v-else
              class="alert alert-info" role="alert"
            >
              {{ $t('organizers.need_log_in') }}
              <LocaleRouterLink
                routeName="Login"
                :routeQuery="{ redirect: this.$route.path }"
                class="alert-link"
              >
                {{ $t('auth.log_in') }}
              </LocaleRouterLink>
            </div>
          </div>
          <div
            v-if="mediaDataList.length > 0"
            class="col-lg-6"
          >
            <TransitionGroup
              tag="ul"
              name="list-group"
              class="list-group list-group-flush"
            >
              <li
                v-for="mediaDataItem in mediaDataList"
                :key="mediaDataItem.uuid"
                class="list-group-item"
              >
                <div
                  v-if="mediaDataItem.author"
                  class="d-flex gap-3 py-3"
                >
                  <LocaleRouterLink
                    v-if="mediaDataItem.author.profile_url"
                    routeName="OrganizerDetail"
                    :routeParams="{ profile_url: mediaDataItem.author.profile_url }"
                  >
                    <UserAvatarExtended
                      :src="mediaDataItem.author.avatar"
                      :width="48"
                      :height="48"
                      :online="mediaDataItem.author.online"
                    />
                  </LocaleRouterLink>
                  <UserAvatarExtended
                    v-else
                    :src="mediaDataItem.author.avatar"
                    :width="48"
                    :height="48"
                    :online="mediaDataItem.author.online"
                  />
                  <div class="flex-grow-1 ms-1">
                    <div class="d-flex justify-content-between">
                      <LocaleRouterLink
                        v-if="mediaDataItem.author.profile_url"
                        routeName="OrganizerDetail"
                        :routeParams="{ profile_url: mediaDataItem.author.profile_url }"
                        class="text-decoration-none link-dark"
                      >
                        <strong class="mb-0">
                          {{ mediaDataItem.author.name }}
                        </strong>
                      </LocaleRouterLink>
                      <strong
                        v-else
                        class="mb-0"
                      >
                        {{ mediaDataItem.author.name }}
                      </strong>
                      <small>
                        {{ getLocaleDateTimeString(mediaDataItem.created_at) }}
                      </small>
                    </div>
                    <div v-if="mediaDataItem.rating == 1">
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-regular fa-star"></i>
                      <i class="fa-regular fa-star"></i>
                      <i class="fa-regular fa-star"></i>
                      <i class="fa-regular fa-star"></i>
                    </div>
                    <div v-else-if="mediaDataItem.rating == 2">
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-regular fa-star"></i>
                      <i class="fa-regular fa-star"></i>
                      <i class="fa-regular fa-star"></i>
                    </div>
                    <div v-else-if="mediaDataItem.rating == 3">
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-regular fa-star"></i>
                      <i class="fa-regular fa-star"></i>
                    </div>
                    <div v-else-if="mediaDataItem.rating == 4">
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-regular fa-star"></i>
                    </div>
                    <div v-else-if="mediaDataItem.rating == 5">
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                    </div>
                  </div>
                </div>
                <p>{{ mediaDataItem.comment }}</p>
              </li>
            </TransitionGroup>
            <div v-if="nextURL" v-intersection="getMoreOrganizerMedia"></div>
            <LoadingIndicator v-if="mediaDataMoreLoading" />
          </div>
          <div
            v-else
            class="col-lg-6 lead d-flex justify-content-center py-3"
          >
            {{ $t('organizers.no_reviews') }}
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.list-group-enter-active,
.list-group-leave-active {
  transition: all 0.5s;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
}
.list-group-enter-from,
.list-group-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style>

<script setup>
import axios from 'axios'

import ProfileAvatar from '@/components/auth/ProfileAvatar.vue'
import ProfileCover from '@/components/auth/ProfileCover.vue'
import BaseInput from '@/components/UI/BaseInput.vue'

import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<script>
export default {
  data() {
    return {
      pageLoading: 0,
      name: '',
      country: null,
      city: null,
      phone: '',
      dateOfWedding: null,
      roles: [],
      description: '',
      countries: [],
      cities: [],
      languages: [],
      costWork: 0.00,
      numberHours: 0,
      profileURL: '',
      rating: 0.0,
      proTime: null,
      countriesList: [],
      citiesList1: [],
      citiesList2: [],
      languagesList: [],
      status: null,
      errors: null
    }
  },
  methods: {
    async getProfileData() {
      try {
        const response = await axios.get('/' + this.$i18n.locale + '/accounts/auth/profile/')
        if (this.userStore.userType == 1) {
          this.name = response.data.name
          this.country = response.data.country
          this.city = response.data.city
          this.phone = response.data.phone
        } else if (this.userStore.userType == 2) {
          this.name = response.data.user.name
          this.country = response.data.user.country
          this.city = response.data.user.city
          this.phone = response.data.user.phone
          this.dateOfWedding = response.data.date_of_wedding
        } else if (this.userStore.userType == 3) {
          this.name = response.data.user.name
          this.country = response.data.user.country
          this.city = response.data.user.city
          this.phone = response.data.user.phone
          this.roles = response.data.roles
          this.cover = response.data.cover
          this.description = response.data.description
          this.countries = response.data.countries
          this.cities = response.data.cities
          this.languages = response.data.languages
          this.costWork = response.data.cost_work
          this.numberHours = response.data.number_hours
          this.profileURL = response.data.profile_url
          this.rating = response.data.rating
          this.proTime = response.data.pro_time
        }
      } catch (error) {
        this.errors = error.response.data
      } finally {
        this.pageLoading++
      }
    },
    async getCountriesData() {
      try {
        const response = await axios.get('/' + this.$i18n.locale + '/main/countries/')
        this.countriesList = response.data
      } catch (error) {
        this.errors = error.response.data
      } finally {
        this.pageLoading++
      }
    },
    async getLanguagesData() {
      try {
        const response = await axios.get('/' + this.$i18n.locale + '/main/languages/')
        this.languagesList = response.data
      } catch (error) {
        this.errors = error.response.data
      } finally {
        this.pageLoading++
      }
    },
    updateProfile() {
      this.status = null
      this.errors = null

      if (!this.country) {
        this.country = null
      }
      if (!this.city) {
        this.city = null
      }
      if (!this.dateOfWedding) {
        this.dateOfWedding = null
      }

      let data = {}
      if (this.userStore.userType == 1) {
        data = {
          'name': this.name,
          'country': this.country,
          'city': this.city,
          'phone': this.phone
        }
      } else if (this.userStore.userType == 2) {
        data = {
          'user': {
            'name': this.name,
            'country': this.country,
            'city': this.city,
            'phone': this.phone
          },
          'date_of_wedding': this.dateOfWedding
        }
      } else if (this.userStore.userType == 3) {
        data = {
          'user': {
            'name': this.name,
            'country': this.country,
            'city': this.city,
            'phone': this.phone
          },
          'roles': this.roles,
          'description': this.description,
          'countries': this.countries,
          'cities': this.cities,
          'languages': this.languages,
          'cost_work': this.costWork,
          'number_hours': this.numberHours,
          'profile_url': this.profileURL
        }
      }

      axios.put('/' + this.$i18n.locale + '/accounts/auth/profile/', data)
      .then((response) => {
        this.userStore.updateName(this.name)
        window.localStorage.setItem('user', JSON.stringify({
          'token': this.userStore.token,
          'username': this.userStore.username,
          'email': this.userStore.email,
          'user_type': this.userStore.userType,
          'name': this.name,
          'avatar': this.userStore.avatar
        }))
        this.status = 'updated_profile'
        this.errors = null
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
      .then(() => {
        document.body.scrollTop = 0
        document.documentElement.scrollTop = 0
      })
    }
  },
  watch: {
    country(newValue, oldValue) {
      if (oldValue) {
        this.city = null
      }
      if (newValue) {
        axios.get('/' + this.$i18n.locale + '/main/cities/', {
          params: {
            country: this.country
          }
        })
        .then((response) => {
          this.citiesList1 = response.data
        })
        .catch((error) => {
          this.errors = error.response.data
        })
      } else {
        this.citiesList1 = []
      }
    },
    countries(newValue) {
      if (newValue.length > 0) {
        let params = new URLSearchParams()
        this.countries.forEach(item => params.append('country', item))
        axios.get('/' + this.$i18n.locale + '/main/cities/', { params: params })
        .then((response) => {
          this.citiesList2 = response.data
        })
        .catch((error) => {
          this.errors = error.response.data
        })
      } else {
        this.citiesList2 = []
      }
    },
    citiesList2(newValue, oldValue) {
      if (newValue.length < oldValue.length) {
        const newCitiesList2 = []
        newValue.forEach(item => newCitiesList2.push(item.id))
        this.cities = this.cities.filter(item => newCitiesList2.includes(item))
      }
    }
  },
  mounted() {
    this.getProfileData()
    this.getCountriesData()
    this.getLanguagesData()
  }
}
</script>

<template>
  <div class="profile-settings px-1 px-lg-3 px-xl-5">
    <h1 class="display-6 mb-5">{{ $t('auth.profile.profile_settings') }}</h1>

    <div v-if="status">
      <div
        class="alert alert-success d-flex align-items-center alert-dismissible fade show"
        role="alert"
      >
        <i class="fa-solid fa-circle-check"></i>
        <div
          v-if="status == 'updated_profile'"
          class="ms-3"
        >
          {{ $t('auth.profile.profile_updated_successfully') }}
        </div>
        <button
          @click="status = null"
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </div>
    </div>

    <div
      v-if="pageLoading < 3"
      class="d-flex justify-content-center"
    >
      <div
        class="spinner-grow text-dark"
        role="status"
      >
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else>
      <ProfileCover />
      <ProfileAvatar />

      <form
        @submit.prevent="updateProfile"
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
          <label
            for="id_country"
            class="form-label"
          >
            {{ $t('auth.profile.country') }}
          </label>
          <select
            v-model="country"
            name="country"
            id="id_country"
            class="form-select"
          >
            <option value=""></option>
            <option
              v-for="countryList in countriesList"
              :value="countryList.code"
              :key="countryList.code"
            >
              {{ countryList.name_local }} ({{ countryList.name }})
            </option>
          </select>
        </div>
        <div class="col-md-6">
          <label
            for="id_city"
            class="form-label"
          >
            {{ $t('auth.profile.city') }}
          </label>
          <select
            v-model="city"
            name="city"
            id="id_city"
            class="form-select"
          >
            <option value=""></option>
            <option
              v-for="cityList in citiesList1"
              :value="cityList.id"
              :key="cityList.id"
            >
              {{ cityList.name_local }} ({{ cityList.name }})
            </option>
          </select>
        </div>
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.user && errors.user.phone"
            v-model="phone"
            :label="$t('auth.profile.phone')"
            :errors="errors.user.phone"
            id="id_phone"
            name="phone"
            type="text"
            maxlength="21"
          />
          <BaseInput
            v-else
            v-model="phone"
            :label="$t('auth.profile.phone')"
            id="id_phone"
            name="phone"
            type="text"
            maxlength="21"
          />
        </div>
        <div
          v-if="userStore.userType == 2"
          class="col-md-12"
        >
          <BaseInput
            v-if="errors && errors.date_of_wedding"
            v-model="dateOfWedding"
            :label="$t('auth.profile.date_of_wedding')"
            :errors="errors.date_of_wedding"
            id="id_date_of_wedding"
            name="date_of_wedding"
            type="date"
          />
          <BaseInput
            v-else
            v-model="dateOfWedding"
            :label="$t('auth.profile.date_of_wedding')"
            id="id_date_of_wedding"
            name="date_of_wedding"
            type="date"
          />
        </div>
        <div
          v-if="userStore.userType == 3"
          class="col-md-12"
        >
          <label
            for="id_roles"
            class="form-label"
          >
            {{ $t('auth.profile.roles') }}
          </label>
          <select
            v-model="roles"
            name="roles"
            id="id_roles"
            multiple=""
            class="form-select"
          >
            <option value="1">{{ $t('roles.photographer') }}</option>
            <option value="2">{{ $t('roles.videographer') }}</option>
            <option value="3">{{ $t('roles.leading') }}</option>
            <option value="4">{{ $t('roles.musician') }}</option>
            <option value="5">{{ $t('roles.dj') }}</option>
            <option value="6">{{ $t('roles.agency') }}</option>
            <option value="7">{{ $t('roles.salon') }}</option>
            <option value="8">{{ $t('roles.confectionery') }}</option>
            <option value="9">{{ $t('roles.decorator') }}</option>
            <option value="10">{{ $t('roles.visagiste') }}</option>
            <option value="11">{{ $t('roles.hairdresser') }}</option>
          </select>
          <div class="form-text">{{ $t('form_help.multiple_select') }}</div>
        </div>
        <div
          v-if="userStore.userType == 3"
          class="col-md-12"
        >
          <label
            for="id_description"
            class="form-label"
          >
            {{ $t('auth.profile.description') }}
          </label>
          <textarea
            v-model="description"
            name="description"
            cols="40"
            rows="10"
            id="id_description"
            class="form-control"
          ></textarea>
        </div>
        <div
          v-if="userStore.userType == 3"
          class="col-md-6"
        >
          <label
            for="id_countries"
            class="form-label"
          >
            {{ $t('auth.profile.countries') }}
          </label>
          <select
            v-model="countries"
            name="countries"
            id="id_countries"
            multiple=""
            class="form-select"
          >
            <option
              v-for="countryList in countriesList"
              :value="countryList.code"
              :key="countryList.code"
            >
              {{ countryList.name_local }} ({{ countryList.name }})
            </option>
          </select>
          <div class="form-text">{{ $t('form_help.multiple_select') }}</div>
        </div>
        <div
          v-if="userStore.userType == 3"
          class="col-md-6"
        >
          <label
            for="id_cities"
            class="form-label"
          >
            {{ $t('auth.profile.cities') }}
          </label>
          <select
            v-model="cities"
            name="cities"
            id="id_cities"
            multiple=""
            class="form-select"
          >
            <option
              v-for="cityList in citiesList2"
              :value="cityList.id"
              :key="cityList.id"
            >
              {{ cityList.name_local }} ({{ cityList.name }})
            </option>
          </select>
          <div class="form-text">{{ $t('form_help.multiple_select') }}</div>
        </div>
        <div
          v-if="userStore.userType == 3"
          class="col-md-12"
        >
          <label
            for="id_languages"
            class="form-label"
          >
            {{ $t('auth.profile.languages') }}
          </label>
          <select
            v-model="languages"
            name="languages"
            id="id_languages"
            multiple=""
            class="form-select"
          >
            <option
              v-for="languageList in languagesList"
              :value="languageList.code"
              :key="languageList.code"
            >
              {{ languageList.name_local }} ({{ languageList.name }})
            </option>
          </select>
          <div class="form-text">{{ $t('form_help.multiple_select') }}</div>
        </div>
        <div
          v-if="userStore.userType == 3"
          class="col-md-6"
        >
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
        <div
          v-if="userStore.userType == 3"
          class="col-md-6"
        >
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
        <div
          v-if="userStore.userType == 3"
          class="col-md-12"
        >
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
          <button
            type="submit"
            class="btn btn-primary"
          >
            {{ $t('auth.profile.update_profile') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

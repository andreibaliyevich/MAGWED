<script setup>
import axios from 'axios'

import ProfileAvatar from '@/components/auth/ProfileAvatar.vue'
import ProfileCover from '@/components/auth/ProfileCover.vue'
import BaseInput from '@/components/UI/BaseInput.vue'
import BaseSelect from '@/components/UI/BaseSelect.vue'

import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<script>
export default {
  data() {
    return {
      pageLoading: 0,
      profile: {
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
      },
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
          this.profile.name = response.data.name
          this.profile.country = response.data.country
          this.profile.city = response.data.city
          this.profile.phone = response.data.phone
        } else if (this.userStore.userType == 2) {
          this.profile.name = response.data.user.name
          this.profile.country = response.data.user.country
          this.profile.city = response.data.user.city
          this.profile.phone = response.data.user.phone
          this.profile.dateOfWedding = response.data.date_of_wedding
        } else if (this.userStore.userType == 3) {
          this.profile.name = response.data.user.name
          this.profile.country = response.data.user.country
          this.profile.city = response.data.user.city
          this.profile.phone = response.data.user.phone
          this.profile.roles = response.data.roles
          this.profile.description = response.data.description
          this.profile.countries = response.data.countries
          this.profile.cities = response.data.cities
          this.profile.languages = response.data.languages
          this.profile.costWork = response.data.cost_work
          this.profile.numberHours = response.data.number_hours
          this.profile.profileURL = response.data.profile_url
          this.profile.rating = response.data.rating
          this.profile.proTime = response.data.pro_time
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
        response.data.forEach((element) => {
          this.countriesList.push({
            'value': element.code,
            'name': `${ element.name_local } (${ element.name })`
          })
        })
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

      if (!this.profile.country) {
        this.profile.country = null
      }
      if (!this.profile.city) {
        this.profile.city = null
      }
      if (!this.profile.dateOfWedding) {
        this.profile.dateOfWedding = null
      }

      let data = {}
      if (this.userStore.userType == 1) {
        data = {
          'name': this.profile.name,
          'country': this.profile.country,
          'city': this.profile.city,
          'phone': this.profile.phone
        }
      } else if (this.userStore.userType == 2) {
        data = {
          'user': {
            'name': this.profile.name,
            'country': this.profile.country,
            'city': this.profile.city,
            'phone': this.profile.phone
          },
          'date_of_wedding': this.profile.dateOfWedding
        }
      } else if (this.userStore.userType == 3) {
        data = {
          'user': {
            'name': this.profile.name,
            'country': this.profile.country,
            'city': this.profile.city,
            'phone': this.profile.phone
          },
          'roles': this.profile.roles,
          'description': this.profile.description,
          'countries': this.profile.countries,
          'cities': this.profile.cities,
          'languages': this.profile.languages,
          'cost_work': this.profile.costWork,
          'number_hours': this.profile.numberHours,
          'profile_url': this.profile.profileURL
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
          'name': this.profile.name,
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
    'profile.country'(newValue, oldValue) {
      if (oldValue) {
        this.profile.city = null
      }
      if (newValue) {
        axios.get('/' + this.$i18n.locale + '/main/cities/', {
          params: {
            country: this.profile.country
          }
        })
        .then((response) => {
          this.citiesList1 = []
          response.data.forEach((element) => {
            this.citiesList1.push({
              'value': element.id,
              'name': `${ element.name_local } (${ element.name })`
            })
          })
        })
        .catch((error) => {
          this.errors = error.response.data
        })
      } else {
        this.citiesList1 = []
      }
    },
    'profile.countries'(newValue) {
      if (newValue.length > 0) {
        let params = new URLSearchParams()
        this.profile.countries.forEach(item => params.append('country', item))
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
      <ProfileCover v-if="userStore.userType == 3" />
      <ProfileAvatar />

      <form
        @submit.prevent="updateProfile"
        class="row g-3 mt-3"
      >
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.user && errors.user.name"
            v-model="profile.name"
            :label="$t('auth.profile.name')"
            :errors="errors.user.name"
            id="id_name"
            name="name"
            type="text"
          />
          <BaseInput
            v-else
            v-model="profile.name"
            :label="$t('auth.profile.name')"
            id="id_name"
            name="name"
            type="text"
          />
        </div>
        <div class="col-md-6">
          <BaseSelect
            v-model="profile.country"
            :label="$t('auth.profile.country')"
            :options="countriesList"
            id="id_country"
            name="country"
          />
        </div>
        <div class="col-md-6">
          <BaseSelect
            v-model="profile.city"
            :label="$t('auth.profile.city')"
            :options="citiesList1"
            id="id_country"
            name="country"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.user && errors.user.phone"
            v-model="profile.phone"
            :label="$t('auth.profile.phone')"
            :errors="errors.user.phone"
            id="id_phone"
            name="phone"
            type="text"
            maxlength="21"
          />
          <BaseInput
            v-else
            v-model="profile.phone"
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
            v-model="profile.dateOfWedding"
            :label="$t('auth.profile.date_of_wedding')"
            :errors="errors.date_of_wedding"
            id="id_date_of_wedding"
            name="date_of_wedding"
            type="date"
          />
          <BaseInput
            v-else
            v-model="profile.dateOfWedding"
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
            v-model="profile.roles"
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
            v-model="profile.description"
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
            v-model="profile.countries"
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
            v-model="profile.cities"
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
            v-model="profile.languages"
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
            v-model="profile.costWork"
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
            v-model="profile.costWork"
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
            v-model="profile.numberHours"
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
            v-model="profile.numberHours"
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
            v-model="profile.profileURL"
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
            v-model="profile.profileURL"
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

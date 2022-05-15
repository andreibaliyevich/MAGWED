<script setup>
import axios from 'axios'

import { useBaseStore } from '@/stores/base.js'
import { useUserStore } from '@/stores/user.js'
const baseStore = useBaseStore()
const userStore = useUserStore()
</script>

<script>
export default {
  data() {
    return {
      name: '',
      country: null,
      city: null,
      phone: '',
      date_of_wedding: null,
      roles: [],
      cover: null,
      description: '',
      countries: [],
      cities: [],
      languages: [],
      cost_work: 0.00,
      number_hours: 0,
      profile_url: '',
      rating: 0.0,
      pro_time: null,
      main_countries: [],
      main_cities: [],
      main_languages: [],
      status: null,
      errors: null
    }
  },
  methods: {
    async getProfileData() {
      try {
        const response = await axios.get('/accounts/auth/profile/')
        if (this.userStore.user_type == 1) {
          this.name = response.data.name
          this.country = response.data.country
          this.city = response.data.city
          this.phone = response.data.phone
        } else if (this.userStore.user_type == 2) {
          this.name = response.data.user.name
          this.country = response.data.user.country
          this.city = response.data.user.city
          this.phone = response.data.user.phone
          this.date_of_wedding = response.data.date_of_wedding
        } else if (this.userStore.user_type == 3) {
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
          this.cost_work = response.data.cost_work
          this.number_hours = response.data.number_hours
          this.profile_url = response.data.profile_url
          this.rating = response.data.rating
          this.pro_time = response.data.pro_time
        }
      } catch (error) {
        this.errors = error.response.data
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
      if (!this.date_of_wedding) {
        this.date_of_wedding = null
      }

      let data = {}
      if (this.userStore.user_type == 1) {
        data = {
          'name': this.name,
          'country': this.country,
          'city': this.city,
          'phone': this.phone
        }
      } else if (this.userStore.user_type == 2) {
        data = {
          'user': {
            'name': this.name,
            'country': this.country,
            'city': this.city,
            'phone': this.phone,
          },
          'date_of_wedding': this.date_of_wedding
        }
      } else if (this.userStore.user_type == 3) {
        data = {
          'user': {
            'name': this.name,
            'country': this.country,
            'city': this.city,
            'phone': this.phone,
          },
          'roles': this.roles,
          'description': this.description,
          'countries': this.countries,
          'cities': this.cities,
          'languages': this.languages,
          'cost_work': this.cost_work,
          'number_hours': this.number_hours,
          'profile_url': this.profile_url,
          'rating': this.rating,
          'pro_time': this.pro_time
        }
      }

      axios.put('/accounts/auth/profile/', data)
      .then((response) => {
        if (response.status === 204) {
          this.status = '204'
        }
      })
      .catch((error) => {
        this.errors = error.response.data
      })
      .then(() => {
        document.body.scrollTop = 0
        document.documentElement.scrollTop = 0
      })
    },
    async getCountriesData() {
      try {
        const response = await axios.get('/main/countries/')
        this.main_countries = response.data
      } catch (error) {
        this.errors = error.response.data
      }
    },
    async getCitiesData() {
      try {
        const response = await axios.get('/main/cities/')
        this.main_cities = response.data
      } catch (error) {
        this.errors = error.response.data
      }
    },
    async getLanguagesData() {
      try {
        const response = await axios.get('/main/languages/')
        this.main_languages = response.data
      } catch (error) {
        this.errors = error.response.data
      }
    }
  },
  mounted() {
    this.getProfileData()
    this.getCountriesData()
    this.getCitiesData()
    this.getLanguagesData()
  }
}
</script>

<template>
  <div class="profile">
    <h1>{{ $t('auth.profile.profile') }}</h1>

    <div>
      <p>Username: {{ userStore.username }}</p>

      <img v-if="userStore.avatar" :src="`${ baseStore.apiURL }${ userStore.avatar }`" width="100" height="100" class="rounded-circle">
      <img v-else src="/avatar.jpg" width="100" height="100" class="rounded-circle">

      <img v-if="cover" :src="`${ baseStore.apiURL }${ cover }`" width="300" height="189">
      <img v-else src="/cover.jpg" width="300" height="100">
    </div>

    <div v-if="status" id="status">
      <div class="alert alert-success d-flex align-items-center alert-dismissible fade show" role="alert">
        <i class="fa-solid fa-circle-check"></i>
        <div class="ms-3">{{ $t('auth.profile.profile_updated_successfully') }}</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    </div>
    <form @submit.prevent="updateProfile" class="row g-3 mt-3">
      <div class="col-md-12">
        <label for="id_name" class="form-label">{{ $t('auth.profile.name') }}</label>
        <input v-model="name" :placeholder="$t('auth.profile.name')" type="text" name="name" maxlength="255" id="id_name" class="form-control">
      </div>
      <div class="col-md-6">
        <label for="id_country" class="form-label">{{ $t('auth.profile.country') }}</label>
        <select v-model="country" name="country" id="id_country" class="form-select">
          <option value="" selected="">---------</option>
          <option v-for="main_country in main_countries" :value="main_country.code" :key="main_country.code">
            {{ main_country.name_local }} ({{ main_country.name }})
          </option>
        </select>
      </div>
      <div class="col-md-6">
        <label for="id_city" class="form-label">{{ $t('auth.profile.city') }}</label>
        <select v-model="city" name="city" id="id_city" class="form-select">
          <option value="" selected="">---------</option>
          <option v-for="main_city in main_cities" :value="main_city.id" :key="main_city.id">
            {{ main_city.name_local }} ({{ main_city.name }})
          </option>
        </select>
      </div>
      <div class="col-md-12">
        <label for="id_phone" class="form-label">{{ $t('auth.profile.phone') }}</label>
        <input  v-model="phone" type="text" name="phone" maxlength="21" id="id_phone" class="form-control">
      </div>
      <div v-if="userStore.user_type == 2" class="col-md-12">
        <label for="id_date_of_wedding" class="form-label">{{ $t('auth.profile.date_of_wedding') }}</label>
        <input v-model="date_of_wedding" type="text" name="date_of_wedding" size="10" id="id_date_of_wedding" class="form-control">
      </div>
      <div v-if="userStore.user_type == 3" class="col-md-12">
        <label for="id_roles" class="form-label">{{ $t('auth.profile.roles') }}</label>
        <select v-model="roles" name="roles" id="id_roles" multiple="" class="form-select">
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
      <div v-if="userStore.user_type == 3" class="col-md-12">
        <label for="id_description" class="form-label">{{ $t('auth.profile.description') }}</label>
        <textarea v-model="description" name="description" cols="40" rows="10" id="id_description" class="form-control"></textarea>
      </div>
      <div v-if="userStore.user_type == 3" class="col-md-6">
        <label for="id_countries" class="form-label">{{ $t('auth.profile.countries') }}</label>
        <select v-model="countries" name="countries" id="id_countries" multiple="" class="form-select">
          <option v-for="main_country in main_countries" :value="main_country.code" :key="main_country.code">
            {{ main_country.name_local }} ({{ main_country.name }})
          </option>
        </select>
        <div class="form-text">{{ $t('form_help.multiple_select') }}</div>
      </div>
      <div v-if="userStore.user_type == 3" class="col-md-6">
        <label for="id_cities" class="form-label">{{ $t('auth.profile.cities') }}</label>
        <select v-model="cities" name="cities" id="id_cities" multiple="" class="form-select">
          <option v-for="main_city in main_cities" :value="main_city.id" :key="main_city.id">
            {{ main_city.name_local }} ({{ main_city.name }})
          </option>
        </select>
        <div class="form-text">{{ $t('form_help.multiple_select') }}</div>
      </div>
      <div v-if="userStore.user_type == 3" class="col-md-12">
        <label for="id_languages" class="form-label">{{ $t('auth.profile.languages') }}</label>
        <select v-model="languages" name="languages" id="id_languages" multiple="" class="form-select">
          <option v-for="main_language in main_languages" :value="main_language.code" :key="main_language.code">
            {{ main_language.name_local }} ({{ main_language.name }})
          </option>
        </select>
        <div class="form-text">{{ $t('form_help.multiple_select') }}</div>
      </div>
      <div v-if="userStore.user_type == 3" class="col-md-6">
        <label for="id_cost_work" class="form-label">{{ $t('auth.profile.cost_work') }}</label>
        <input v-model="cost_work" type="number" name="cost_work" min="0.00" step="0.01" required="" id="id_cost_work" class="form-control">
      </div>
      <div v-if="userStore.user_type == 3" class="col-md-6">
        <label for="id_number_hours" class="form-label">{{ $t('auth.profile.number_hours') }}</label>
        <input v-model="number_hours" type="number" name="number_hours" min="0" required="" id="id_number_hours" class="form-control">
      </div>
      <div v-if="userStore.user_type == 3" class="col-md-12">
        <label for="id_profile_url" class="form-label">{{ $t('auth.profile.profile_url') }}</label>
        <div v-if="errors && errors.profile_url">
          <input v-model="profile_url" type="text" name="profile_url" maxlength="64" required="" id="id_profile_url" class="form-control is-invalid">
          <div v-for="error in errors.profile_url" class="invalid-feedback">{{ error }}</div>
        </div>
        <input v-else v-model="profile_url" type="text" name="profile_url" maxlength="64" required="" id="id_profile_url" class="form-control">
      </div>
      <div class="col-12">
        <button type="submit" class="btn btn-primary">{{ $t('auth.profile.update_profile') }}</button>
      </div>
    </form>
  </div>
</template>

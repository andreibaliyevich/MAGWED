<script setup>
import axios from 'axios'

import ProfileAvatar from '@/components/auth/ProfileAvatar.vue'
import ProfileCover from '@/components/auth/ProfileCover.vue'

import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<script>
export default {
  data() {
    return {
      pageLoading: 0,
      roleTypeOptions: [],
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
      countriesOptions: [],
      citiesOptions1: [],
      citiesOptions2: [],
      languagesOptions: [],
      status: null,
      errors: null
    }
  },
  methods: {
    setRoleTypeOptions() {
      this.roleTypeOptions = [
        { value: 1, text: this.$t('roles.photographer') },
        { value: 2, text: this.$t('roles.videographer') },
        { value: 3, text: this.$t('roles.leading') },
        { value: 4, text: this.$t('roles.musician') },
        { value: 5, text: this.$t('roles.dj') },
        { value: 6, text: this.$t('roles.agency') },
        { value: 7, text: this.$t('roles.salon') },
        { value: 8, text: this.$t('roles.confectionery') },
        { value: 9, text: this.$t('roles.decorator') },
        { value: 10, text: this.$t('roles.visagiste') },
        { value: 11, text: this.$t('roles.hairdresser') }
      ]
    },
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
          this.countriesOptions.push({
            'value': element.code,
            'text': `${ element.name_local } (${ element.name })`
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
        response.data.forEach((element) => {
          this.languagesOptions.push({
            'value': element.code,
            'text': `${ element.name_local } (${ element.name })`
          })
        })
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
    '$i18n.locale'() {
      this.setRoleTypeOptions()
    },
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
          this.citiesOptions1 = []
          response.data.forEach((element) => {
            this.citiesOptions1.push({
              'value': element.id,
              'text': `${ element.name_local } (${ element.name })`
            })
          })
        })
        .catch((error) => {
          this.errors = error.response.data
        })
      } else {
        this.citiesOptions1 = []
      }
    },
    'profile.countries'(newValue) {
      if (newValue.length > 0) {
        let params = new URLSearchParams()
        this.profile.countries.forEach((element) => {
          params.append('country', element)
        })
        axios.get('/' + this.$i18n.locale + '/main/cities/', { params: params })
        .then((response) => {
          this.citiesOptions2 = []
          response.data.forEach((element) => {
            this.citiesOptions2.push({
              'value': element.id,
              'text': `${ element.name_local } (${ element.name })`
            })
          })
        })
        .catch((error) => {
          this.errors = error.response.data
        })
      } else {
        this.citiesOptions2 = []
      }
    },
    citiesOptions2(newValue, oldValue) {
      if (newValue.length < oldValue.length) {
        const newCities = []
        newValue.forEach(element => newCities.push(element.value))
        this.profile.cities = this.profile.cities.filter((element) => {
          return newCities.includes(element)
        })
      }
    }
  },
  mounted() {
    this.setRoleTypeOptions()
    this.getProfileData()
    this.getCountriesData()
    this.getLanguagesData()
  }
}
</script>

<template>
  <div class="profile-settings px-1 px-lg-3 px-xl-5">
    <h1 class="display-6 mb-5">{{ $t('auth.profile.profile_settings') }}</h1>

    <PageLoadingIndicator v-if="pageLoading < 3" />
    <div v-else>
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
            :options="countriesOptions"
            id="id_country"
            name="country"
          />
        </div>
        <div class="col-md-6">
          <BaseSelect
            v-model="profile.city"
            :label="$t('auth.profile.city')"
            :options="citiesOptions1"
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
            type="tel"
            maxlength="21"
          />
          <BaseInput
            v-else
            v-model="profile.phone"
            :label="$t('auth.profile.phone')"
            id="id_phone"
            name="phone"
            type="tel"
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
          <MultipleSelect
            v-model="profile.roles"
            :label="$t('auth.profile.roles')"
            :options="roleTypeOptions"
            id="id_roles"
            name="roles"
          />
        </div>
        <div
          v-if="userStore.userType == 3"
          class="col-md-12"
        >
          <BaseTextarea
            v-model="profile.description"
            :label="$t('auth.profile.description')"
            id="id_description"
            name="description"
          />
        </div>
        <div
          v-if="userStore.userType == 3"
          class="col-md-12"
        >
          <MultipleSelect
            v-model="profile.countries"
            :label="$t('auth.profile.countries')"
            :options="countriesOptions"
            id="id_countries"
            name="countries"
          />
        </div>
        <div
          v-if="userStore.userType == 3"
          class="col-md-12"
        >
          <MultipleSelect
            v-model="profile.cities"
            :label="$t('auth.profile.cities')"
            :options="citiesOptions2"
            id="id_cities"
            name="cities"
          />
        </div>
        <div
          v-if="userStore.userType == 3"
          class="col-md-12"
        >
          <MultipleSelect
            v-model="profile.languages"
            :label="$t('auth.profile.languages')"
            :options="languagesOptions"
            id="id_languages"
            name="languages"
          />
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
            class="btn btn-brand btn-lg"
          >
            {{ $t('auth.profile.update_profile') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

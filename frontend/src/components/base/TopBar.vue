<script setup>
import { RouterLink } from 'vue-router'
import axios from 'axios'

import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<script>
export default {
  methods: {
    changeLocale(event) {
      this.$router.push({ params: { locale: event.target.value } })
    },
    logout() {
      axios.post('/en/accounts/auth/logout/')
        .then(() => {
          window.localStorage.removeItem('user')
          window.location.reload()
        })
    }
  }
}
</script>

<template>
  <div class="bg-dark text-white py-1">
    <div class="container">
      <div class="d-flex justify-content-between">
        <div class="d-flex align-items-center">Social icons</div>
        <div class="d-flex">
          <div class="d-flex align-items-center dropdown me-3">
            <a class="d-flex align-items-center dropdown-toggle text-decoration-none text-white" href="#" role="button" id="dropdownLocale" data-bs-toggle="dropdown" aria-expanded="false">
              <img :src="'/flags/' + this.$i18n.locale + '.png'" width="20" :alt="this.$i18n.locale">
              <span class="text-uppercase ms-1">{{ this.$i18n.locale }} / $</span>
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownLocale">
              <li class="dropdown-item">
                <select :value="$i18n.locale" @change="changeLocale" class="form-select">
                  <option value="en">English</option>
                  <option value="ru">Русский</option>
                  <option value="be">Беларуская</option>
                  <option value="uk">Українська</option>
                </select>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ params: { locale: 'en' }}">
                  <img src="/flags/en.png" width="20" alt="en">
                  <span class="ms-1">English</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ params: { locale: 'ru' }}">
                  <img src="/flags/ru.png" width="20" alt="ru">
                  <span class="ms-1">Русский</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ params: { locale: 'be' }}">
                  <img src="/flags/be.png" width="20" alt="be">
                  <span class="ms-1">Беларуская</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ params: { locale: 'uk' }}">
                  <img src="/flags/uk.png" width="20" alt="uk">
                  <span class="ms-1">Українська</span>
                </RouterLink>
              </li>
            </ul>
          </div>
          <div class="d-flex align-items-center" v-if="userStore.isLoggedIn">
            <RouterLink class="btn btn-brand btn-sm rounded-pill px-3 me-1" :to="{ name: 'Profile', params: { locale: `${ $i18n.locale }` }}">{{ $t('auth.profile') }}</RouterLink>
            <button class="btn btn-outline-brand btn-sm rounded-pill px-3" @click="logout">{{ $t('auth.logout') }}</button>
          </div>
          <div class="d-flex align-items-center" v-else>
            <RouterLink class="btn btn-brand btn-sm rounded-pill px-3 me-1" :to="{ name: 'Registration', params: { locale: `${ $i18n.locale }` }}">{{ $t('auth.registration') }}</RouterLink>
            <RouterLink class="btn btn-outline-brand btn-sm rounded-pill px-3" :to="{ name: 'Login', params: { locale: `${ $i18n.locale }` }}">{{ $t('auth.login') }}</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>

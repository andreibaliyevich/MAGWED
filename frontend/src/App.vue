<script setup>
import { RouterLink, RouterView } from 'vue-router'
import axios from 'axios'

import AppNav from '@/components/base/AppNav.vue'
import LanguageSwitcher from '@/components/base/LanguageSwitcher.vue'

import { useBaseStore } from '@/stores/base.js'
import { useUserStore } from '@/stores/user.js'
const baseStore = useBaseStore()
const userStore = useUserStore()
</script>

<script>
export default {
  created() {
    const userString = window.localStorage.getItem('user')
    if (userString) {
      const userData = JSON.parse(userString)
      axios.defaults.headers.common['Authorization'] = `Token ${ userData.token }`
      this.userStore.setUserData(userData)
    }

    axios.defaults.baseURL = this.baseStore.apiURL
    axios.interceptors.response.use(
      response => response,
      error => {
        if (error.response.status === 401) {
          window.localStorage.removeItem('user')
          window.location.reload()
        }
        return Promise.reject(error)
      }
    )
  }
}
</script>

<template>
  <header>
    <div class="wrapper">
      <AppNav />
      <LanguageSwitcher />
    </div>
  </header>

  <RouterView />
</template>

<style>
@import '@/assets/base.css';


</style>

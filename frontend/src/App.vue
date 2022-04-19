<script setup>
import { RouterLink, RouterView } from 'vue-router'
import axios from 'axios'

import AppNav from '@/components/base/AppNav.vue'
import LanguageSwitcher from '@/components/base/LanguageSwitcher.vue'
import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<script>
export default {
  created() {
    const userString = window.localStorage.getItem('AUTH_USER')
    if (userString) {
      const authUser = JSON.parse(userString)
      axios.defaults.headers.common['Authorization'] = `Token ${ authUser.token }`
      this.userStore.setUser(authUser)
    }

    axios.defaults.baseURL = 'http://localhost:8000'
    axios.interceptors.response.use(
      response => response,
      error => {
        if (error.response.status === 401) {
          window.localStorage.removeItem('AUTH_USER')
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

<script setup>
import { RouterLink } from 'vue-router'
import axios from 'axios'

import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<script>
export default {
  methods: {
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
  <nav>
    <RouterLink :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">{{ $t('nav.home') }}</RouterLink>
    <RouterLink :to="{ name: 'About', params: { locale: `${ $i18n.locale }` }}">{{ $t('nav.about') }}</RouterLink>
    <RouterLink :to="{ name: 'Blog', params: { locale: `${ $i18n.locale }` }}">{{ $t('blog.blog') }}</RouterLink>
    <div v-if="userStore.isLoggedIn">
      <RouterLink :to="{ name: 'Profile', params: { locale: `${ $i18n.locale }` }}">{{ $t('auth.profile') }}</RouterLink>
      <button @click="logout" class="logoutButton">{{ $t('auth.logout') }}</button>
    </div>
    <div v-else>
      <RouterLink :to="{ name: 'Login', params: { locale: `${ $i18n.locale }` }}">{{ $t('auth.login') }}</RouterLink>
      <RouterLink :to="{ name: 'Registration', params: { locale: `${ $i18n.locale }` }}">{{ $t('auth.registration') }}</RouterLink>
    </div>
  </nav>
</template>

<style>
.logoutButton {
  cursor: pointer;
}
</style>

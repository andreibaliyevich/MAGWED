<script setup>
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<script>
export default {
  methods: {
    logout() {
      this.userStore.logout()
      .then(() => {
        window.location.reload()
      })
    }
  }
}
</script>

<template>
  <nav>
    <RouterLink :to="{ name: 'home', params: { locale: `${ $i18n.locale }` }}">{{ $t('nav.home') }}</RouterLink>
    <RouterLink :to="{ name: 'about', params: { locale: `${ $i18n.locale }` }}">{{ $t('nav.about') }}</RouterLink>
    <RouterLink :to="{ name: 'blog', params: { locale: `${ $i18n.locale }` }}">{{ $t('blog.blog') }}</RouterLink>
    <div v-if="userStore.isLoggedIn">
      <RouterLink :to="{ name: 'profile', params: { locale: `${ $i18n.locale }` }}">{{ $t('auth.profile') }}</RouterLink>
      <button @click="logout" class="logoutButton">Logout</button>
    </div>
    <div v-else>
      <RouterLink :to="{ name: 'login', params: { locale: `${ $i18n.locale }` }}">{{ $t('auth.login') }}</RouterLink>
    </div>
  </nav>
</template>

<style>
.logoutButton {
  cursor: pointer;
}
</style>

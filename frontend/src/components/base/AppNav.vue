<script setup>
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<template>
  <nav>
    <RouterLink :to="{ name: 'home', params: { locale: `${ $i18n.locale }` }}">{{ $t('nav.home') }}</RouterLink>
    <RouterLink :to="{ name: 'about', params: { locale: `${ $i18n.locale }` }}">{{ $t('nav.about') }}</RouterLink>
    <a v-if="userStore.loggedIn" href="#">Profile</a>
    <RouterLink v-else :to="{ name: 'login', params: { locale: `${ $i18n.locale }` }}">{{ $t('auth.login') }}</RouterLink>
    <RouterLink :to="{ name: 'blog', params: { locale: `${ $i18n.locale }` }}">{{ $t('blog.blog') }}</RouterLink>
  </nav>
</template>

<style>

</style>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav>
    <RouterLink :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">{{ $t('nav.home') }}</RouterLink>
    <RouterLink :to="{ name: 'About', params: { locale: `${ $i18n.locale }` }}">{{ $t('nav.about') }}</RouterLink>
    <RouterLink :to="{ name: 'Blog', params: { locale: `${ $i18n.locale }` }}">{{ $t('blog.blog') }}</RouterLink>
  </nav>
</template>

<style scoped>

</style>

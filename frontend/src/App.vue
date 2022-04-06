<script setup>
import { RouterLink, RouterView } from 'vue-router'
import LanguageSwitcher from '@/components/base/LanguageSwitcher.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink :to="{ name: 'home', params: { locale: `${ $i18n.locale }` }}">{{ $t('nav.home') }}</RouterLink>
        <RouterLink :to="{ name: 'about', params: { locale: `${ $i18n.locale }` }}">{{ $t('nav.about') }}</RouterLink>
        <RouterLink :to="{ name: 'login', params: { locale: `${ $i18n.locale }` }}">{{ $t('auth.login') }}</RouterLink>
        <RouterLink :to="{ name: 'blog', params: { locale: `${ $i18n.locale }` }}">{{ $t('blog.blog') }}</RouterLink>
      </nav>
      <LanguageSwitcher />
    </div>
  </header>

  <RouterView />
</template>

<style>
@import '@/assets/base.css';


</style>

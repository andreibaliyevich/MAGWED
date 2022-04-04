<script setup>
import { RouterLink, RouterView } from 'vue-router'
import LanguageSwitcher from '@/components/base/LanguageSwitcher.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">{{ $t('nav.home') }}</RouterLink>
        <RouterLink to="/about">{{ $t('nav.about') }}</RouterLink>
        <RouterLink to="/login">{{ $t('auth.login') }}</RouterLink>
        <RouterLink to="/blog">{{ $t('blog.blog') }}</RouterLink>
      </nav>
      <LanguageSwitcher />
    </div>
  </header>

  <RouterView />
</template>

<style>
@import '@/assets/base.css';


</style>

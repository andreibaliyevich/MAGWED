<script setup>
import { RouterLink, RouterView } from 'vue-router'
import LanguageSwitcher from '@/components/base/LanguageSwitcher.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">{{ $t('router.home') }}</RouterLink>
        <RouterLink to="/about">{{ $t('router.about') }}</RouterLink>
      </nav>
      <LanguageSwitcher />
    </div>
  </header>

  <RouterView />
</template>

<style>
@import '@/assets/base.css';


</style>

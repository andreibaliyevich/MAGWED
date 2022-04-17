<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppNav from '@/components/base/AppNav.vue'
import LanguageSwitcher from '@/components/base/LanguageSwitcher.vue'
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

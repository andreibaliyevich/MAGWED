<script setup>
import { RouterLink, RouterView } from 'vue-router'
import axios from 'axios'
import LanguageSwitcher from '@/components/base/LanguageSwitcher.vue'

axios.defaults.baseURL = 'http://localhost:8000';
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">{{ $t('nav.home') }}</RouterLink>
        <RouterLink to="/about">{{ $t('nav.about') }}</RouterLink>
        <RouterLink to="/login">{{ $t('auth.login') }}</RouterLink>
      </nav>
      <LanguageSwitcher />
    </div>
  </header>

  <RouterView />
</template>

<style>
@import '@/assets/base.css';


</style>

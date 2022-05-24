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
  <div class="position-sticky" style="top: 120px;">
    <button class="btn btn-secondary w-100 d-lg-none mb-3" type="button" data-bs-toggle="collapse" data-bs-target="#account-menu" aria-expanded="false" aria-label="Account menu">
      {{ $t('auth.account_menu') }}
      <i class="fa-solid fa-caret-down ms-1"></i>
    </button>
    <div id="account-menu" class="collapse d-lg-block">
      <div class="text-uppercase fw-bolder text-secondary">{{ $t('auth.social') }}</div>
      <ul class="nav nav-pills flex-column">
        <li class="nav-item">
          <RouterLink v-if="this.$route.name == 'Messenger'" class="nav-link active" aria-current="page" :to="{ name: 'Messenger', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-comments"></i>
            {{ $t('auth.messenger') }}
          </RouterLink>
          <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Messenger', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-comments"></i>
            {{ $t('auth.messenger') }}
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink v-if="this.$route.name == 'Notifications'" class="nav-link active" aria-current="page" :to="{ name: 'Notifications', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-bell"></i>
            {{ $t('auth.notifications') }}
          </RouterLink>
          <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Notifications', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-bell"></i>
            {{ $t('auth.notifications') }}
          </RouterLink>
        </li>
        <li v-if="userStore.user_type == 3" class="nav-item">
          <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-users"></i>
            {{ $t('auth.followers') }}
          </RouterLink>
          <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-users"></i>
            {{ $t('auth.followers') }}
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-user-group"></i>
            {{ $t('auth.following') }}
          </RouterLink>
          <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-user-group"></i>
            {{ $t('auth.following') }}
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-star"></i>
            {{ $t('auth.favorites') }}
          </RouterLink>
          <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-star"></i>
            {{ $t('auth.favorites') }}
          </RouterLink>
        </li>
      </ul>
      <div class="text-uppercase fw-bolder text-secondary mt-3">{{ $t('auth.account') }}</div>
      <ul class="nav nav-pills flex-column">
        <li class="nav-item">
          <RouterLink v-if="this.$route.name == 'Profile'" class="nav-link active" aria-current="page" :to="{ name: 'Profile', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-user"></i>
            {{ $t('auth.profile.profile') }}
          </RouterLink>
          <RouterLink v-else class="w-100 nav-link text-dark" :to="{ name: 'Profile', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-user"></i>
            {{ $t('auth.profile.profile') }}
          </RouterLink>
        </li>
        <li v-if="userStore.user_type == 3" class="nav-item">
          <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-briefcase"></i>
            {{ $t('auth.portfolio') }}
          </RouterLink>
          <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-briefcase"></i>
            {{ $t('auth.portfolio') }}
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-key"></i>
            {{ $t('auth.change_password') }}
          </RouterLink>
          <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-key"></i>
            {{ $t('auth.change_password') }}
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-user-xmark"></i>
            {{ $t('auth.delete_profile') }}
          </RouterLink>
          <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-user-xmark"></i>
            {{ $t('auth.delete_profile') }}
          </RouterLink>
        </li>
        <li class="nav-item">
          <div v-if="this.$route.name == 'Home'" @click="logout" class="nav-link active" aria-current="page">
            <i class="fa-solid fa-right-from-bracket"></i>
            {{ $t('auth.logout') }}
          </div>
          <div v-else @click="logout" class="nav-link text-dark">
            <i class="fa-solid fa-right-from-bracket"></i>
            {{ $t('auth.logout') }}
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

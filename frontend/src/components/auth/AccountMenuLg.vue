<script setup>
import axios from 'axios'

import { userType } from '@/config.js'

import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<script>
export default {
  methods: {
    logout() {
      axios.post('/accounts/auth/logout/')
      .then(() => {
        window.localStorage.removeItem('user')
        window.location.reload()
      })
    }
  }
}
</script>

<template>
  <div class="account-menu-lg">
    <div class="text-uppercase fw-bolder text-secondary">
      {{ $t('auth.social') }}
    </div>
    <ul class="nav nav-pills flex-column">
      <li class="nav-item">
        <LocaleRouterLink
          v-if="this.$route.name == 'Notifications'"
          routeName="Notifications"
          class="nav-link active"
          aria-current="page"
        >
          <i class="fa-solid fa-bell"></i>
          {{ $t('auth.notifications') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          v-else
          routeName="Notifications"
          class="nav-link text-dark"
        >
          <i class="fa-solid fa-bell"></i>
          {{ $t('auth.notifications') }}
        </LocaleRouterLink>
      </li>
      <li v-if="userStore.userType == userType.ORGANIZER" class="nav-item">
        <LocaleRouterLink
          v-if="this.$route.name == 'Home'"
          routeName="Home"
          class="nav-link active"
          aria-current="page"
        >
          <i class="fa-solid fa-users"></i>
          {{ $t('auth.followers') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          v-else
          routeName="Home"
          class="nav-link text-dark"
        >
          <i class="fa-solid fa-users"></i>
          {{ $t('auth.followers') }}
        </LocaleRouterLink>
      </li>
      <li class="nav-item">
        <LocaleRouterLink
          v-if="this.$route.name == 'Home'"
          routeName="Home"
          class="nav-link active"
          aria-current="page"
        >
          <i class="fa-solid fa-user-group"></i>
          {{ $t('auth.following') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          v-else
          routeName="Home"
          class="nav-link text-dark"
        >
          <i class="fa-solid fa-user-group"></i>
          {{ $t('auth.following') }}
        </LocaleRouterLink>
      </li>
      <li class="nav-item">
        <LocaleRouterLink
          v-if="this.$route.name == 'Home'"
          routeName="Home"
          class="nav-link active"
          aria-current="page"
        >
          <i class="fa-solid fa-star"></i>
          {{ $t('auth.favorites') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          v-else
          routeName="Home"
          class="nav-link text-dark"
        >
          <i class="fa-solid fa-star"></i>
          {{ $t('auth.favorites') }}
        </LocaleRouterLink>
      </li>
    </ul>
    <div class="text-uppercase fw-bolder text-secondary mt-3">
      {{ $t('auth.account') }}
    </div>
    <ul class="nav nav-pills flex-column">
      <li class="nav-item">
        <LocaleRouterLink
          v-if="this.$route.name == 'Profile'"
          routeName="Profile"
          class="nav-link active"
          aria-current="page"
        >
          <i class="fa-solid fa-user"></i>
          {{ $t('auth.profile.profile') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          v-else
          routeName="Profile"
          class="nav-link text-dark"
        >
          <i class="fa-solid fa-user"></i>
          {{ $t('auth.profile.profile') }}
        </LocaleRouterLink>
      </li>
      <li v-if="userStore.userType == userType.ORGANIZER" class="nav-item">
        <LocaleRouterLink
          v-if="this.$route.name == 'ExternalLinks'"
          routeName="ExternalLinks"
          class="nav-link active"
          aria-current="page"
        >
          <i class="fa-solid fa-link"></i>
          {{ $t('auth.externallinks.external_links') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          v-else
          routeName="ExternalLinks"
          class="nav-link text-dark"
        >
          <i class="fa-solid fa-link"></i>
          {{ $t('auth.externallinks.external_links') }}
        </LocaleRouterLink>
      </li>
      <li v-if="userStore.userType == userType.ORGANIZER" class="nav-item">
        <LocaleRouterLink
          v-if="this.$route.name == 'Home'"
          routeName="Home"
          class="nav-link active"
          aria-current="page"
        >
          <i class="fa-solid fa-briefcase"></i>
          {{ $t('auth.portfolio') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          v-else
          routeName="Home"
          class="nav-link text-dark"
        >
          <i class="fa-solid fa-briefcase"></i>
          {{ $t('auth.portfolio') }}
        </LocaleRouterLink>
      </li>
      <li class="nav-item">
        <LocaleRouterLink
          v-if="this.$route.name == 'PasswordChange'"
          routeName="PasswordChange"
          class="nav-link active"
          aria-current="page"
        >
          <i class="fa-solid fa-key"></i>
          {{ $t('auth.password.change_password') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          v-else
          routeName="PasswordChange"
          class="nav-link text-dark"
        >
          <i class="fa-solid fa-key"></i>
          {{ $t('auth.password.change_password') }}
        </LocaleRouterLink>
      </li>
      <li class="nav-item">
        <LocaleRouterLink
          v-if="this.$route.name == 'Home'"
          routeName="Home"
          class="nav-link active"
          aria-current="page"
        >
          <i class="fa-solid fa-user-xmark"></i>
          {{ $t('auth.delete_profile') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          v-else
          routeName="Home"
          class="nav-link text-dark"
        >
          <i class="fa-solid fa-user-xmark"></i>
          {{ $t('auth.delete_profile') }}
        </LocaleRouterLink>
      </li>
      <li class="nav-item">
        <div
          @click="logout"
          class="nav-link text-dark"
        >
          <i class="fa-solid fa-right-from-bracket"></i>
          {{ $t('auth.log_out') }}
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.account-menu-lg {
  position: -webkit-sticky;
  position: sticky;
  top: 125px;
}
</style>

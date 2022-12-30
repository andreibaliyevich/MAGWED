<script setup>
import axios from 'axios'

import { userType } from '@/config.js'

import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<script>
export default {
  methods: {
    hideAaccountMenu() {
      this.$refs.buttonAaccountMenu.click()
    },
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
  <div class="account-menu">
    <div class="rounded shadow-sm mb-3">
      <button
        ref="buttonAaccountMenu"
        class="btn btn-secondary w-100"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#account-menu"
        aria-expanded="false"
        aria-label="Account menu"
      >
        {{ $t('auth.account_menu') }}
        <i class="fa-solid fa-caret-down ms-1"></i>
      </button>
      <div id="account-menu" class="collapse p-3">
        <div class="text-uppercase fw-bolder text-secondary">
          {{ $t('auth.social') }}
        </div>
        <ul class="nav nav-pills flex-column">
          <li class="nav-item">
            <LocaleRouterLink
              v-if="this.$route.name == 'Notifications'"
              routeName="Notifications"
              @click="hideAaccountMenu"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-bell"></i>
              {{ $t('auth.notifications') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Notifications"
              @click="hideAaccountMenu"
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
              @click="hideAaccountMenu"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-users"></i>
              {{ $t('auth.followers') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Home"
              @click="hideAaccountMenu"
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
              @click="hideAaccountMenu"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-user-group"></i>
              {{ $t('auth.following') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Home"
              @click="hideAaccountMenu"
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
              @click="hideAaccountMenu"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-star"></i>
              {{ $t('auth.favorites') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Home"
              @click="hideAaccountMenu"
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
              @click="hideAaccountMenu"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-user"></i>
              {{ $t('auth.profile.profile') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Profile"
              @click="hideAaccountMenu"
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
              @click="hideAaccountMenu"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-link"></i>
              {{ $t('auth.externallinks.external_links') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="ExternalLinks"
              @click="hideAaccountMenu"
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
              @click="hideAaccountMenu"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-briefcase"></i>
              {{ $t('auth.portfolio') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Home"
              @click="hideAaccountMenu"
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
              @click="hideAaccountMenu"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-key"></i>
              {{ $t('auth.password.change_password') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="PasswordChange"
              @click="hideAaccountMenu"
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
              @click="hideAaccountMenu"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-user-xmark"></i>
              {{ $t('auth.delete_profile') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Home"
              @click="hideAaccountMenu"
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
              {{ $t('auth.logout') }}
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

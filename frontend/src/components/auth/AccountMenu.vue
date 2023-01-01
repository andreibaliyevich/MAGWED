<script setup>
import { userType } from '@/config.js'

import { useLogout } from '@/composables/logout.js'
const { logout } = useLogout()

import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<template>
  <div class="account-menu">
    <div class="rounded shadow-sm">
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
              @click="$refs.buttonAaccountMenu.click()"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-bell"></i>
              {{ $t('auth.notifications') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Notifications"
              @click="$refs.buttonAaccountMenu.click()"
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
              @click="$refs.buttonAaccountMenu.click()"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-users"></i>
              {{ $t('auth.followers') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Home"
              @click="$refs.buttonAaccountMenu.click()"
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
              @click="$refs.buttonAaccountMenu.click()"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-user-group"></i>
              {{ $t('auth.following') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Home"
              @click="$refs.buttonAaccountMenu.click()"
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
              @click="$refs.buttonAaccountMenu.click()"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-star"></i>
              {{ $t('auth.favorites') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Home"
              @click="$refs.buttonAaccountMenu.click()"
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
              @click="$refs.buttonAaccountMenu.click()"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-user"></i>
              {{ $t('auth.profile.profile') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Profile"
              @click="$refs.buttonAaccountMenu.click()"
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
              @click="$refs.buttonAaccountMenu.click()"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-link"></i>
              {{ $t('auth.externallinks.external_links') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="ExternalLinks"
              @click="$refs.buttonAaccountMenu.click()"
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
              @click="$refs.buttonAaccountMenu.click()"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-briefcase"></i>
              {{ $t('auth.portfolio') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Home"
              @click="$refs.buttonAaccountMenu.click()"
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
              @click="$refs.buttonAaccountMenu.click()"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-key"></i>
              {{ $t('auth.password.change_password') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="PasswordChange"
              @click="$refs.buttonAaccountMenu.click()"
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
              @click="$refs.buttonAaccountMenu.click()"
              class="nav-link active"
              aria-current="page"
            >
              <i class="fa-solid fa-user-xmark"></i>
              {{ $t('auth.delete_profile') }}
            </LocaleRouterLink>
            <LocaleRouterLink
              v-else
              routeName="Home"
              @click="$refs.buttonAaccountMenu.click()"
              class="nav-link text-dark"
            >
              <i class="fa-solid fa-user-xmark"></i>
              {{ $t('auth.delete_profile') }}
            </LocaleRouterLink>
          </li>
          <li class="nav-item">
            <div
              @click="logout()"
              class="nav-link text-dark"
            >
              <i class="fa-solid fa-right-from-bracket"></i>
              {{ $t('auth.log_out') }}
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

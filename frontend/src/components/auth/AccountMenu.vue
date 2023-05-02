<script setup>
import { userType } from '@/config.js'
import { useLogout } from '@/composables/logout.js'
import { useUserStore } from '@/stores/user.js'

const { logout } = useLogout()
const userStore = useUserStore()
</script>

<template>
  <div class="account-menu">
    <div class="rounded shadow-sm">
      <button
        ref="buttonAaccountMenu"
        type="button"
        class="btn btn-light border w-100"
        data-bs-toggle="collapse"
        data-bs-target="#account-menu"
        aria-controls="account-menu"
        aria-expanded="false"
      >
        {{ $t('auth.account_menu') }}
        <i class="fa-solid fa-caret-down ms-1"></i>
      </button>
      <div id="account-menu" class="collapse">
        <div class="text-uppercase fw-bolder text-secondary text-center mt-3">
          {{ $t('auth.social') }}
        </div>
        <ul class="nav nav-pills flex-column">
          <li v-if="userStore.userType == userType.ORGANIZER" class="nav-item">
            <LocaleRouterLink
              routeName="Home"
              @click="$refs.buttonAaccountMenu.click()"
              :class="[
                'nav-link',
                {
                  'active': this.$route.name == 'Home',
                  'text-dark': !(this.$route.name == 'Home')
                }
              ]"
            >
              <i class="fa-solid fa-users"></i>
              {{ $t('auth.followers') }}
            </LocaleRouterLink>
          </li>
          <li class="nav-item">
            <LocaleRouterLink
              routeName="Home"
              @click="$refs.buttonAaccountMenu.click()"
              :class="[
                'nav-link',
                {
                  'active': this.$route.name == 'Home',
                  'text-dark': !(this.$route.name == 'Home')
                }
              ]"
            >
              <i class="fa-solid fa-user-group"></i>
              {{ $t('auth.following') }}
            </LocaleRouterLink>
          </li>
          <li class="nav-item">
            <LocaleRouterLink
              routeName="Home"
              @click="$refs.buttonAaccountMenu.click()"
              :class="[
                'nav-link',
                {
                  'active': this.$route.name == 'Home',
                  'text-dark': !(this.$route.name == 'Home')
                }
              ]"
            >
              <i class="fa-solid fa-star"></i>
              {{ $t('auth.favorites') }}
            </LocaleRouterLink>
          </li>
        </ul>
        <div class="text-uppercase fw-bolder text-secondary text-center mt-3">
          {{ $t('auth.account') }}
        </div>
        <ul class="nav nav-pills flex-column">
          <li class="nav-item">
            <LocaleRouterLink
              routeName="Profile"
              @click="$refs.buttonAaccountMenu.click()"
              :class="[
                'nav-link',
                {
                  'active': this.$route.name == 'Profile',
                  'text-dark': !(this.$route.name == 'Profile')
                }
              ]"
            >
              <i class="fa-solid fa-user"></i>
              {{ $t('auth.profile.profile') }}
            </LocaleRouterLink>
          </li>
          <li v-if="userStore.userType == userType.ORGANIZER" class="nav-item">
            <LocaleRouterLink
              routeName="SocialLinks"
              @click="$refs.buttonAaccountMenu.click()"
              :class="[
                'nav-link',
                {
                  'active': this.$route.name == 'SocialLinks',
                  'text-dark': !(this.$route.name == 'SocialLinks')
                }
              ]"
            >
              <i class="fa-solid fa-link"></i>
              {{ $t('auth.sociallinks.social_links') }}
            </LocaleRouterLink>
          </li>
          <li v-if="userStore.userType == userType.ORGANIZER" class="nav-item">
            <LocaleRouterLink
              routeName="Portfolio"
              @click="$refs.buttonAaccountMenu.click()"
              :class="[
                'nav-link',
                {
                  'active': this.$route.name == 'Portfolio'
                    || this.$route.name == 'PortfolioAlbums'
                    || this.$route.name == 'PortfolioPhotos'
                    || this.$route.name == 'PortfolioAlbum',
                  'text-dark': !(this.$route.name == 'Portfolio'
                    || this.$route.name == 'PortfolioAlbums'
                    || this.$route.name == 'PortfolioPhotos'
                    || this.$route.name == 'PortfolioAlbum'
                  )
                }
              ]"
            >
              <i class="fa-solid fa-briefcase"></i>
              {{ $t('auth.portfolio.portfolio') }}
            </LocaleRouterLink>
          </li>
          <li class="nav-item">
            <LocaleRouterLink
              routeName="PasswordChange"
              @click="$refs.buttonAaccountMenu.click()"
              :class="[
                'nav-link',
                {
                  'active': this.$route.name == 'PasswordChange',
                  'text-dark': !(this.$route.name == 'PasswordChange')
                }
              ]"
            >
              <i class="fa-solid fa-key"></i>
              {{ $t('auth.password.change_password') }}
            </LocaleRouterLink>
          </li>
          <li class="nav-item">
            <LocaleRouterLink
              routeName="ProfileDelete"
              @click="$refs.buttonAaccountMenu.click()"
              :class="[
                'nav-link',
                {
                  'active': this.$route.name == 'ProfileDelete',
                  'text-dark': !(this.$route.name == 'ProfileDelete')
                }
              ]"
            >
              <i class="fa-solid fa-user-xmark"></i>
              {{ $t('auth.profile_delete.profile_delete') }}
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

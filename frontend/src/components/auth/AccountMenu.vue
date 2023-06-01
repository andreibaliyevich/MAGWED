<script setup>
import { userType } from '@/config.js'
import { useLogout } from '@/composables/logout.js'
import { useUserStore } from '@/stores/user.js'

const { logout } = useLogout()
const userStore = useUserStore()
</script>

<template>
  <div class="account-menu">
    <button
      type="button"
      class="btn btn-light border w-100 d-lg-none"
      data-bs-toggle="offcanvas"
      data-bs-target="#account-menu"
      aria-controls="account-menu"
    >
      {{ $t('auth.account_menu') }}
      <i class="fa-solid fa-bars"></i>
    </button>
    <div
      id="account-menu"
      tabindex="-1"
      class="offcanvas-lg offcanvas-end"
      aria-labelledby="account-menu-label"
    >
      <div class="offcanvas-header">
        <h5
          id="account-menu-label"
          class="offcanvas-title"
        >
          {{ $t('auth.account_menu') }}
        </h5>
        <button
          ref="accountMenuClose"
          type="button"
          class="btn-close"
          data-bs-dismiss="offcanvas"
          data-bs-target="#account-menu"
          aria-label="Close"
        ></button>
      </div>
      <div class="offcanvas-body d-lg-block">
        <div class="text-uppercase fw-bolder text-secondary">
          {{ $t('auth.social') }}
        </div>
        <ul class="nav nav-pills flex-column">
          <li v-if="userStore.userType == userType.ORGANIZER" class="nav-item">
            <LocaleRouterLink
              routeName="Home"
              @click="$refs.accountMenuClose.click()"
              :class="[
                'nav-link',
                this.$route.name == 'Home' ? 'active' : 'text-dark'
              ]"
            >
              <i class="fa-solid fa-users"></i>
              {{ $t('auth.followers') }}
            </LocaleRouterLink>
          </li>
          <li class="nav-item">
            <LocaleRouterLink
              routeName="Home"
              @click="$refs.accountMenuClose.click()"
              :class="[
                'nav-link',
                this.$route.name == 'Home' ? 'active' : 'text-dark'
              ]"
            >
              <i class="fa-solid fa-user-group"></i>
              {{ $t('auth.following') }}
            </LocaleRouterLink>
          </li>
          <li class="nav-item">
            <LocaleRouterLink
              routeName="Home"
              @click="$refs.accountMenuClose.click()"
              :class="[
                'nav-link',
                this.$route.name == 'Home' ? 'active' : 'text-dark'
              ]"
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
              routeName="Profile"
              @click="$refs.accountMenuClose.click()"
              :class="[
                'nav-link',
                this.$route.name == 'Profile' ? 'active' : 'text-dark'
              ]"
            >
              <i class="fa-solid fa-user"></i>
              {{ $t('profile.profile') }}
            </LocaleRouterLink>
          </li>
          <li v-if="userStore.userType == userType.ORGANIZER" class="nav-item">
            <LocaleRouterLink
              routeName="SocialLinks"
              @click="$refs.accountMenuClose.click()"
              :class="[
                'nav-link',
                this.$route.name == 'SocialLinks' ? 'active' : 'text-dark'
              ]"
            >
              <i class="fa-solid fa-link"></i>
              {{ $t('auth.sociallinks.social_links') }}
            </LocaleRouterLink>
          </li>
          <li v-if="userStore.userType == userType.ORGANIZER" class="nav-item">
            <LocaleRouterLink
              routeName="Portfolio"
              @click="$refs.accountMenuClose.click()"
              :class="[
                'nav-link',
                this.$route.name == 'Portfolio'
                  || this.$route.name == 'PortfolioAlbumList'
                  || this.$route.name == 'PortfolioAlbumDetail'
                  || this.$route.name == 'PortfolioPhotoList'
                  ? 'active'
                  : 'text-dark'
              ]"
            >
              <i class="fa-solid fa-briefcase"></i>
              {{ $t('portfolio.portfolio') }}
            </LocaleRouterLink>
          </li>
          <li class="nav-item">
            <LocaleRouterLink
              routeName="PasswordChange"
              @click="$refs.accountMenuClose.click()"
              :class="[
                'nav-link',
                this.$route.name == 'PasswordChange' ? 'active' : 'text-dark'
              ]"
            >
              <i class="fa-solid fa-key"></i>
              {{ $t('auth.password.change_password') }}
            </LocaleRouterLink>
          </li>
          <li class="nav-item">
            <LocaleRouterLink
              routeName="ProfileDelete"
              @click="$refs.accountMenuClose.click()"
              :class="[
                'nav-link',
                this.$route.name == 'ProfileDelete' ? 'active' : 'text-dark'
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

<script setup>
import { userType } from '@/config.js'
import { useLogout } from '@/composables/logout.js'
import { useUserStore } from '@/stores/user.js'

const { logout } = useLogout()
const userStore = useUserStore()
</script>

<template>
  <div class="account-menu-lg">
    <div class="text-uppercase fw-bolder text-secondary">
      {{ $t('auth.social') }}
    </div>
    <ul class="nav nav-pills flex-column">
      <li v-if="userStore.userType == userType.ORGANIZER" class="nav-item">
        <LocaleRouterLink
          routeName="Home"
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
          {{ $t('auth.portfolio.portfolio') }}
        </LocaleRouterLink>
      </li>
      <li class="nav-item">
        <LocaleRouterLink
          routeName="PasswordChange"
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
</template>

<style scoped>
.account-menu-lg {
  position: -webkit-sticky;
  position: sticky;
  top: 125px;
}
</style>

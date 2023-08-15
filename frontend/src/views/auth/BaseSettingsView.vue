<script setup>
import { RouterView } from 'vue-router'
import { userType } from '@/config.js'
import { useLogout } from '@/composables/logout.js'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()
const { logout } = useLogout()
</script>

<template>
  <div class="base-account-view">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 pt-5 pb-lg-5">
          <button
            type="button"
            class="btn btn-light border w-100 d-lg-none"
            data-bs-toggle="offcanvas"
            data-bs-target="#settings-menu"
            aria-controls="settings-menu"
          >
            {{ $t('auth.settings_menu') }}
            
            <i class="fa-solid fa-sliders"></i>
          </button>
          <div
            id="settings-menu"
            tabindex="-1"
            class="offcanvas-lg offcanvas-end"
            aria-labelledby="settings-menu-label"
          >
            <div class="offcanvas-header">
              <h5
                id="settings-menu-label"
                class="offcanvas-title"
              >
                {{ $t('auth.settings_menu') }}
              </h5>
              <button
                ref="accountMenuClose"
                type="button"
                class="btn-close"
                data-bs-dismiss="offcanvas"
                data-bs-target="#settings-menu"
                aria-label="Close"
              ></button>
            </div>
            <div class="offcanvas-body d-lg-block">
              <div class="d-none d-lg-block text-uppercase fw-bolder text-secondary mb-3">
                {{ $t('auth.settings') }}
              </div>
              <ul class="nav nav-pills flex-column">
                <li
                  :class="[
                    'nav-item',
                    this.$route.name == 'Profile' ? 'active' : null
                  ]"
                >
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
                <li
                  v-if="userStore.userType == userType.ORGANIZER"
                  :class="[
                    'nav-item',
                    this.$route.name == 'SocialLinks' ? 'active' : null
                  ]"
                >
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
                <li
                  v-if="userStore.userType == userType.ORGANIZER"
                  :class="[
                    'nav-item',
                    this.$route.name == 'Portfolio'
                      || this.$route.name == 'PortfolioAlbumList'
                      || this.$route.name == 'PortfolioAlbumDetail'
                      || this.$route.name == 'PortfolioPhotoList'
                      ? 'active'
                      : null
                  ]"
                >
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
                <li
                  :class="[
                    'nav-item',
                    this.$route.name == 'PasswordChange' ? 'active' : null
                  ]"
                >
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
                <li
                  :class="[
                    'nav-item',
                    this.$route.name == 'ProfileDelete' ? 'active' : null
                  ]"
                >
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
        <div class="col-lg-8 py-5 px-lg-5">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media(min-width: 992px) {
  .col-lg-4.pt-5.pb-lg-5 {
    border-right: 1px solid #dee2e6;
  }
  #settings-menu {
    position: -webkit-sticky;
    position: sticky;
    top: 125px;
  }
}
</style>

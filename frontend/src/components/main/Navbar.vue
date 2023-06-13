<script setup>
import { useUserStore } from '@/stores/user.js'
import NavbarSearch from './NavbarSearch.vue'
import NavbarNotifications from './NavbarNotifications.vue'
import NavbarUser from './NavbarUser.vue'

const userStore = useUserStore()
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
    <div class="container py-lg-2">
      <button
        type="button"
        class="navbar-toggler"
        data-bs-toggle="offcanvas"
        data-bs-target="#main-menu"
        aria-controls="main-menu"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <LocaleRouterLink
        routeName="Home"
        class="navbar-brand d-flex d-sm-none align-items-center me-0"
      >
        <img
          src="/logo-navbar.png"
          width="50"
        >
      </LocaleRouterLink>
      <LocaleRouterLink
        routeName="Home"
        class="navbar-brand d-flex d-none d-sm-inline-flex align-items-center me-0"
      >
        <img
          src="/logo-navbar-full.png"
          width="150"
        >
      </LocaleRouterLink>
      <div
        id="main-menu"
        tabindex="-1"
        class="offcanvas offcanvas-start"
        aria-labelledby="offcanvasNavbarLabel"
      >
        <div class="offcanvas-header">
          <h5
            class="offcanvas-title"
            id="offcanvasNavbarLabel"
          >
            {{ $t('nav.menu') }}
          </h5>
          <button
            ref="offcanvasMenuClose"
            type="button"
            class="btn-close text-reset"
            data-bs-dismiss="offcanvas"
            data-bs-target="#main-menu"
            aria-label="Close"
          ></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav d-flex align-items-lg-center flex-grow-1 mx-3">
            <li class="nav-item">
              <LocaleRouterLink
                routeName="OrganizerList"
                @click="$refs.offcanvasMenuClose.click()"
                :class="[
                  'nav-link text-uppercase fw-bold',
                  this.$route.name == 'OrganizerList'
                    || this.$route.name == 'OrganizerDetail'
                    ? 'active'
                    : 'text-dark'
                ]"
              >
                {{ $t('nav.organizers') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item dropdown ms-xl-3">
              <a
                id="nav_link_albums"
                href="#"
                :class="[
                  'nav-link text-uppercase fw-bold',
                  this.$route.name == 'AlbumList'
                    || this.$route.name == 'AlbumDetail'
                    || this.$route.name == 'PhotoList'
                    || this.$route.name == 'PhotoDetail'
                    ? 'active'
                    : 'text-dark'
                ]"
                data-bs-toggle="dropdown"
                data-bs-auto-close="outside"
                aria-expanded="false"
              >
                {{ $t('nav.photos') }}
                <i class="fa-solid fa-angle-down fa-xs"></i>
              </a>
              <ul
                class="dropdown-menu border border-light shadow"
                aria-labelledby="nav_link_albums"
              >
                <li>
                  <LocaleRouterLink
                    routeName="PhotoList"
                    :routeQuery="{ tab: 'popular' }"
                    @click="$refs.offcanvasMenuClose.click()"
                    class="dropdown-item"
                  >
                    {{ $t('nav.popular_photos') }}
                  </LocaleRouterLink>
                </li>
                <li>
                  <LocaleRouterLink
                    routeName="PhotoList"
                    :routeQuery="{ tab: 'fresh' }"
                    @click="$refs.offcanvasMenuClose.click()"
                    class="dropdown-item"
                  >
                    {{ $t('nav.fresh_photos') }}
                  </LocaleRouterLink>
                </li>
                <li>
                  <LocaleRouterLink
                    routeName="PhotoList"
                    :routeQuery="{ tab: 'editors' }"
                    @click="$refs.offcanvasMenuClose.click()"
                    class="dropdown-item"
                  >
                    {{ $t('nav.editors_choice') }}
                  </LocaleRouterLink>
                </li>
                <li>
                  <LocaleRouterLink
                    routeName="AlbumList"
                    :routeQuery="{ tab: 'popular' }"
                    @click="$refs.offcanvasMenuClose.click()"
                    class="dropdown-item"
                  >
                    {{ $t('nav.photo_albums') }}
                  </LocaleRouterLink>
                </li>
              </ul>
            </li>
            <li class="nav-item ms-xl-3">
              <LocaleRouterLink
                routeName="Home"
                @click="$refs.offcanvasMenuClose.click()"
                :class="[
                  'nav-link text-uppercase fw-bold',
                  this.$route.name == 'Home' ? 'active' : 'text-dark'
                ]"
              >
                {{ $t('nav.awards') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item ms-xl-3">
              <LocaleRouterLink
                routeName="Blog"
                @click="$refs.offcanvasMenuClose.click()"
                :class="[
                  'nav-link text-uppercase fw-bold',
                  this.$route.name == 'Blog' ? 'active' : 'text-dark'
                ]"
              >
                {{ $t('nav.blog') }}
              </LocaleRouterLink>
            </li>
          </ul>
        </div>
      </div>
      <NavbarSearch />
      <div
        v-if="userStore.isLoggedIn"
        class="d-flex align-items-center gap-3 ms-lg-3"
      >
        <NavbarNotifications />
        <NavbarUser />
      </div>
      <div
        v-else
        class="d-flex align-items-center ms-lg-3"
      >
        <LocaleRouterLink
          routeName="Login"
          @click="$refs.offcanvasMenuClose.click()"
          class="btn btn-outline-brand border-secondary rounded-pill px-3"
        >
          {{ $t('auth.log_in') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          routeName="Registration"
          @click="$refs.offcanvasMenuClose.click()"
          class="btn btn-brand rounded-pill px-3 ms-1 d-flex d-none d-md-inline-flex"
        >
          {{ $t('auth.register') }}
        </LocaleRouterLink>
      </div>
    </div>
  </nav>
</template>

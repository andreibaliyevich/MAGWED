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
        class="navbar-toggler"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasMenu"
        aria-controls="offcanvasMenu"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <LocaleRouterLink
        routeName="Home"
        class="navbar-brand d-flex d-sm-none align-items-center me-0"
      >
        <img
          src="/logo-navbar.png"
          width="53"
        >
      </LocaleRouterLink>
      <LocaleRouterLink
        routeName="Home"
        class="navbar-brand d-flex d-none d-sm-inline-flex align-items-center me-0"
      >
        <img
          src="/logo-navbar-full.png"
          width="190"
        >
      </LocaleRouterLink>
      <div
        class="offcanvas offcanvas-start"
        tabindex="-1"
        id="offcanvasMenu"
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
            ref="offcanvasClose"
            type="button"
            class="btn-close text-reset"
            data-bs-dismiss="offcanvas"
            aria-label="Close"
          ></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav d-flex align-items-lg-center flex-grow-1 mx-3">
            <li class="nav-item">
              <LocaleRouterLink
                routeName="OrganizerList"
                @click="$refs.offcanvasClose.click()"
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
                href="#"
                :class="[
                  'nav-link text-uppercase fw-bold',
                  this.$route.name == 'Home' ? 'active' : 'text-dark'
                ]"
                data-bs-toggle="dropdown"
                data-bs-auto-close="outside"
                aria-expanded="false"
              >
                {{ $t('nav.places') }}
                <i class="fa-solid fa-angle-down fa-xs"></i>
              </a>
              <ul class="dropdown-menu border border-light shadow">
                <li><a class="dropdown-item" href="#">Action</a></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li><a class="dropdown-item" href="#">Something else here</a></li>
              </ul>
            </li>
            <li class="nav-item ms-xl-3">
              <LocaleRouterLink
                routeName="Home"
                @click="$refs.offcanvasClose.click()"
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
                @click="$refs.offcanvasClose.click()"
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
          @click="$refs.offcanvasClose.click()"
          class="btn btn-outline-brand border-secondary rounded-pill px-3"
        >
          {{ $t('auth.log_in') }}
        </LocaleRouterLink>
        <LocaleRouterLink
          routeName="Registration"
          @click="$refs.offcanvasClose.click()"
          class="btn btn-brand rounded-pill px-3 ms-1 d-flex d-none d-md-inline-flex"
        >
          {{ $t('auth.register') }}
        </LocaleRouterLink>
      </div>
    </div>
  </nav>
</template>

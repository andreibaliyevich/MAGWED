<script setup>
import { useUserStore } from '@/stores/user.js'
import NavBarNotifications from './NavBarNotifications.vue'
import NavBarUser from './NavBarUser.vue'

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
            <li class="nav-item text-uppercase fw-bold">
              <LocaleRouterLink
                v-if="this.$route.name == 'Home'"
                routeName="Home"
                @click="$refs.offcanvasClose.click()"
                class="nav-link active"
                aria-current="page"
              >
                {{ $t('nav.best') }}
              </LocaleRouterLink>
              <LocaleRouterLink
                v-else
                routeName="Home"
                @click="$refs.offcanvasClose.click()"
                class="nav-link text-dark"
              >
                {{ $t('nav.best') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item text-uppercase fw-bold ms-xl-3">
              <LocaleRouterLink
                v-if="this.$route.name == 'Home'"
                routeName="Home"
                @click="$refs.offcanvasClose.click()"
                class="nav-link active"
                aria-current="page"
              >
                {{ $t('nav.places') }}
              </LocaleRouterLink>
              <LocaleRouterLink
                v-else
                routeName="Home"
                @click="$refs.offcanvasClose.click()"
                class="nav-link text-dark"
              >
                {{ $t('nav.places') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item text-uppercase fw-bold ms-xl-3">
              <LocaleRouterLink
                v-if="this.$route.name == 'Home'"
                routeName="Home"
                @click="$refs.offcanvasClose.click()"
                class="nav-link active"
                aria-current="page"
              >
                {{ $t('nav.awards') }}
              </LocaleRouterLink>
              <LocaleRouterLink
                v-else
                routeName="Home"
                @click="$refs.offcanvasClose.click()"
                class="nav-link text-dark"
              >
                {{ $t('nav.awards') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item text-uppercase fw-bold ms-xl-3">
              <LocaleRouterLink
                v-if="this.$route.name == 'Blog'"
                routeName="Blog"
                @click="$refs.offcanvasClose.click()"
                class="nav-link active"
                aria-current="page"
              >
                {{ $t('nav.blog') }}
              </LocaleRouterLink>
              <LocaleRouterLink
                v-else
                routeName="Blog"
                @click="$refs.offcanvasClose.click()"
                class="nav-link text-dark"
              >
                {{ $t('nav.blog') }}
              </LocaleRouterLink>
            </li>
          </ul>
          <div class="dropdown mt-3 mt-lg-0">
            <form
              class="d-flex align-items-center border rounded-pill"
              id="dropdownSearch"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <span class="text-secondary ms-2">
                <i class="fa-solid fa-magnifying-glass"></i>
              </span>
              <input
                class="form-control rounded-pill border-0 shadow-none m-1"
                id="search"
                type="search"
                placeholder="Search..."
                aria-label="Search"
                autocomplete="off"
              >
            </form>
            <ul
              class="dropdown-menu shadow w-100 overflow-auto"
              aria-labelledby="dropdownSearch"
            >
              <li><a class="dropdown-item" href="#">Search Result 1</a></li>
              <li><a class="dropdown-item" href="#">Search Result 2</a></li>
              <li><a class="dropdown-item" href="#">Search Result 3</a></li>
              <li><a class="dropdown-item" href="#">Search Result 4</a></li>
              <li><a class="dropdown-item" href="#">Search Result 5 (Extended, Extended, Extended)</a></li>
              <li><a class="dropdown-item" href="#">Search Result 6</a></li>
              <li><a class="dropdown-item" href="#">Search Result 7</a></li>
              <li><a class="dropdown-item" href="#">Search Result 8</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div
        v-if="userStore.isLoggedIn"
        class="d-flex align-items-center"
      >
        <div class="ms-lg-3">
          <LocaleRouterLink
            routeName="Messenger"
            class="link-secondary position-relative"
          >
            <i class="fa-solid fa-message fa-lg"></i>
            <span class="position-absolute top-0 start-100 translate-middle p-1 bg-danger rounded-circle">
              <span class="visually-hidden">New messages</span>
            </span>
          </LocaleRouterLink>
        </div>
        <NavBarNotifications />
        <NavBarUser />
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

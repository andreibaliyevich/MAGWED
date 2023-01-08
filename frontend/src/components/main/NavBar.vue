<script setup>
import { API_URL, userType } from '@/config.js'
import { useLogout } from '@/composables/logout.js'
import { useUserStore } from '@/stores/user.js'

const { logout } = useLogout()
const user = useUserStore()
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
        v-if="user.isLoggedIn"
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
        <div class="dropdown ms-3">
          <a
            class="link-secondary position-relative"
            href="#"
            role="button"
            id="dropdownNotifications"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <i class="fa-solid fa-bell fa-lg"></i>
            <span class="position-absolute top-0 start-100 translate-middle p-1 bg-danger rounded-circle">
              <span class="visually-hidden">New notifications</span>
            </span>
          </a>
          <ul
            class="dropdown-menu dropdown-menu-end shadow w-100 overflow-auto"
            aria-labelledby="dropdownNotifications"
          >
            <li><a class="dropdown-item" href="#">Notifications 1</a></li>
            <li><a class="dropdown-item" href="#">Notifications 2</a></li>
            <li><a class="dropdown-item" href="#">Notifications 3</a></li>
            <li><a class="dropdown-item" href="#">Notifications 4</a></li>
            <li><a class="dropdown-item" href="#">Notifications 5 (Extended, Extended, Extended)</a></li>
            <li><a class="dropdown-item" href="#">Notifications 6</a></li>
            <li><a class="dropdown-item" href="#">Notifications 7</a></li>
            <li><a class="dropdown-item" href="#">Notifications 8</a></li>
          </ul>
        </div>
        <div class="dropdown ms-3">
          <a
            ref="dropdownUser"
            id="dropdownUser"
            href="#"
            class="d-flex align-items-center text-decoration-none text-decoration-none text-dark"
            data-bs-toggle="dropdown"
            data-bs-auto-close="outside"
            aria-expanded="false"
          >
            <img
              v-if="user.avatar"
              :src="`${ API_URL }${ user.avatar }`"
              class="rounded-circle"
              width="32"
              height="32"
              alt="avatar"
            >
            <img
              v-else
              src="/user-avatar.jpg"
              class="rounded-circle"
              width="32"
              height="32"
              alt="avatar"
            >
          </a>
          <ul
            class="dropdown-menu dropdown-menu-end shadow"
            aria-labelledby="dropdownUser"
          >
            <li class="px-3 pt-2 pb-3">
              <div class="d-flex gap-2 align-items-center mb-1">
                <img
                  v-if="user.avatar"
                  :src="`${ API_URL }${ user.avatar }`"
                  class="rounded-circle"
                  width="48"
                  height="48"
                  alt="avatar"
                >
                <img
                  v-else
                  src="/user-avatar.jpg"
                  class="rounded-circle"
                  width="48"
                  height="48"
                  alt="avatar"
                >
                <div class="ms-1">
                  <span class="d-flex flex-nowrap fw-bolder">
                    {{ user.name }}
                  </span>
                  <small class="text-muted">
                    {{ user.email }}
                  </small>
                </div>
              </div>
              <LocaleRouterLink
                routeName="Profile"
                @click="$refs.dropdownUser.click()"
                class="w-100 btn btn-light-brand btn-sm text-center"
              >
                {{ $t('auth.profile.edit_profile') }}
              </LocaleRouterLink>
            </li>
            <li>
              <LocaleRouterLink
                v-if="user.userType == userType.ORGANIZER"
                routeName="Home"
                @click="$refs.dropdownUser.click()"
                class="dropdown-item d-flex gap-2 align-items-center"
              >
                <i class="fa-solid fa-users"></i>
                {{ $t('auth.followers') }}
              </LocaleRouterLink>
              <LocaleRouterLink
                routeName="Home"
                @click="$refs.dropdownUser.click()"
                class="dropdown-item d-flex gap-2 align-items-center"
              >
                <i class="fa-solid fa-user-group"></i>
                {{ $t('auth.following') }}
              </LocaleRouterLink>
              <LocaleRouterLink
                routeName="Home"
                @click="$refs.dropdownUser.click()"
                class="dropdown-item d-flex gap-2 align-items-center"
              >
                <i class="fa-solid fa-star"></i>
                {{ $t('auth.favorites') }}
              </LocaleRouterLink>
              <LocaleRouterLink
                routeName="Home"
                @click="$refs.dropdownUser.click()"
                class="dropdown-item d-flex gap-2 align-items-center"
              >
                <i class="fa-solid fa-comment-dots"></i>
                {{ $t('footer.feedback') }}
              </LocaleRouterLink>
            </li>
            <li><hr class="dropdown-divider"></li>
            <li>
              <div
                @click="logout()"
                class="dropdown-item d-flex gap-2 align-items-center"
              >
                <i class="fa-solid fa-right-from-bracket"></i>
                {{ $t('auth.log_out') }}
              </div>
            </li>
          </ul>
        </div>
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

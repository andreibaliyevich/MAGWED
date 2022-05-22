<script setup>
import { RouterLink } from 'vue-router'
import axios from 'axios'

import { useBaseStore } from '@/stores/base.js'
import { useUserStore } from '@/stores/user.js'
const baseStore = useBaseStore()
const userStore = useUserStore()
</script>

<script>
export default {
  methods: {
    hideOffcanvas() {
      document.getElementById("offcanvasClose").click()
    },
    logout() {
      axios.post('/en/accounts/auth/logout/')
      .then(() => {
        window.localStorage.removeItem('user')
        window.location.reload()
      })
    }
  }
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
    <div class="container py-lg-2">
      <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasMenu" aria-controls="offcanvasMenu">
        <span class="navbar-toggler-icon"></span>
      </button>
      <RouterLink class="navbar-brand d-flex d-sm-none align-items-center me-0" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
        <img width="53" src="/logo-navbar.png">
      </RouterLink>
      <RouterLink class="navbar-brand d-flex d-none d-sm-inline-flex align-items-center me-0" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
        <img width="190" src="/logo-navbar-full.png">
      </RouterLink>
      <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasMenu" aria-labelledby="offcanvasNavbarLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Menu</h5>
          <button id="offcanvasClose" type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav d-flex align-items-lg-center flex-grow-1 mx-3">
            <li class="nav-item text-uppercase fw-bold">
              <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('nav.best') }}</RouterLink>
              <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('nav.best') }}</RouterLink>
            </li>
            <li class="nav-item text-uppercase fw-bold ms-xl-3">
              <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('nav.places') }}</RouterLink>
              <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('nav.places') }}</RouterLink>
            </li>
            <li class="nav-item text-uppercase fw-bold ms-xl-3">
              <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('nav.awards') }}</RouterLink>
              <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('nav.awards') }}</RouterLink>
            </li>
            <li class="nav-item text-uppercase fw-bold ms-xl-3">
              <RouterLink v-if="this.$route.name == 'Blog'" class="nav-link active" aria-current="page" :to="{ name: 'Blog', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('nav.blog') }}</RouterLink>
              <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Blog', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('nav.blog') }}</RouterLink>
            </li>
          </ul>
          <div class="dropdown mt-3 mt-lg-0">
            <form class="d-flex align-items-center border rounded-pill" id="dropdownSearch" data-bs-toggle="dropdown" aria-expanded="false">
              <span class="text-secondary ms-2"><i class="fa-solid fa-magnifying-glass"></i></span>
              <input class="form-control rounded-pill border-0 shadow-none m-1" id="search" type="search" placeholder="Search..." aria-label="Search" autocomplete="off">
            </form>
            <ul class="dropdown-menu shadow w-100 overflow-auto" aria-labelledby="dropdownSearch">
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
      <div v-if="userStore.isLoggedIn" class="d-flex align-items-center">
        <div class="ms-lg-3">
          <RouterLink class="link-secondary position-relative" :to="{ name: 'Messenger', params: { locale: `${ $i18n.locale }` }}">
            <i class="fa-solid fa-message fa-lg"></i>
            <span class="position-absolute top-0 start-100 translate-middle p-1 bg-danger rounded-circle">
              <span class="visually-hidden">New messages</span>
            </span>
          </RouterLink>
        </div>
        <div class="dropdown ms-3">
          <a class="link-secondary position-relative" href="#" role="button" id="dropdownNotifications" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="fa-solid fa-bell fa-lg"></i>
            <span class="position-absolute top-0 start-100 translate-middle p-1 bg-danger rounded-circle">
              <span class="visually-hidden">New notifications</span>
            </span>
          </a>
          <ul class="dropdown-menu dropdown-menu-end shadow w-100 overflow-auto" aria-labelledby="dropdownNotifications">
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
          <a href="#" class="d-flex align-items-center text-decoration-none text-decoration-none text-dark" id="dropdownUser" data-bs-toggle="dropdown" aria-expanded="false">
            <img v-if="userStore.avatar" :src="`${ baseStore.apiURL }${ userStore.avatar }`" class="rounded-circle" width="32" height="32" alt="avatar">
            <img v-else src="/avatar.jpg" class="rounded-circle" width="32" height="32" alt="avatar">
          </a>
          <ul class="dropdown-menu dropdown-menu-end shadow" aria-labelledby="dropdownUser">
            <li>
              <RouterLink v-if="this.$route.name == 'Profile'" class="dropdown-item d-flex gap-2 align-items-center active" :to="{ name: 'Profile', params: { locale: `${ $i18n.locale }` }}">
                <i class="fa-solid fa-user"></i>
                {{ $t('auth.profile.profile') }}
              </RouterLink>
              <RouterLink v-else class="dropdown-item d-flex gap-2 align-items-center" :to="{ name: 'Profile', params: { locale: `${ $i18n.locale }` }}">
                <i class="fa-solid fa-user"></i>
                {{ $t('auth.profile.profile') }}
              </RouterLink>
            </li>
            <li><hr class="dropdown-divider"></li>
            <li>
              <div class="dropdown-item d-flex gap-2 align-items-center" @click="logout">
                <i class="fa-solid fa-right-from-bracket"></i>
                {{ $t('auth.logout') }}
              </div>
            </li>
          </ul>
        </div>
      </div>
      <div v-else class="d-flex align-items-center ms-lg-3">
        <RouterLink class="btn btn-outline-brand border-secondary rounded-pill px-3" :to="{ name: 'Login', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('auth.login') }}</RouterLink>
        <RouterLink class="btn btn-brand rounded-pill px-3 ms-1 d-flex d-none d-md-inline-flex" :to="{ name: 'Registration', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('auth.registration') }}</RouterLink>
      </div>
    </div>
  </nav>
</template>

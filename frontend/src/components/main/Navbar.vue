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
        data-bs-target="#main_menu"
        aria-controls="main_menu"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <router-link
        :to="{
          name: 'Home',
          params: { locale: $i18n.locale }
        }"
        class="navbar-brand d-flex d-sm-none align-items-center me-0"
      >
        <img
          src="/logo-navbar.png"
          width="50"
        >
      </router-link>
      <router-link
        :to="{
          name: 'Home',
          params: { locale: $i18n.locale }
        }"
        class="navbar-brand d-flex d-none d-sm-inline-flex align-items-center me-0"
      >
        <img
          src="/logo-navbar-full.png"
          width="150"
        >
      </router-link>
      <div
        id="main_menu"
        tabindex="-1"
        class="offcanvas offcanvas-start"
        aria-labelledby="main_menu_label"
      >
        <div class="offcanvas-header border-bottom">
          <h5
            class="offcanvas-title"
            id="main_menu_label"
          >
            {{ $t('nav.menu') }}
          </h5>
          <button
            ref="offcanvasMenuClose"
            type="button"
            class="btn-close text-reset"
            data-bs-dismiss="offcanvas"
            data-bs-target="#main_menu"
            aria-label="Close"
          ></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav d-flex align-items-lg-center flex-grow-1 mx-3">
            <li class="nav-item">
              <router-link
                :to="{
                  name: 'OrganizerList',
                  params: { locale: $i18n.locale }
                }"
                @click="$refs.offcanvasMenuClose.click()"
                :class="[
                  'nav-link text-uppercase fw-bold',
                  $route.name === 'OrganizerList'
                    || $route.name === 'OrganizerDetail'
                    ? 'active'
                    : 'text-dark'
                ]"
              >
                {{ $t('nav.organizers') }}
              </router-link>
            </li>
            <li class="nav-item dropdown ms-xl-3">
              <a
                id="nav_link_albums"
                href="#"
                :class="[
                  'nav-link text-uppercase fw-bold',
                  $route.name === 'AlbumList'
                    || $route.name === 'AlbumDetail'
                    || $route.name === 'PhotoList'
                    || $route.name === 'PhotoDetail'
                    ? 'active'
                    : 'text-dark'
                ]"
                data-bs-toggle="dropdown"
                data-bs-auto-close="true"
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
                  <router-link
                    :to="{
                      name: 'PhotoList',
                      params: { locale: $i18n.locale },
                      query: { tab: 'popular' }
                    }"
                    @click="$refs.offcanvasMenuClose.click()"
                    class="dropdown-item"
                  >
                    {{ $t('nav.popular_photos') }}
                  </router-link>
                </li>
                <li>
                  <router-link
                    :to="{
                      name: 'PhotoList',
                      params: { locale: $i18n.locale },
                      query: { tab: 'fresh' }
                    }"
                    @click="$refs.offcanvasMenuClose.click()"
                    class="dropdown-item"
                  >
                    {{ $t('nav.fresh_photos') }}
                  </router-link>
                </li>
                <li>
                  <router-link
                    :to="{
                      name: 'PhotoList',
                      params: { locale: $i18n.locale },
                      query: { tab: 'editors' }
                    }"
                    @click="$refs.offcanvasMenuClose.click()"
                    class="dropdown-item"
                  >
                    {{ $t('nav.editors_choice') }}
                  </router-link>
                </li>
                <li>
                  <router-link
                    :to="{
                      name: 'AlbumList',
                      params: { locale: $i18n.locale },
                      query: { tab: 'popular' }
                    }"
                    @click="$refs.offcanvasMenuClose.click()"
                    class="dropdown-item"
                  >
                    {{ $t('nav.photo_albums') }}
                  </router-link>
                </li>
              </ul>
            </li>
            <li class="nav-item ms-xl-3">
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                @click="$refs.offcanvasMenuClose.click()"
                :class="[
                  'nav-link text-uppercase fw-bold',
                  $route.name === 'Home' ? 'active' : 'text-dark'
                ]"
              >
                {{ $t('nav.awards') }}
              </router-link>
            </li>
            <li class="nav-item ms-xl-3">
              <router-link
                :to="{
                  name: 'ArticleList',
                  params: { locale: $i18n.locale }
                }"
                @click="$refs.offcanvasMenuClose.click()"
                :class="[
                  'nav-link text-uppercase fw-bold',
                  $route.name === 'ArticleList'
                    || $route.name === 'ArticleDetail'
                    ? 'active'
                    : 'text-dark'
                ]"
              >
                {{ $t('nav.blog') }}
              </router-link>
            </li>
          </ul>
        </div>
      </div>
      <div class="d-flex align-items-center gap-3">
        <NavbarSearch />
        <div
          v-if="userStore.isLoggedIn"
          class="d-flex align-items-center gap-3"
        >
          <NavbarNotifications />
          <NavbarUser />
        </div>
        <div
          v-else
          class="d-flex align-items-center gap-1"
        >
          <router-link
            :to="{
              name: 'Login',
              params: { locale: $i18n.locale }
            }"
            class="btn btn-outline-brand border-secondary rounded-pill px-3"
          >
            {{ $t('auth.log_in') }}
          </router-link>
          <router-link
            :to="{
              name: 'Registration',
              params: { locale: $i18n.locale }
            }"
            class="btn btn-brand rounded-pill d-none d-md-inline-flex px-3"
          >
            {{ $t('auth.register') }}
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<script>
export default {
  methods: {
    hideOffcanvas() {
      document.getElementById("offcanvasClose").click()
    }
  }
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
    <div class="container py-1 py-lg-3">
      <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar">
        <span class="navbar-toggler-icon"></span>
      </button>
      <RouterLink class="navbar-brand" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">
        <img width="190" src="/logo-navbar.png">
      </RouterLink>

      <div class="w-100 d-flex d-none d-lg-inline-flex mx-3">
        <form class="input-group border rounded-pill d-flex align-items-center">
          <label class="text-secondary ms-2" for="search-lg"><i class="fa-solid fa-magnifying-glass"></i></label>
          <input class="form-control rounded-pill border-0 shadow-none m-1" id="search-lg" type="search" placeholder="Search..." aria-label="Search">
        </form>
      </div>

      <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Menu</h5>
          <button id="offcanvasClose" type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <div class="d-flex d-lg-none">
            <form class="input-group border rounded-pill d-flex align-items-center">
              <label class="text-secondary ms-2" for="search-sm"><i class="fa-solid fa-magnifying-glass"></i></label>
              <input class="form-control rounded-pill border-0 shadow-none m-1" id="search-sm" type="search" placeholder="Search..." aria-label="Search">
            </form>
          </div>
          <ul class="navbar-nav justify-content-end flex-grow-1 ms-1">
            <li class="nav-item text-uppercase fw-bold">
              <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">Лучшие</RouterLink>
              <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">Лучшие</RouterLink>
            </li>
            <li class="nav-item text-uppercase fw-bold ms-lg-3">
              <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">Места</RouterLink>
              <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">Места</RouterLink>
            </li>
            <li class="nav-item text-uppercase fw-bold ms-lg-3">
              <RouterLink v-if="this.$route.name == 'Home'" class="nav-link active" aria-current="page" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">Awards</RouterLink>
              <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">Awards</RouterLink>
            </li>
            <li class="nav-item text-uppercase fw-bold ms-lg-3">
              <RouterLink v-if="this.$route.name == 'Blog'" class="nav-link active" aria-current="page" :to="{ name: 'Blog', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('blog.blog') }}</RouterLink>
              <RouterLink v-else class="nav-link text-dark" :to="{ name: 'Blog', params: { locale: `${ $i18n.locale }` }}" @click="hideOffcanvas">{{ $t('blog.blog') }}</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

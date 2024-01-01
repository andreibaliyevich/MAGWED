<script setup>
import PortfolioPhotoList from '@/components/auth/PortfolioPhotoList.vue'
</script>

<template>
  <div class="portfolio-photo-list-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <div class="d-flex align-items-center mb-5">
        <router-link
          :to="{ name: 'Portfolio' }"
          class="link-danger text-decoration-none display-6"
        >
          {{ $t('portfolio.portfolio') }}
        </router-link>
        <i class="fa-solid fa-chevron-right mt-2 mx-2"></i>
        <h1 class="display-6 mb-0">
          {{ $t('portfolio.photos') }}
        </h1>
      </div>
      <PortfolioPhotoList />
    </div>
  </div>
</template>

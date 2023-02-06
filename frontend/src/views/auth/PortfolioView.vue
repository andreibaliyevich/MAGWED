<script setup>
import { ref } from 'vue'
import PortfolioAlbums from '@/components/auth/PortfolioAlbums.vue'
import PortfolioPhotos from '@/components/auth/PortfolioPhotos.vue'

const viewAlbums = ref(true)
</script>

<template>
  <div class="portfolio-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">
        {{ $t('auth.portfolio.portfolio') }}
      </h1>

      <ul class="nav nav-tabs nav-fill">
        <li class="nav-item">
          <a
            v-if="viewAlbums"
            href="#"
            class="nav-link active"
            aria-current="true"
          >
            {{ $t('auth.portfolio.albums') }}
          </a>
          <a
            v-else
            @click="viewAlbums=true"
            href="#"
            class="nav-link"
          >
            {{ $t('auth.portfolio.albums') }}
          </a>
        </li>
        <li class="nav-item">
          <a
            v-if="viewAlbums"
            @click="viewAlbums=false"
            href="#"
            class="nav-link"
          >
            {{ $t('auth.portfolio.photos') }}
          </a>
          <a
            v-else
            href="#"
            class="nav-link active"
            aria-current="true"
          >
            {{ $t('auth.portfolio.photos') }}
          </a>
        </li>
      </ul>

      <PortfolioAlbums v-if="viewAlbums" />
      <PortfolioPhotos v-else />
    </div>
  </div>
</template>

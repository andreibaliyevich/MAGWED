<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { locale } = useI18n({ useScope: 'global' })

const viewAlbums = ref(true)

const goAddAlbum = () => {
  router.push({
    name: 'PortfolioAddAlbum',
    params: { locale: locale.value }
  })
}

const goAddPhoto = () => {
  router.push({
    name: 'PortfolioAddPhoto',
    params: { locale: locale.value }
  })
}
</script>

<template>
  <div class="portfolio-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">
        {{ $t('auth.portfolio.portfolio') }}
      </h1>

      <ul class="nav nav-tabs nav-fill mb-3">
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

      <button
        v-if="viewAlbums"
        @click="goAddAlbum()"
        class="btn btn-brand"
        type="button"
      >
        {{ $t('modal.add') }}
      </button>
      <button
        v-else
        @click="goAddPhoto()"
        class="btn btn-brand"
        type="button"
      >
        {{ $t('modal.add') }}
      </button>
    </div>
  </div>
</template>

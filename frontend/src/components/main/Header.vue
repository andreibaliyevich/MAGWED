<script setup>
import { RouterLink } from 'vue-router'
import { ref } from 'vue'
import { LANGUAGES, CURRENCIES } from '@/config.js'
import { useCurrencyStore } from '@/stores/currency.js'

const currencyStore = useCurrencyStore()
const currencyLi = ref(null)

const changeCurrency = (event) => {
  window.localStorage.setItem('currency', event.target.value)
  currencyStore.setCurrency(event.target.value)
  currencyLi.value.click()
}
</script>

<template>
  <header class="bg-dark text-white py-2">
    <div class="container">
      <div class="d-flex justify-content-between">
        <div class="d-flex align-items-center">
          <a
            class="text-white link-facebook"
            href="https://www.facebook.com/"
            target="_blank"
          >
            <i class="fa-brands fa-facebook-f"></i>
          </a>
          <a
            class="text-white link-twitter ms-2"
            href="https://twitter.com/"
            target="_blank"
          >
            <i class="fa-brands fa-twitter"></i>
          </a>
          <a
            class="text-white link-instagram ms-2"
            href="https://www.instagram.com/"
            target="_blank"
          >
            <i class="fa-brands fa-instagram"></i>
          </a>
          <a
            class="text-white link-linkedin ms-2"
            href="https://www.linkedin.com/"
            target="_blank"
          >
            <i class="fa-brands fa-linkedin"></i>
          </a>
          <a
            class="text-white link-spotify ms-2"
            href="https://www.spotify.com/"
            target="_blank"
          >
            <i class="fa-brands fa-spotify"></i>
          </a>
          <a
            class="text-white link-youtube ms-2"
            href="https://www.youtube.com/"
            target="_blank"
          >
            <i class="fa-brands fa-youtube"></i>
          </a>
          <a
            class="text-white link-soundcloud ms-2"
            href="https://soundcloud.com/"
            target="_blank"
          >
            <i class="fa-brands fa-soundcloud"></i>
          </a>
          <a
            class="text-white link-pinterest ms-2"
            href="https://www.pinterest.com/"
            target="_blank"
          >
            <i class="fa-brands fa-pinterest"></i>
          </a>
          <a
            class="text-white link-vk ms-2"
            href="https://vk.com/"
            target="_blank"
          >
            <i class="fa-brands fa-vk"></i>
          </a>
        </div>
        <div class="dropdown d-flex align-items-center">
          <a
            id="locale_dropdown"
            href="#"
            role="button"
            class="dropdown-toggle d-flex align-items-center text-decoration-none text-white"
            data-bs-toggle="dropdown"
            data-bs-auto-close="true"
            aria-expanded="false"
          >
            <img
              :src="`/flags/${$i18n.locale}.png`"
              width="20"
              :alt="$i18n.locale"
            >
            <span class="text-uppercase ms-1">
              {{ $i18n.locale }} / {{ currencyStore.currencyValue }}
            </span>
          </a>
          <ul
            class="dropdown-menu dropdown-menu-end border border-light shadow z-index-1050"
            aria-labelledby="locale_dropdown"
          >
            <li
              ref="currencyLi"
              class="dropdown-item"
            >
              <select
                :value="currencyStore.currencyValue"
                @change="changeCurrency"
                class="form-select"
              >
                <option
                  v-for="currency in CURRENCIES"
                  :key="currency.value"
                  :value="currency.value"
                >
                  {{ currency.text }} {{ currency.value }}
                </option>
              </select>
            </li>
            <li
              v-for="language in LANGUAGES"
              :key="language.value"
            >
              <RouterLink
                :to="{ params: { locale: language.value }}"
                class="dropdown-item"
                >
                <img
                  :src="`/flags/${language.value}.png`"
                  width="20"
                  :alt="language.value"
                >
                <span class="ms-1">{{ language.text }}</span>
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </header>
</template>

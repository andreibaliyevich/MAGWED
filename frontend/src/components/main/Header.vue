<script setup>
import { RouterLink } from 'vue-router'

import { useMainStore } from '@/stores/main.js'
const mainStore = useMainStore()
</script>

<script>
export default {
  methods: {
    changeCurrency(event) {
      window.localStorage.setItem('currency', event.target.value)
      this.mainStore.setCurrency(event.target.value)
      this.$refs.currencyList.click()
    }
  }
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
          <a
            class="text-white link-linkedin ms-2"
            href="https://www.linkedin.com/"
            target="_blank"
          >
            <i class="fa-brands fa-linkedin"></i>
          </a>
        </div>
        <div class="d-flex">
          <div class="dropdown d-flex align-items-center">
            <a
              class="dropdown-toggle d-flex align-items-center text-decoration-none text-white"
              href="#"
              role="button"
              id="dropdownLocale"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <img
                :src="'/flags/' + $i18n.locale + '.png'"
                width="20"
                :alt="$i18n.locale"
              >
              <span class="text-uppercase ms-1">
                {{ $i18n.locale }} / {{ mainStore.currency }}
              </span>
            </a>
            <ul
              class="dropdown-menu dropdown-menu-end"
              aria-labelledby="dropdownLocale"
            >
              <li
                ref="currencyList"
                class="dropdown-item"
              >
                <select
                  :value="mainStore.currency"
                  @change="changeCurrency"
                  class="form-select"
                >
                  <option value="USD">$ USD</option>
                  <option value="EUR">€ EUR</option>
                  <option value="RUB">₽ RUB</option>
                  <option value="BYN">Br BYN</option>
                  <option value="UAH">₴ UAH</option>
                </select>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ params: { locale: 'en' }}">
                  <img src="/flags/en.png" width="20" alt="en">
                  <span class="ms-1">English</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ params: { locale: 'ru' }}">
                  <img src="/flags/ru.png" width="20" alt="ru">
                  <span class="ms-1">Русский</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ params: { locale: 'be' }}">
                  <img src="/flags/be.png" width="20" alt="be">
                  <span class="ms-1">Беларуская</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ params: { locale: 'uk' }}">
                  <img src="/flags/uk.png" width="20" alt="uk">
                  <span class="ms-1">Українська</span>
                </RouterLink>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
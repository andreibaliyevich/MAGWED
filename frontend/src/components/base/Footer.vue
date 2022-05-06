<script setup>
import { RouterLink } from 'vue-router'

import { useBaseStore } from '@/stores/base.js'
const baseStore = useBaseStore()
</script>

<script>
export default {
  methods: {
    changeCurrency(event) {
      window.localStorage.setItem('currency', event.target.value)
      this.baseStore.setCurrency(event.target.value)
    },
    changeLocale(event) {
      this.$router.push({ params: { locale: event.target.value } })
    }
  }
}
</script>

<template>
  <footer class="bg-dark text-white">
    <div class="container pt-5">
      <div class="row">
        <div class="col-md-3">
          <a href="/"><img height="160" src="/for-footer.jpg"></a>
        </div>
        <div class="col-md-3 mt-3 mt-md-0">
          <ul class="nav flex-column">
            <li class="nav-item mb-2">
              <RouterLink class="nav-link p-0 text-white" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">Правила</RouterLink>
            </li>
            <li class="nav-item mb-2">
              <RouterLink class="nav-link p-0 text-white" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">Реклама</RouterLink>
            </li>
            <li class="nav-item mb-2">
              <RouterLink class="nav-link p-0 text-white" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">Наши Логотипы</RouterLink>
            </li>
            <li class="nav-item mb-2">
              <RouterLink class="nav-link p-0 text-white" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">Обратная связь</RouterLink>
            </li>
            <li class="nav-item mb-2">
              <RouterLink class="nav-link p-0 text-white" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">Подробнее о MAGWED</RouterLink>
            </li>
          </ul>
        </div>
        <div class="col-md-3">
          <ul class="nav flex-column">
            <li class="nav-item mb-2">
              <RouterLink class="nav-link p-0 text-white" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">Аналитика</RouterLink>
            </li>
            <li class="nav-item mb-2">
              <RouterLink class="nav-link p-0 text-white" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">Карьера в MAGWED</RouterLink>
            </li>
            <li class="nav-item mb-2">
              <RouterLink class="nav-link p-0 text-white" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">Условия использования</RouterLink>
            </li>
            <li class="nav-item mb-2">
              <RouterLink class="nav-link p-0 text-white" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">Политика конфиденциальности</RouterLink>
            </li>
            <li class="nav-item mb-2">
              <RouterLink class="nav-link p-0 text-white" :to="{ name: 'Home', params: { locale: `${ $i18n.locale }` }}">Реклама и продвижение</RouterLink>
            </li>
          </ul>
        </div>
        <div class="col-md-3 mt-3 mt-md-0">
          <ul class="nav flex-column">
            <li class="nav-item mb-2">
              <select class="form-select bg-dark text-white border-secondary" :value="baseStore.currency" @change="changeCurrency">
                <option class="bg-white text-dark" value="USD">$ USD</option>
                <option class="bg-white text-dark" value="EUR">€ EUR</option>
                <option class="bg-white text-dark" value="RUB">₽ RUB</option>
                <option class="bg-white text-dark" value="BYN">Br BYN</option>
                <option class="bg-white text-dark" value="UAH">₴ UAH</option>
              </select>
            </li>
            <li class="nav-item mb-2">
              <select class="form-select bg-dark text-white border-secondary" :value="$i18n.locale" @change="changeLocale">
                <option class="bg-white text-dark" value="en">English</option>
                <option class="bg-white text-dark" value="ru">Русский</option>
                <option class="bg-white text-dark" value="be">Беларуская</option>
                <option class="bg-white text-dark" value="uk">Українська</option>
              </select>
            </li>
          </ul>
        </div>
      </div>
      <hr class="text-white my-4">
      <div class="row flex-md-row-reverse align-items-center pb-4">
        <div class="col-md-6 text-center text-md-end">
          <a class="text-muted link-facebook me-3" href="https://www.facebook.com/" target="_blank">
            <i class="fa-brands fa-facebook-f"></i>
          </a>
          <a class="text-muted link-twitter me-3" href="https://twitter.com/" target="_blank">
            <i class="fa-brands fa-twitter"></i>
          </a>
          <a class="text-muted link-instagram me-3" href="https://www.instagram.com/" target="_blank">
            <i class="fa-brands fa-instagram"></i>
          </a>
          <a class="text-muted link-spotify me-3" href="https://www.spotify.com/" target="_blank">
            <i class="fa-brands fa-spotify"></i>
          </a>
          <a class="text-muted link-youtube me-3" href="https://www.youtube.com/" target="_blank">
            <i class="fa-brands fa-youtube"></i>
          </a>
          <a class="text-muted link-soundcloud me-3" href="https://soundcloud.com/" target="_blank">
            <i class="fa-brands fa-soundcloud"></i>
          </a>
          <a class="text-muted link-pinterest me-3" href="https://www.pinterest.com/" target="_blank">
            <i class="fa-brands fa-pinterest"></i>
          </a>
          <a class="text-muted link-vk me-3" href="https://vk.com/" target="_blank">
            <i class="fa-brands fa-vk"></i>
          </a>
          <a class="text-muted link-linkedin" href="https://www.linkedin.com/" target="_blank">
            <i class="fa-brands fa-linkedin"></i>
          </a>
        </div>
        <div class="col-md-6 text-center text-md-start text-muted mt-3 mt-md-0">Copyright © 2022-{{ new Date().getFullYear() }} MAGWED</div>
      </div>
    </div>
  </footer>
</template>

<style scoped>

</style>

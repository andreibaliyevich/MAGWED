<script setup>
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { LANGUAGES, CURRENCIES } from '@/config.js'
import { useCurrencyStore } from '@/stores/currency.js'

const router = useRouter()
const currencyStore = useCurrencyStore()

const magazineDataLoading = ref(true)
const magazineData = ref({})

const getMagazine = async () => {
  try {
    const response = await axios.get('/main/magazine/')
    magazineData.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    magazineDataLoading.value = false
  }
}

const changeCurrency = (event) => {
  window.localStorage.setItem('currency', event.target.value)
  currencyStore.setCurrency(event.target.value)
}

const changeLocale = (event) => {
  router.push({ params: { locale: event.target.value } })
}

onMounted(() => {
  getMagazine()
})
</script>

<template>
  <footer class="bg-dark text-white">
    <div class="container pt-5">
      <div class="row">
        <div class="col-md-3">
          <LoadingIndicator v-if="magazineDataLoading" />
          <a
            v-else
            :href="magazineData.file"
            :title="magazineData.title"
            target="_blank"
          >
            <img
              height="160"
              :src="magazineData.image"
            >
          </a>
        </div>
        <div class="col-md-3 mt-3 mt-md-0">
          <ul class="nav flex-column">
            <li class="nav-item mb-2">
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.rules') }}
              </router-link>
            </li>
            <li class="nav-item mb-2">
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.advertising') }}
              </router-link>
            </li>
            <li class="nav-item mb-2">
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.our_logos') }}
              </router-link>
            </li>
            <li class="nav-item mb-2">
              <router-link
                :to="{
                  name: 'Feedback',
                  params: { locale: $i18n.locale }
                }"
                class="nav-link p-0 text-white"
              >
                {{ $t('feedback.feedback') }}
              </router-link>
            </li>
            <li class="nav-item mb-2">
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.more_about_magwed') }}
              </router-link>
            </li>
          </ul>
        </div>
        <div class="col-md-3">
          <ul class="nav flex-column">
            <li class="nav-item mb-2">
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.analytics') }}
              </router-link>
            </li>
            <li class="nav-item mb-2">
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.career_at_magwed') }}
              </router-link>
            </li>
            <li class="nav-item mb-2">
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.terms_of_use') }}
              </router-link>
            </li>
            <li class="nav-item mb-2">
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.privacy_policy') }}
              </router-link>
            </li>
            <li class="nav-item mb-2">
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.advertising_and_promotion') }}
              </router-link>
            </li>
          </ul>
        </div>
        <div class="col-md-3 mt-3 mt-md-0">
          <ul class="nav flex-column">
            <li class="nav-item mb-2">
              <select
                :value="currencyStore.currencyValue"
                @change="changeCurrency"
                class="form-select bg-dark text-white border-secondary"
              >
                <option
                  v-for="currency in CURRENCIES"
                  :key="currency.value"
                  :value="currency.value"
                  class="bg-white text-dark"
                >
                  {{ currency.text }} {{ currency.value }}
                </option>
              </select>
            </li>
            <li class="nav-item mb-2">
              <select
                :value="$i18n.locale"
                @change="changeLocale"
                class="form-select bg-dark text-white border-secondary"
              >
                <option
                  v-for="language in LANGUAGES"
                  :key="language.value"
                  :value="language.value"
                  class="bg-white text-dark"
                >
                  {{ language.text }}
                </option>
              </select>
            </li>
          </ul>
        </div>
      </div>
      <hr class="text-white my-4">
      <div class="row flex-md-row-reverse align-items-center pb-4">
        <div class="col-md-6 text-center text-md-end">
          <a
            class="text-secondary link-facebook me-3"
            href="https://www.facebook.com/"
            target="_blank"
          >
            <i class="fa-brands fa-facebook-f"></i>
          </a>
          <a
            class="text-secondary link-twitter me-3"
            href="https://twitter.com/"
            target="_blank"
          >
            <i class="fa-brands fa-twitter"></i>
          </a>
          <a
            class="text-secondary link-instagram me-3"
            href="https://www.instagram.com/"
            target="_blank"
          >
            <i class="fa-brands fa-instagram"></i>
          </a>
          <a
            class="text-secondary link-linkedin me-3"
            href="https://www.linkedin.com/"
            target="_blank"
          >
            <i class="fa-brands fa-linkedin"></i>
          </a>
          <a
            class="text-secondary link-spotify me-3"
            href="https://www.spotify.com/"
            target="_blank"
          >
            <i class="fa-brands fa-spotify"></i>
          </a>
          <a
            class="text-secondary link-youtube me-3"
            href="https://www.youtube.com/"
            target="_blank"
          >
            <i class="fa-brands fa-youtube"></i>
          </a>
          <a
            class="text-secondary link-soundcloud me-3"
            href="https://soundcloud.com/"
            target="_blank"
          >
            <i class="fa-brands fa-soundcloud"></i>
          </a>
          <a
            class="text-secondary link-pinterest me-3"
            href="https://www.pinterest.com/"
            target="_blank"
          >
            <i class="fa-brands fa-pinterest"></i>
          </a>
          <a
            class="text-secondary link-vk"
            href="https://vk.com/"
            target="_blank"
          >
            <i class="fa-brands fa-vk"></i>
          </a>
        </div>
        <div class="col-md-6 text-center text-md-start text-secondary mt-3 mt-md-0">
          Copyright © 2022-{{ new Date().getFullYear() }} MAGWED
        </div>
      </div>
    </div>
  </footer>
</template>

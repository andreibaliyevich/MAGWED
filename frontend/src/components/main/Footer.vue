<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '@/stores/main.js'

const router = useRouter()
const mainStore = useMainStore()

const magazineLoading = ref(true)
const magazineData = ref({})

const getMagazine = async () => {
  try {
    const response = await axios.get('/main/magazine/')
    magazineData.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    magazineLoading.value = false
  }
}

const changeCurrency = (event) => {
  window.localStorage.setItem('currency', event.target.value)
  mainStore.setCurrency(event.target.value)
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
          <LoadingIndicator v-if="magazineLoading" />
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
              <LocaleRouterLink
                routeName="Home"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.rules') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item mb-2">
              <LocaleRouterLink
                routeName="Home"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.advertising') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item mb-2">
              <LocaleRouterLink
                routeName="Home"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.our_logos') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item mb-2">
              <LocaleRouterLink
                routeName="Home"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.feedback') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item mb-2">
              <LocaleRouterLink
                routeName="Home"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.more_about_magwed') }}
              </LocaleRouterLink>
            </li>
          </ul>
        </div>
        <div class="col-md-3">
          <ul class="nav flex-column">
            <li class="nav-item mb-2">
              <LocaleRouterLink
                routeName="Home"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.analytics') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item mb-2">
              <LocaleRouterLink
                routeName="Home"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.career_at_magwed') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item mb-2">
              <LocaleRouterLink
                routeName="Home"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.terms_of_use') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item mb-2">
              <LocaleRouterLink
                routeName="Home"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.privacy_policy') }}
              </LocaleRouterLink>
            </li>
            <li class="nav-item mb-2">
              <LocaleRouterLink
                routeName="Home"
                class="nav-link p-0 text-white"
              >
                {{ $t('footer.advertising_and_promotion') }}
              </LocaleRouterLink>
            </li>
          </ul>
        </div>
        <div class="col-md-3 mt-3 mt-md-0">
          <ul class="nav flex-column">
            <li class="nav-item mb-2">
              <select
                :value="mainStore.currency"
                @change="changeCurrency"
                class="form-select bg-dark text-white border-secondary"
              >
                <option class="bg-white text-dark" value="USD">$ USD</option>
                <option class="bg-white text-dark" value="EUR">€ EUR</option>
                <option class="bg-white text-dark" value="RUB">₽ RUB</option>
                <option class="bg-white text-dark" value="BYN">Br BYN</option>
                <option class="bg-white text-dark" value="UAH">₴ UAH</option>
              </select>
            </li>
            <li class="nav-item mb-2">
              <select
                :value="$i18n.locale"
                @change="changeLocale"
                class="form-select bg-dark text-white border-secondary"
              >
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
          <a
            class="text-muted link-facebook me-3"
            href="https://www.facebook.com/"
            target="_blank"
          >
            <i class="fa-brands fa-facebook-f"></i>
          </a>
          <a
            class="text-muted link-twitter me-3"
            href="https://twitter.com/"
            target="_blank"
          >
            <i class="fa-brands fa-twitter"></i>
          </a>
          <a
            class="text-muted link-instagram me-3"
            href="https://www.instagram.com/"
            target="_blank"
          >
            <i class="fa-brands fa-instagram"></i>
          </a>
          <a
            class="text-muted link-linkedin me-3"
            href="https://www.linkedin.com/"
            target="_blank"
          >
            <i class="fa-brands fa-linkedin"></i>
          </a>
          <a
            class="text-muted link-spotify me-3"
            href="https://www.spotify.com/"
            target="_blank"
          >
            <i class="fa-brands fa-spotify"></i>
          </a>
          <a
            class="text-muted link-youtube me-3"
            href="https://www.youtube.com/"
            target="_blank"
          >
            <i class="fa-brands fa-youtube"></i>
          </a>
          <a
            class="text-muted link-soundcloud me-3"
            href="https://soundcloud.com/"
            target="_blank"
          >
            <i class="fa-brands fa-soundcloud"></i>
          </a>
          <a
            class="text-muted link-pinterest me-3"
            href="https://www.pinterest.com/"
            target="_blank"
          >
            <i class="fa-brands fa-pinterest"></i>
          </a>
          <a
            class="text-muted link-vk"
            href="https://vk.com/"
            target="_blank"
          >
            <i class="fa-brands fa-vk"></i>
          </a>
        </div>
        <div class="col-md-6 text-center text-md-start text-muted mt-3 mt-md-0">
          Copyright © 2022-{{ new Date().getFullYear() }} MAGWED
        </div>
      </div>
    </div>
  </footer>
</template>

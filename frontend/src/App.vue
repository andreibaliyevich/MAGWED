<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { WS_URL } from '@/config.js'
import { useMainStore } from '@/stores/main.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import Header from '@/components/main/Header.vue'
import Navbar from '@/components/main/Navbar.vue'
import Footer from '@/components/main/Footer.vue'

const mainStore = useMainStore()
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const deviceUUID = ref(null)
const connectionSocket = ref(null)

axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response.status === 401) {
      window.localStorage.removeItem('user')
      window.location.reload()
    }
    return Promise.reject(error)
  }
)

deviceUUID.value = window.localStorage.getItem('deviceUUID')
if (!deviceUUID.value) {
  deviceUUID.value = crypto.randomUUID()
  window.localStorage.setItem('deviceUUID', deviceUUID.value)
}

const currency = window.localStorage.getItem('currency')
if (currency) {
  mainStore.setCurrency(currency)
}

const userString = window.localStorage.getItem('user')
if (userString) {
  const userData = JSON.parse(userString)
  axios.defaults.headers.common['Authorization'] = `Token ${userData.token}`
  userStore.setUserData(userData)
}

onMounted(async () => {
  if (userStore.isLoggedIn) {
    try {
      const response = await axios.get('/accounts/auth/wstoken/')
      connectionSocket.value = new WebSocket(
        WS_URL
        + '/ws/connection/'
        + deviceUUID.value
        + '/?'
        + response.data.wstoken
      )
      connectionSocket.value.onmessage = (event) => {
        connectionBusStore.setUserStatus(JSON.parse(event.data))
      }
    } catch (error) {
      console.error(error)
    }
  } else {
    connectionSocket.value = new WebSocket(
      WS_URL
      + '/ws/connection/'
      + deviceUUID.value
      + '/'
    )
    connectionSocket.value.onmessage = (event) => {
      connectionBusStore.setUserStatus(JSON.parse(event.data))
    }
  }
})
</script>

<template>
  <Header />
  <Navbar />
  <main>
    <RouterView />
  </main>
  <Footer />
</template>

<style>
@import '@/assets/base.css';
</style>

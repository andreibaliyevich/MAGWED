<script setup>
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid'
import { RouterLink, RouterView } from 'vue-router'

import Header from '@/components/base/Header.vue'
import NavBar from '@/components/base/NavBar.vue'
import Footer from '@/components/base/Footer.vue'

import { useBaseStore } from '@/stores/base.js'
import { useUserStore } from '@/stores/user.js'
const baseStore = useBaseStore()
const userStore = useUserStore()
</script>

<script>
export default {
  created() {
    axios.defaults.baseURL = this.baseStore.apiURL
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

    const deviceId = window.localStorage.getItem('deviceId')
    if (deviceId) {
      this.baseStore.setDeviceId(deviceId)
    } else {
      const deviceUuid = uuidv4()
      window.localStorage.setItem('deviceId', deviceUuid)
      this.baseStore.setDeviceId(deviceUuid)
    }

    const currencyString = window.localStorage.getItem('currency')
    if (currencyString) {
      this.baseStore.setCurrency(currencyString)
    }

    const userString = window.localStorage.getItem('user')
    if (userString) {
      const userData = JSON.parse(userString)
      axios.defaults.headers.common['Authorization'] = `Token ${ userData.token }`
      this.userStore.setUserData(userData)
    }
  },
  mounted() {
    if (this.userStore.isLoggedIn) {
      axios.get('/' + this.$i18n.locale + '/accounts/auth/wstoken/')
      .then((response) => {
        this.connectionSocket = new WebSocket(
          this.baseStore.wsURL
          + '/ws/connection/' + this.baseStore.deviceId
          + '/?' + response.data.wstoken
        )
        this.connectionSocket.onmessage = (event) => {
          this.socketOnMessage(event)
        }
      })
    } else {
      this.connectionSocket = new WebSocket(
        this.baseStore.wsURL
        + '/ws/connection/' + this.baseStore.deviceId + '/'
      )
      this.connectionSocket.onmessage = (event) => {
        this.socketOnMessage(event)
      }
    }
  },
  methods: {
    socketOnMessage(event) {
      console.log(`[message] Данные получены с сервера: ${event.data}`)
    }
  }
}
</script>

<template>
  <Header />
  <NavBar />
  <main>
    <RouterView />
  </main>
  <Footer />
</template>

<style>
@import '@/assets/base.css';
</style>

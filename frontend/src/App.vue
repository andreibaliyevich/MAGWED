<script setup>
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid'
import { RouterView } from 'vue-router'

import { WS_URL } from '@/config.js'

import Header from '@/components/main/Header.vue'
import NavBar from '@/components/main/NavBar.vue'
import Footer from '@/components/main/Footer.vue'

import { useMainStore } from '@/stores/main.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
const mainStore = useMainStore()
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()
</script>

<script>
export default {
  data() {
    return {
      deviceId: null,
      connectionSocket: null
    }
  },
  created() {
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

    this.deviceId = window.localStorage.getItem('deviceId')
    if (!this.deviceId) {
      this.deviceId = uuidv4()
      window.localStorage.setItem('deviceId', this.deviceId)
    }

    const currency = window.localStorage.getItem('currency')
    if (currency) {
      this.mainStore.setCurrency(currency)
    }

    const userString = window.localStorage.getItem('user')
    if (userString) {
      const userData = JSON.parse(userString)
      axios.defaults.headers.common['Authorization'] = `Token ${userData.token}`
      this.userStore.setUserData(userData)
    }
  },
  mounted() {
    if (this.userStore.isLoggedIn) {
      axios.get('/accounts/auth/wstoken/')
      .then((response) => {
        this.connectionSocket = new WebSocket(
          WS_URL
          + '/ws/connection/'
          + this.deviceId
          + '/?'
          + response.data.wstoken
        )
        this.connectionSocket.onmessage = (event) => {
          this.connectionBusStore.setUserStatus(JSON.parse(event.data))
        }
      })
    } else {
      this.connectionSocket = new WebSocket(
        WS_URL
        + '/ws/connection/'
        + this.deviceId
        + '/'
      )
      this.connectionSocket.onmessage = (event) => {
        this.connectionBusStore.setUserStatus(JSON.parse(event.data))
      }
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

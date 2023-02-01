<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { WS_URL } from '@/config.js'
import NavbarNotice from './NavbarNotice.vue'

const notificationsLoading = ref(true)
const notifications = ref([])
const notificationsSocket = ref(null)
const notificationsSocketConnect = ref(null)
const countNotViewed = ref(0)
const nextURL = ref(null)

const scrollArea = ref(null)

const getNotifications = async () => {
  try {
    const response = await axios.get('/notifications/')
    notifications.value = response.data.results
    notifications.value.forEach(element => {
      if (!element.viewed) {
        countNotViewed.value += 1
      }
    })
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    notificationsLoading.value = false
  }
}

const getMoreNotifications = async () => {
  notificationsLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    notifications.value = [...notifications.value, ...response.data.results]
    response.data.results.forEach(element => {
      if (!element.viewed) {
        countNotViewed.value += 1
      }
    })
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    notificationsLoading.value = false
  }
}

const connectSocket = async () => {
  try {
    const response = await axios.get('/accounts/auth/wstoken/')
    notificationsSocket.value = new WebSocket(
      WS_URL
      + '/ws/notifications/?'
      + response.data.wstoken
    )
    notificationsSocket.value.onopen = (event) => {
      notificationsSocketConnect.value = true
    }
    notificationsSocket.value.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.action == 'created') {
        notifications.value.unshift(data.notice)
      } else if (data.action == 'updated') {
        const foundIndex = notifications.value.findIndex((element) => {
          return element.id == data.notice.id
        })
        notifications.value[foundIndex] = data.notice
      } else if (data.action == 'viewed') {
        const foundIndex = notifications.value.findIndex((element) => {
          return element.id == data.notice_id
        })
        notifications.value[foundIndex].viewed = data.notice_viewed
        countNotViewed.value -= 1
      }
    }
    notificationsSocket.value.onclose = (event) => {
      notificationsSocket.value = null
      notificationsSocketConnect.value = false
    }
    notificationsSocket.value.onerror = (error) => {
      notificationsSocket.value = null
      notificationsSocketConnect.value = false
    }
  } catch (error) {
    console.error(error)
  } finally {
    notificationsLoading.value = false
  }
}

const setNoticeViewed = (notice_id) => {
  notificationsSocket.value.send(JSON.stringify({
    'notice_id': notice_id
  }))
}

const vIntersectionNotifications = {
  mounted(el) {
    const options = {
      root: scrollArea.value,
      rootMargin: '0px',
      threshold: 1.0
    }
    const callback = (entries, observer) => {
      if (entries[0].isIntersecting) {
        getMoreNotifications()
      }
    }
    const observer = new IntersectionObserver(callback, options)
    observer.observe(el)
  }
}
const vIntersectionNotice = {
  mounted(el, binding) {
    const options = {
      root: scrollArea.value,
      rootMargin: '0px',
      threshold: 1.0
    }
    const callback = (entries, observer) => {
      if (entries[0].isIntersecting) {
        setNoticeViewed(binding.value)
      }
    }
    const observer = new IntersectionObserver(callback, options)
    observer.observe(el)
  }
}

onMounted(() => {
  getNotifications()
  connectSocket()
})
</script>

<template>
  <div class="dropdown-notifications">
    <div class="dropdown">
      <a
        ref="dropdownNotifications"
        id="dropdownNotifications"
        href="#"
        class="link-secondary position-relative"
        data-bs-toggle="dropdown"
        data-bs-auto-close="outside"
        aria-expanded="false"
      >
        <i class="fa-solid fa-bell fa-lg"></i>
        <span
          v-if="countNotViewed > 0"
          class="position-absolute top-0 start-100 translate-middle p-1 rounded-circle bg-danger"
        >
          <span class="visually-hidden">New notifications</span>
        </span>
      </a>
      <ul
        ref="scrollArea"
        class="dropdown-menu dropdown-menu-end shadow overflow-auto"
        aria-labelledby="dropdownNotifications"
      >
        <li v-if="notifications.length > 0">
          <ul class="list-group list-group-flush">
            <li
              v-for="notice in notifications"
              :key="notice.id"
              class="list-group-item list-group-item-action"
            >
              <NavbarNotice
                v-if="notice.viewed || !notificationsSocketConnect"
                :notice="notice"
                @clickLink="$refs.dropdownNotifications.click()"
              />
              <NavbarNotice
                v-else
                :notice="notice"
                @clickLink="$refs.dropdownNotifications.click()"
                v-intersection-notice="notice.id"
              />
            </li>
          </ul>
        </li>
        <li v-else>
          <div class="lead d-flex justify-content-center py-3">
            {{ $t('notifications.no_notifications') }}
          </div>
        </li>
        <li v-if="nextURL" v-intersection-notifications></li>
        <li v-if="notificationsLoading">
          <LoadingIndicator />
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
* {
  scrollbar-color: #c0c0c0;
  scrollbar-width: thin;
}
::-webkit-scrollbar {
  width: 0.3em;
  height: 0.3em;
  background-color: #f5f5f5;
}
::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 3em;
}
::-webkit-scrollbar-thumb:hover {
  background-color: #808080;
}

.dropdown-menu.overflow-auto {
  width: 330px;
  max-height: 530px;
}
</style>

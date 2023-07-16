<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { WS_URL } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import NavbarNotice from './NavbarNotice.vue'

const userStore = useUserStore()

const notificationListLoading = ref(true)
const notificationList = ref([])
const nextURL = ref(null)
const countNotViewed = ref(0)

const notificationsSocket = ref(null)
const notificationsSocketConnect = ref(null)

const notificationListDropdown = ref(null)

const getNotificationList = async () => {
  try {
    const response = await axios.get('/notifications/')
    notificationList.value = response.data.results
    notificationList.value.forEach(element => {
      if (!element.viewed) {
        countNotViewed.value += 1
      }
    })
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    notificationListLoading.value = false
  }
}

const getMoreNotificationList = async () => {
  notificationListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    notificationList.value = [...notificationList.value, ...response.data.results]
    response.data.results.forEach(element => {
      if (!element.viewed) {
        countNotViewed.value += 1
      }
    })
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    notificationListLoading.value = false
  }
}

const connectSocket = async () => {
  notificationsSocket.value = new WebSocket(
    WS_URL
    + '/ws/notifications/?'
    + userStore.token
  )
  notificationsSocket.value.onopen = (event) => {
    notificationsSocketConnect.value = true
  }
  notificationsSocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.action == 'created') {
      notificationList.value.unshift(data.notice)
    } else if (data.action == 'updated') {
      const foundIndex = notificationList.value.findIndex((element) => {
        return element.uuid == data.notice.uuid
      })
      if (foundIndex != -1) {
        notificationList.value[foundIndex] = data.notice
      }
    } else if (data.action == 'viewed') {
      const foundIndex = notificationList.value.findIndex((element) => {
        return element.uuid == data.notice_uuid
      })
      if (foundIndex != -1) {
        notificationList.value[foundIndex].viewed = data.notice_viewed
        countNotViewed.value -= 1
      }
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
}

const setNoticeViewed = (notice_uuid) => {
  notificationsSocket.value.send(JSON.stringify({
    'notice_uuid': notice_uuid
  }))
}

const vIntersectionNotifications = {
  mounted(el) {
    const options = {
      root: notificationListDropdown.value,
      rootMargin: '0px',
      threshold: 1.0
    }
    const callback = (entries, observer) => {
      if (entries[0].isIntersecting) {
        getMoreNotificationList()
      }
    }
    const observer = new IntersectionObserver(callback, options)
    observer.observe(el)
  }
}
const vIntersectionNotice = {
  mounted(el, binding) {
    const options = {
      root: notificationListDropdown.value,
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
  getNotificationList()
  connectSocket()
})
</script>

<template>
  <div class="dropdown-notifications">
    <div class="dropdown">
      <a
        ref="dropdownNotifications"
        id="dropdown-notifications"
        href="#"
        class="text-decoration-none link-secondary"
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
        ref="notificationListDropdown"
        class="dropdown-menu dropdown-menu-end border border-light shadow"
        aria-labelledby="notification-list-dropdown"
      >
        <li class="overflow-auto">
          <ul
            v-if="notificationList.length > 0"
            class="list-group list-group-flush"
          >
            <li
              v-for="notice in notificationList"
              :key="notice.uuid"
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
                v-intersection-notice="notice.uuid"
              />
            </li>
          </ul>
          <div
            v-else-if="!notificationListLoading"
            class="lead d-flex justify-content-center py-3"
          >
            {{ $t('notifications.no_notifications') }}
          </div>
          <div v-if="nextURL" v-intersection-notifications></div>
          <LoadingIndicator v-if="!notificationListLoading" />
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.dropdown-menu.dropdown-menu-end {
  width: 330px;
}

li.overflow-auto {
  max-height: 550px;
}
li.overflow-auto::-webkit-scrollbar {
  width: 0.2em;
}
li.overflow-auto::-webkit-scrollbar-track {
  background-color: #f5f5f5;
}
li.overflow-auto::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 1em;
}
li.overflow-auto::-webkit-scrollbar-thumb:hover {
  background-color: #e72a26;
}
</style>
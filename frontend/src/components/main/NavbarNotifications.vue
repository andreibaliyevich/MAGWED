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
const notViewedCount = ref(0)

const notificationSocket = ref(null)
const notificationSocketConnect = ref(null)

const notificationListArea = ref(null)

const getNotificationList = async () => {
  try {
    const response = await axios.get('/notifications/')
    notificationList.value = response.data.results
    notificationList.value.forEach(element => {
      if (!element.viewed) {
        notViewedCount.value += 1
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
        notViewedCount.value += 1
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
  notificationSocket.value = new WebSocket(
    WS_URL
    + '/ws/notifications/?'
    + userStore.token
  )
  notificationSocket.value.onopen = (event) => {
    notificationSocketConnect.value = true
  }
  notificationSocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.action == 'created') {
      notificationList.value.unshift(data.data)
      notViewedCount.value += 1
    } else if (data.action == 'updated') {
      const foundIndex = notificationList.value.findIndex((element) => {
        return element.uuid == data.data.uuid
      })
      if (foundIndex != -1) {
        notificationList.value[foundIndex].content_object = data.data.content_object
      }
    } else if (data.action == 'deleted') {
      const foundIndex = notificationList.value.findIndex((element) => {
        return element.uuid == data.data
      })
      if (foundIndex != -1) {
        if (!notificationList.value[foundIndex].viewed) {
          notViewedCount.value -= 1
        }
        notificationList.value = notificationList.value.filter((element) => {
          return element.uuid !== data.data
        })
      }
    } else if (data.action == 'viewed') {
      const foundIndex = notificationList.value.findIndex((element) => {
        return element.uuid == data.data.uuid
      })
      if (foundIndex != -1) {
        notificationList.value[foundIndex].viewed = data.data.viewed
        notViewedCount.value -= 1
      }
    }
  }
  notificationSocket.value.onclose = (event) => {
    notificationSocket.value = null
    notificationSocketConnect.value = false
  }
  notificationSocket.value.onerror = (error) => {
    notificationSocket.value = null
    notificationSocketConnect.value = false
  }
}

const setNoticeViewed = (notice_uuid) => {
  notificationSocket.value.send(JSON.stringify({
    'notice_uuid': notice_uuid
  }))
}

onMounted(() => {
  getNotificationList()
  connectSocket()
})
</script>

<template>
  <div class="notifications_dropdown">
    <div class="dropdown">
      <button
        ref="notificationsDropdown"
        id="notifications_dropdown"
        type="button"
        class="btn btn-link link-secondary p-0"
        data-bs-toggle="dropdown"
        data-bs-auto-close="true"
        aria-expanded="false"
      >
        <i class="fa-solid fa-bell fa-lg"></i>
        <span
          v-if="notViewedCount > 0"
          class="position-absolute top-0 start-100 translate-middle p-1 rounded-circle bg-danger"
        >
          <span class="visually-hidden">New notifications</span>
        </span>
      </button>
      <div
        class="dropdown-menu dropdown-menu-end border border-light shadow"
        aria-labelledby="notification-list-dropdown"
      >
        <div
          ref="notificationListArea"
          class="overflow-y-auto"
        >
          <ul
            v-if="notificationList.length > 0"
            class="list-group list-group-flush"
          >
            <li
              v-for="notice in notificationList"
              :key="notice.uuid"
              :class="[
                'list-group-item list-group-item-action',
                { 'bg-light': !notice.viewed }
              ]"
            >
              <NavbarNotice
                v-if="notice.viewed || !notificationSocketConnect"
                :notice="notice"
              />
              <NavbarNotice
                v-else
                :notice="notice"
                v-intersection="{
                  'scrollArea': null,
                  'callbackFunction': setNoticeViewed,
                  'functionArguments': [notice.uuid]
                }"
              />
            </li>
          </ul>
          <div
            v-else-if="!notificationListLoading"
            class="lead d-flex justify-content-center py-3"
          >
            {{ $t('notifications.no_notifications') }}
          </div>
          <div
            v-if="nextURL"
            style="min-height: 1px; margin-bottom: 1px;"
            v-intersection="{
              'scrollArea': notificationListArea,
              'callbackFunction': getMoreNotificationList,
              'functionArguments': []
            }"
          ></div>
          <LoadingIndicator v-if="notificationListLoading" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dropdown-menu.dropdown-menu-end {
  width: 330px;
}

div.overflow-y-auto {
  max-height: 550px;
}
div.overflow-y-auto::-webkit-scrollbar {
  width: 0.2em;
}
div.overflow-y-auto::-webkit-scrollbar-track {
  background-color: #f5f5f5;
}
div.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 1em;
}
div.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background-color: #e72a26;
}
</style>
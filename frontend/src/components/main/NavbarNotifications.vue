<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { WS_URL, reasonOfNotification } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const { getLocaleDateTimeString } = useLocaleDateTime()

const notificationsLoading = ref(true)
const notifications = ref([])
const notificationsSocket = ref(null)
const countNotViewed = ref(0)

const getNotifications = async () => {
  try {
    const response = await axios.get('/notifications/')
    notifications.value = response.data.results
    notifications.value.forEach(element => {
      if (!element.viewed) {
        countNotViewed.value += 1
      }
    })
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
    notificationsSocket.value.onmessage = (event) => {
      const data = JSON.parse(event.data)
    }
    notificationsSocket.value.onerror = (event) => {
      notificationsSocket.value = null
      conversation.value = {}
      notifications.value = []
    }
  } catch (error) {
    console.error(error)
  } finally {
    notificationsLoading.value = false
  }
}

const noticeViewed = (notice_id) => {
  notificationsSocket.value.send(JSON.stringify({
    'notice_id': notice_id
  }))
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
        class="dropdown-menu dropdown-menu-end shadow overflow-auto"
        aria-labelledby="dropdownNotifications"
      >
        <li v-if="notifications.length > 0">
          <ul class="list-group list-group-flush">
            <li
              v-for="notice in notifications"
              class="list-group-item list-group-item-action"
            >
              <div class="d-flex gap-3">

                <a
                  v-if="notice.initiator.profile_url"
                  :href="`#${notice.initiator.profile_url}`"
                >
                  <UserAvatar
                    :src="notice.initiator.avatar"
                    :width="36"
                    :height="36"
                  />
                </a>
                <UserAvatar
                  v-else
                  :src="notice.initiator.avatar"
                  :width="36"
                  :height="36"
                />

                <div
                  v-if="notice.reason == reasonOfNotification.FOLLOW"
                  class="d-flex align-content-between flex-wrap h-100"
                >
                  <p class="text-dark mb-0">
                    {{ $t('notifications.follow', { user_name: notice.initiator.name }) }}
                  </p>
                  <small class="text-muted">
                    {{ getLocaleDateTimeString(notice.created_at) }}
                  </small>
                </div>
                <a
                  v-else-if="notice.reason == reasonOfNotification.ARTICLE"
                  :href="`#${notice.content_object.slug}`"
                  class="d-flex justify-content-between align-items-center text-decoration-none w-100"
                >
                  <div class="d-flex align-content-between flex-wrap h-100">
                    <p class="text-dark mb-0">
                      {{ $t('notifications.article', { user_name: notice.initiator.name, article_title: notice.content_object.translated_title }) }}
                    </p>
                    <small class="text-muted">
                      {{ getLocaleDateTimeString(notice.created_at) }}
                    </small>
                  </div>
                  <img :src="notice.content_object.thumbnail" width="64" height="64">
                </a>
                <a
                  v-else-if="notice.reason == reasonOfNotification.ALBUM"
                  :href="`#${notice.content_object.id}`"
                  class="d-flex justify-content-between align-items-center text-decoration-none w-100"
                >
                  <div class="d-flex align-content-between flex-wrap h-100">
                    <p class="text-dark mb-0">
                      {{ $t('notifications.album', { user_name: notice.initiator.name, album_title: notice.content_object.title }) }}
                    </p>
                    <small class="text-muted">
                      {{ getLocaleDateTimeString(notice.created_at) }}
                    </small>
                  </div>
                  <img :src="notice.content_object.thumbnail" width="64" height="64">
                </a>
                <a
                  v-else-if="notice.reason == reasonOfNotification.PHOTO"
                  :href="`#${notice.content_object.id}`"
                  class="d-flex justify-content-between align-items-center text-decoration-none w-100"
                >
                  <div class="d-flex align-content-between flex-wrap h-100">
                    <p class="text-dark mb-0">
                      {{ $t('notifications.photo', { user_name: notice.initiator.name }) }}
                    </p>
                    <small class="text-muted">
                      {{ getLocaleDateTimeString(notice.created_at) }}
                    </small>
                  </div>
                  <img :src="notice.content_object.thumbnail" width="64" height="64">
                </a>
                <a
                  v-else-if="notice.reason == reasonOfNotification.LIKE_ALBUM"
                  :href="`#${notice.content_object.id}`"
                  class="d-flex justify-content-between align-items-center text-decoration-none w-100"
                >
                  <div class="d-flex align-content-between flex-wrap h-100">
                    <p class="text-dark mb-0">
                      {{ $t('notifications.like_album', { user_name: notice.initiator.name, album_title: notice.content_object.title }) }}
                    </p>
                    <small class="text-muted">
                      {{ getLocaleDateTimeString(notice.created_at) }}
                    </small>
                  </div>
                  <img :src="notice.content_object.thumbnail" width="64" height="64">
                </a>
                <a
                  v-else-if="notice.reason == reasonOfNotification.LIKE_PHOTO"
                  :href="`#${notice.content_object.id}`"
                  class="d-flex justify-content-between align-items-center text-decoration-none w-100"
                >
                  <div class="d-flex align-content-between flex-wrap h-100">
                    <p class="text-dark mb-0">
                      {{ $t('notifications.like_photo', { user_name: notice.initiator.name }) }}
                    </p>
                    <small class="text-muted">
                      {{ getLocaleDateTimeString(notice.created_at) }}
                    </small>
                  </div>
                  <img :src="notice.content_object.thumbnail" width="64" height="64">
                </a>
                <a
                  v-else-if="notice.reason == reasonOfNotification.COMMENT_ARTICLE"
                  :href="`#${notice.content_object.slug}`"
                  class="d-flex justify-content-between align-items-center text-decoration-none w-100"
                >
                  <div class="d-flex align-content-between flex-wrap h-100">
                    <p class="text-dark mb-0">
                      {{ $t('notifications.comment_article', { user_name: notice.initiator.name, article_title: notice.content_object.translated_title }) }}
                    </p>
                    <small class="text-muted">
                      {{ getLocaleDateTimeString(notice.created_at) }}
                    </small>
                  </div>
                  <img :src="notice.content_object.thumbnail" width="64" height="64">
                </a>
                <a
                  v-else-if="notice.reason == reasonOfNotification.COMMENT_ALBUM"
                  :href="`#${notice.content_object.id}`"
                  class="d-flex justify-content-between align-items-center text-decoration-none w-100"
                >
                  <div class="d-flex align-content-between flex-wrap h-100">
                    <p class="text-dark mb-0">
                      {{ $t('notifications.comment_album', { user_name: notice.initiator.name, album_title: notice.content_object.title }) }}
                    </p>
                    <small class="text-muted">
                      {{ getLocaleDateTimeString(notice.created_at) }}
                    </small>
                  </div>
                  <img :src="notice.content_object.thumbnail" width="64" height="64">
                </a>
                <a
                  v-else-if="notice.reason == reasonOfNotification.COMMENT_PHOTO"
                  :href="`#${notice.content_object.id}`"
                  class="d-flex justify-content-between align-items-center text-decoration-none w-100"
                >
                  <div class="d-flex align-content-between flex-wrap h-100">
                    <p class="text-dark mb-0">
                      {{ $t('notifications.comment_photo', { user_name: notice.initiator.name }) }}
                    </p>
                    <small class="text-muted">
                      {{ getLocaleDateTimeString(notice.created_at) }}
                    </small>
                  </div>
                  <img :src="notice.content_object.thumbnail" width="64" height="64">
                </a>
                <a
                  v-else-if="notice.reason == reasonOfNotification.COMMENT"
                  :href="`#${notice.content_object.id}`"
                  class="d-flex justify-content-between align-items-center text-decoration-none w-100"
                >
                  <div class="d-flex align-content-between flex-wrap h-100">
                    <p class="text-dark mb-0">
                      {{ $t('notifications.comment', { user_name: notice.initiator.name }) }}
                    </p>
                    <small class="text-muted">
                      {{ getLocaleDateTimeString(notice.created_at) }}
                    </small>
                  </div>
                  <img :src="notice.content_object.thumbnail" width="64" height="64">
                </a>
                <div
                  v-else-if="notice.reason == reasonOfNotification.REVIEW"
                  class="d-flex align-content-between flex-wrap h-100"
                >
                  <p class="text-dark mb-0">
                    {{ $t('notifications.review', { user_name: notice.initiator.name }) }}
                  </p>
                  <small class="text-muted">
                    {{ getLocaleDateTimeString(notice.created_at) }}
                  </small>
                </div>

              </div>
            </li>
          </ul>
        </li>
        <li v-else>
          <div class="lead d-flex justify-content-center py-3">
            No notifications!
          </div>
        </li>
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

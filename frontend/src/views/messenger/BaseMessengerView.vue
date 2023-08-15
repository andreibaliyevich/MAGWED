<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { chatType, messageType } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import GroupAvatar from '@/components/messenger/GroupAvatar.vue'

const connectionBusStore = useConnectionBusStore()

const chatListLoading = ref(true)
const chatList = ref([])

const { getLocaleDateTimeString } = useLocaleDateTime()

const getChatList = async () => {
  try {
    const response = await axios.get('/messenger/chats/')
    chatList.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    chatListLoading.value = false
  }
}

const updateUserStatus = (mutation, state) => {
  chatList.value.forEach((element) => {
    if (
      element.chat_type == chatType.DIALOG &&
      element.details.uuid == state.user_uuid
    ) {
      element.details.online = state.online
    }
  })
}

onMounted(() => {
  getChatList()
  connectionBusStore.$subscribe(updateUserStatus)
})
</script>

<template>
  <div class="base-messenger-view">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 py-4">
          <button
            type="button"
            class="btn btn-light border w-100 d-lg-none"
            data-bs-toggle="offcanvas"
            data-bs-target="#chat-list"
            aria-controls="chat-list"
          >
            <i class="fa-regular fa-comments"></i>
            {{ $t('messenger.chat_list') }}
          </button>
          <div
            id="chat-list"
            tabindex="-1"
            class="offcanvas-lg offcanvas-start"
            aria-labelledby="chat-list-label"
          >
            <div class="offcanvas-header">
              <h5
                id="chat-list-label"
                class="offcanvas-title"
              >
                {{ $t('messenger.chats') }}
              </h5>
              <button
                ref="chatListClose"
                type="button"
                class="btn-close"
                data-bs-dismiss="offcanvas"
                data-bs-target="#chat-list"
                aria-label="Close"
              ></button>
            </div>
            <div class="offcanvas-body overflow-auto d-lg-block">
              <div class="d-none d-lg-block text-uppercase fw-bolder text-secondary mb-3">
                {{ $t('messenger.chats') }}
              </div>

              <LoadingIndicator v-if="chatListLoading" />
              <ul
                v-else-if="chatList.length > 0"
                class="nav nav-pills flex-column px-1"
              >
                <li
                  v-for="chat in chatList"
                  :class="[
                    'nav-item',
                    this.$route.params.uuid == chat.uuid ? 'active' : null
                  ]"
                >
                  <LocaleRouterLink
                    routeName="Chat"
                    :routeParams="{ uuid: chat.uuid }"
                    @click="$refs.chatListClose.click()"
                    :class="[
                      'nav-link',
                      this.$route.params.uuid == chat.uuid ? 'active' : 'text-dark'
                    ]"
                  >
                    <div class="d-flex gap-3">
                      <UserAvatarExtended
                        v-if="chat.chat_type == chatType.DIALOG"
                        :src="chat.details.avatar"
                        :width="48"
                        :height="48"
                        :online="chat.details.online"
                      />
                      <GroupAvatar
                        v-else-if="chat.chat_type == chatType.GROUP"
                        :src="chat.details.image"
                        :width="48"
                        :height="48"
                      />
                      <img
                        v-else
                        src="/chat.jpg"
                        class="rounded-circle"
                        width="48"
                        height="48"
                      >
                      <div class="flex-grow-1 ms-1">
                        <div class="d-flex justify-content-between">
                          <div
                            v-if="chat.chat_type == chatType.GROUP"
                            class="d-flex align-items-center"
                          >
                            <i class="fa-solid fa-user-group"></i>
                            &nbsp;
                            <strong class="mb-0">{{ chat.details.name }}</strong>
                          </div>
                          <strong
                            v-else
                            class="mb-0"
                          >
                            {{ chat.details.name }}
                          </strong>
                          <small v-if="chat.last_message.created_at">
                            {{ getLocaleDateTimeString(chat.last_message.created_at) }}
                          </small>
                        </div>
                        <p
                          v-if="chat.last_message.msg_type == messageType.TEXT"
                          class="mb-0 opacity-75"
                        >
                          {{ chat.last_message.content }}
                        </p>
                        <p
                          v-else-if="chat.last_message.msg_type == messageType.IMAGES"
                          class="mb-0 opacity-75"
                        >
                          {{ chat.last_message.content }} Images
                        </p>
                        <p
                          v-else-if="chat.last_message.msg_type == messageType.FILES"
                          class="mb-0 opacity-75"
                        >
                          {{ chat.last_message.content }} Files
                        </p>
                      </div>
                    </div>
                  </LocaleRouterLink>
                </li>
              </ul>
              <div
                v-else
                class="lead d-flex justify-content-center py-3"
              >
                {{ $t('messenger.no_chats') }}
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-8 p-lg-3">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.offcanvas-body.overflow-auto::-webkit-scrollbar {
  width: 0.3em;
}
.offcanvas-body.overflow-auto::-webkit-scrollbar-track {
  background-color: #f5f5f5;
}
.offcanvas-body.overflow-auto::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 1em;
}
.offcanvas-body.overflow-auto::-webkit-scrollbar-thumb:hover {
  background-color: #e72a26;
}

strong,
small,
.mb-0.opacity-75 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media(min-width: 992px) {
  .offcanvas-body.overflow-auto {
    min-height: 75vh;
  }
  .col-lg-4.py-4 {
    border-right: 1px solid #dee2e6;
  }
}
</style>

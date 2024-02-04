<script setup>
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { WS_URL, chatType, messageType } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import GroupAvatar from '@/components/messenger/GroupAvatar.vue'

const route = useRoute()
const router = useRouter()
const { locale } = useI18n({ useScope: 'global' })
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const chatListLoading = ref(true)
const chatList = ref([])
const nextURL = ref(null)

const chatListSocket = ref(null)

const relatedUserListLoading = ref(false)
const relatedUserList = ref([])
const relatedUserListNextURL = ref(null)

const chatCreating = ref(false)
const selectedChatType = ref(chatType.DIALOG)
const selectedMembers = ref([])
const groupChatName = ref('')
const groupChatImage = ref(null)

const { getLocaleDateTimeString } = useLocaleDateTime()

const errors = ref(null)

const chatListArea = ref(null)
const createChatModal = ref(null)
const createChatModalBootstrap = ref(null)
const relatedUserArea = ref(null)

const sortedChatList = computed(() => {
  return [...chatList.value].sort((chat1, chat2) => {
    return new Date(
      chat2.last_message?.created_at ? chat2.last_message.created_at : Date()
    ) - new Date(
      chat1.last_message?.created_at ? chat1.last_message.created_at : Date()
    )
  })
})

const chatIndex = computed(() => {
  return chatList.value.findIndex((element) => {
    return element.uuid === route.params.uuid
  })
})

const chatCreationDisabled = computed(() => {
  if (
    selectedChatType.value === chatType.DIALOG &&
    selectedMembers.value.length > 0
  ) {
    return false
  }
  if (
    selectedChatType.value === chatType.GROUP &&
    selectedMembers.value.length > 0 &&
    groupChatName.value
  ) {
    return false
  }
  return true
})

const openChatListSocket = async () => {
  chatListSocket.value = new WebSocket(
    WS_URL
      + '/ws/chat-list/?'
      + userStore.token
  )
  chatListSocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.action === 'create_chat') {
      chatList.value.push(data.data)
    } else if (data.action === 'destroy_chat') {
      chatList.value = chatList.value.filter((element) => {
        return element.uuid !== data.data
      })
      if (data.data === route.params.uuid) {
        router.push({
          name: 'Messenger',
          params: { locale: locale.value }
        })
      }
    } else if (data.action === 'new_msg') {
      const foundIndex = chatList.value.findIndex((element) => {
        return element.uuid === data.data.chat_uuid
      })
      chatList.value[foundIndex].last_message = data.data.msg
      if (data.data.author_uuid !== userStore.uuid) {
        chatList.value[foundIndex].unviewed_msg_count += 1
      }
    }
  }
  chatListSocket.value.onclose = (event) => {
    chatListSocket.value = null
  }
  chatListSocket.value.onerror = (error) => {
    chatListSocket.value = null
  }
}

const closeChatListSocket = () => {
  if (chatListSocket.value) {
    chatListSocket.value.close()
  }
}

const getChatList = async () => {
  try {
    const response = await axios.get('/messenger/chat/list/')
    chatList.value = response.data.results
    nextURL.value = response.data.next
    openChatListSocket()
  } catch (error) {
    console.error(error)
  } finally {
    chatListLoading.value = false
  }
}

const getMoreChatList = async () => {
  chatListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    chatList.value = [...chatList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    chatListLoading.value = false
  }
}

const getRelatedUserList = async () => {
  relatedUserListLoading.value = true
  try {
    const response = await axios.get('/social/follow/related-users/')
    relatedUserList.value = response.data.results
    relatedUserListNextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    relatedUserListLoading.value = false
  }
}

const getMoreRelatedUserList = async () => {
  relatedUserListLoading.value = true
  try {
    const response = await axios.get(relatedUserListNextURL.value)
    relatedUserList.value = [...relatedUserList.value, ...response.data.results]
    relatedUserListNextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    relatedUserListLoading.value = false
  }
}

const createChat = async () => {
  chatCreating.value = true

  let formData = new FormData()
  formData.append('chat_type', selectedChatType.value)

  if (selectedChatType.value === chatType.DIALOG) {
    formData.append('members', selectedMembers.value[0])
  } else if (selectedChatType.value === chatType.GROUP) {
    selectedMembers.value.forEach((element) => {
      formData.append('members', element)
    })
    formData.append('name', groupChatName.value)
    if (groupChatImage.value) {
      formData.append('image', groupChatImage.value)
    }
  }

  try {
    const response = await axios.post('/messenger/chat/create/', formData)
    if (response.status === 201) {
      createChatModalBootstrap.value.hide()
    }
  } catch (error) {
    if (error.response.data.uuid) {
      router.push({
        name: 'Chat',
        params: {
          locale: locale.value,
          uuid: error.response.data.uuid
        }
      })
      createChatModalBootstrap.value.hide()
    } else {
      errors.value = error.response.data
    }
  } finally {
    chatCreating.value = false
  }
}

const changeSelectedMembers = (user_uuid) => {
  if (selectedChatType.value === chatType.DIALOG) {
    selectedMembers.value = [user_uuid]
  } else if (selectedChatType.value === chatType.GROUP) {
    if (selectedMembers.value.includes(user_uuid)) {
      selectedMembers.value = selectedMembers.value.filter((element) => {
        return element !== user_uuid
      })
    } else {
      selectedMembers.value.push(user_uuid)
    }
  }
}

const updateUserStatus = (mutation, state) => {
  chatList.value.forEach((element) => {
    if (
      element.chat_type === chatType.DIALOG &&
      element.details.uuid === state.user_uuid
    ) {
      element.details.status = state.status
    }
  })
}

watch(selectedChatType, (newValue) => {
  selectedMembers.value = []
  groupChatName.value = ''
  groupChatImage.value = null
  errors.value = null
})

onMounted(() => {
  getChatList()
  connectionBusStore.$subscribe(updateUserStatus)
  createChatModal.value.addEventListener('show.bs.modal', () => {
    getRelatedUserList()
  })
  createChatModal.value.addEventListener('hidden.bs.modal', () => {
    selectedChatType.value = chatType.DIALOG
    selectedMembers.value = []
    groupChatName.value = ''
    groupChatImage.value = null
    relatedUserList.value = []
    relatedUserListNextURL.value = null
    errors.value = null
  })
  createChatModalBootstrap.value = new bootstrap.Modal(createChatModal.value)
})

onUnmounted(() => {
  closeChatListSocket()
})
</script>

<template>
  <div class="base-messenger-view">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 py-3">
          <div class="d-flex justify-content-evenly d-lg-none">
            <button
              type="button"
              class="btn btn-light border"
              data-bs-toggle="offcanvas"
              data-bs-target="#chat_list"
              aria-controls="chat_list"
            >
              <i class="fa-regular fa-comments"></i>
              {{ $t('messenger.chat_list') }}
            </button>
            <button
              type="button"
              class="btn btn-light border"
              data-bs-toggle="modal"
              data-bs-target="#create_chat_modal"
            >
              {{ $t('messenger.create_chat') }}
              <i class="fa-regular fa-square-plus"></i>
            </button>
          </div>
          <div class="d-none d-lg-flex justify-content-between align-items-center border-bottom pb-3 mb-3">
            <div class="d-inline-block text-uppercase fw-bolder text-secondary">
              {{ $t('messenger.chats') }}
            </div>
            <button
              type="button"
              class="btn btn-light btn-sm"
              data-bs-toggle="modal"
              data-bs-target="#create_chat_modal"
            >
              <i class="fa-regular fa-square-plus"></i>
            </button>
          </div>
          <div
            id="chat_list"
            tabindex="-1"
            class="offcanvas-lg offcanvas-start"
            aria-labelledby="chat_list_label"
          >
            <div class="offcanvas-header border-bottom">
              <h5
                id="chat_list_label"
                class="offcanvas-title"
              >
                {{ $t('messenger.chats') }}
              </h5>
              <button
                ref="chatListClose"
                type="button"
                class="btn-close"
                data-bs-dismiss="offcanvas"
                data-bs-target="#chat_list"
                aria-label="Close"
              ></button>
            </div>
            <div
              ref="chatListArea"
              class="offcanvas-body overflow-y-auto d-lg-block"
            >
              <ul
                v-if="chatList.length > 0"
                class="nav nav-pills flex-column px-1"
              >
                <li
                  v-for="chat in sortedChatList"
                  :key="chat.uuid"
                  :class="[
                    'nav-item',
                    $route.params.uuid === chat.uuid ? 'active' : null
                  ]"
                >
                  <router-link
                    :to="{
                      name: 'Chat',
                      params: { uuid: chat.uuid }
                    }"
                    @click="$refs.chatListClose.click()"
                    :class="[
                      'nav-link',
                      $route.params.uuid === chat.uuid ? 'active' : 'text-dark'
                    ]"
                  >
                    <div class="d-flex gap-3">
                      <UserAvatarExtended
                        v-if="chat.chat_type === chatType.DIALOG"
                        :src="chat.details.avatar"
                        :width="48"
                        :height="48"
                        :online="chat.details.status === 'online' ? true : false"
                      />
                      <GroupAvatar
                        v-else-if="chat.chat_type === chatType.GROUP"
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
                      <div class="flex-grow-1">
                        <div class="d-flex justify-content-between align-items-center">
                          <div
                            v-if="chat.chat_type === chatType.GROUP"
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
                          <small v-if="chat.last_message">
                            {{ getLocaleDateTimeString(chat.last_message.created_at) }}
                          </small>
                        </div>
                        <div
                          v-if="chat.last_message"
                          class="d-flex align-items-center"
                        >
                          <span
                            v-if="chat.last_message.msg_type === messageType.TEXT"
                            class="mb-0 opacity-75 me-auto"
                          >
                            {{ chat.last_message.content }}
                          </span>
                          <span
                            v-else-if="chat.last_message.msg_type === messageType.IMAGES"
                            class="mb-0 opacity-75 me-auto"
                          >
                            {{ $t('messenger.images', { n: chat.last_message.content }) }}
                          </span>
                          <span
                            v-else-if="chat.last_message.msg_type === messageType.FILES"
                            class="mb-0 opacity-75 me-auto"
                          >
                            {{ $t('messenger.files', { n: chat.last_message.content }) }}
                          </span>
                          <span
                            v-if="chat.unviewed_msg_count > 0"
                            class="badge text-bg-primary rounded-pill"
                          >
                            {{ chat.unviewed_msg_count }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </router-link>
                </li>
              </ul>
              <div
                v-else-if="!chatListLoading"
                class="lead d-flex justify-content-center py-3"
              >
                {{ $t('messenger.no_chats') }}
              </div>
              <div
                v-if="nextURL"
                style="min-height: 1px; margin-bottom: 1px;"
                v-intersection="{
                  'scrollArea': chatListArea,
                  'callbackFunction': getMoreChatList,
                  'functionArguments': []
                }"
              ></div>
              <LoadingIndicator v-if="chatListLoading" />
            </div>
          </div>
        </div>
        <div class="col-lg-8 py-lg-2">
          <router-view
            @msgViewed="chatList[chatIndex].unviewed_msg_count -= 1"
            @leaveChat="(chatUUID) => {
              chatList = chatList.filter((element) => {
                return element.uuid !== chatUUID
              })
            }"
          ></router-view>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <div
        ref="createChatModal"
        id="create_chat_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="create_chat_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="create_chat_modal_label"
                class="modal-title"
              >
                {{ $t('messenger.creating_chat') }}
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form
                @submit.prevent="createChat()"
                id="create_chat_form"
              >
                <div class="d-flex justify-content-center mb-3">
                  <div
                    role="group"
                    class="btn-group"
                    aria-label="Chat Type"
                  >
                    <input
                      v-model="selectedChatType"
                      :value="chatType.DIALOG"
                      id="id_chat_type_1"
                      name="chat_type"
                      type="radio"
                      class="btn-check"
                    >
                    <label
                      for="id_chat_type_1"
                      class="btn btn-outline-dark"
                    >
                      {{ $t('messenger.dialog') }}
                    </label>

                    <input
                      v-model="selectedChatType"
                      :value="chatType.GROUP"
                      id="id_chat_type_2"
                      name="chat_type"
                      type="radio"
                      class="btn-check"
                    >
                    <label
                      for="id_chat_type_2"
                      class="btn btn-outline-dark"
                    >
                      {{ $t('messenger.group') }}
                    </label>
                  </div>
                </div>
                <div
                  v-if="selectedChatType === chatType.GROUP"
                  class="mb-3"
                >
                  <BaseInput
                    v-model="groupChatName"
                    type="text"
                    maxlength="150"
                    id="id_name"
                    name="name"
                    :label="$t('messenger.group_name')"
                    :errors="errors?.name ? errors.name : []"
                  />
                </div>
                <div
                  v-if="selectedChatType === chatType.GROUP"
                  class="mb-3"
                >
                  <span v-if="groupChatImage">
                    {{ $t('messenger.chosen_image') }}:
                    {{ groupChatImage.name }}
                  </span>
                  <FileInputButton
                    @selectedFiles="(filelist) => groupChatImage = filelist[0]"
                    buttonClass="btn btn-soft-brand w-100"
                    accept="image/*"
                  >
                    {{ $t('messenger.choose_image') }}
                    <i class="fa-regular fa-image"></i>
                  </FileInputButton>
                  <div
                    v-if="errors && errors.image"
                    id="id_image-errors"
                    class="text-danger"
                    aria-live="assertive"
                  >
                    <small v-for="error in errors.image">
                      {{ error }}
                    </small>
                  </div>
                </div>
                
                <div
                  ref="relatedUserArea"
                  class="border rounded overflow-y-auto"
                >
                  <div v-if="relatedUserList.length > 0">
                    <div
                      v-if="selectedChatType === chatType.DIALOG"
                      class="list-group list-group-flush"
                    >
                      <label
                        v-for="user in relatedUserList"
                        class="list-group-item d-flex align-items-center gap-2"
                      >
                        <input
                          :value="user.uuid"
                          :checked="selectedMembers.includes(user.uuid)"
                          @change="changeSelectedMembers(user.uuid)"
                          type="radio"
                          name="dialog_members"
                          :id="`dialog_member_${user.uuid}`"
                          class="form-check-input"
                        >
                        <UserAvatarExtended
                          :src="user.avatar"
                          :width="32"
                          :height="32"
                          :online="user.status === 'online' ? true : false"
                        />
                        <span class="fw-medium">
                          {{ user.name }}
                        </span>
                      </label>
                    </div>
                    <div
                      v-else-if="selectedChatType === chatType.GROUP"
                      class="list-group list-group-flush"
                    >
                      <label
                        v-for="user in relatedUserList"
                        class="list-group-item d-flex align-items-center gap-2"
                      >
                        <input
                          :value="user.uuid"
                          :checked="selectedMembers.includes(user.uuid)"
                          @change="changeSelectedMembers(user.uuid)"
                          type="checkbox"
                          name="group_members"
                          :id="`group_member_${user.uuid}`"
                          class="form-check-input"
                        >
                        <UserAvatarExtended
                          :src="user.avatar"
                          :width="32"
                          :height="32"
                          :online="user.status === 'online' ? true : false"
                        />
                        <span class="fw-medium">
                          {{ user.name }}
                        </span>
                      </label>
                    </div>
                  </div>
                  <div
                    v-else-if="!relatedUserListLoading"
                    class="lead d-flex justify-content-center py-3"
                  >
                    {{ $t('follow.no_followers_and_following') }}
                  </div>
                  <div
                    v-if="relatedUserListNextURL"
                    style="min-height: 1px; margin-bottom: 1px;"
                    v-intersection="{
                      'scrollArea': relatedUserArea,
                      'callbackFunction': getMoreRelatedUserList,
                      'functionArguments': []
                    }"
                  ></div>
                  <LoadingIndicator v-if="relatedUserListLoading" />
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-light"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.cancel') }}
              </button>
              <SubmitButton
                :loadingStatus="chatCreating"
                buttonClass="btn btn-brand"
                form="create_chat_form"
                :disabled="chatCreationDisabled"
              >
                {{ $t('btn.create') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.border.rounded.overflow-y-auto {
  max-height: 50vh;
}
.offcanvas-body.overflow-y-auto::-webkit-scrollbar,
.border.rounded.overflow-y-auto::-webkit-scrollbar {
  width: 0.3em;
}
.offcanvas-body.overflow-y-auto::-webkit-scrollbar-track,
.border.rounded.overflow-y-auto::-webkit-scrollbar-track {
  background-color: #f5f5f5;
}
.offcanvas-body.overflow-y-auto::-webkit-scrollbar-thumb,
.border.rounded.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 1em;
}
.offcanvas-body.overflow-y-auto::-webkit-scrollbar-thumb:hover,
.border.rounded.overflow-y-auto::-webkit-scrollbar-thumb:hover {
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
  .container > .row {
    border: 1px solid #dee2e6;
    border-radius: 0.375rem;
    margin-top: 0.25rem;
    margin-bottom: 0.25rem
  }
  .offcanvas-body.overflow-y-auto {
    height: 73vh;
  }
  .col-lg-4.py-3 {
    border-right: 1px solid #dee2e6;
  }
}
</style>

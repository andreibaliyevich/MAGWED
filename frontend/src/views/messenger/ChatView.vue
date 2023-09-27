<script setup>
import axios from 'axios'
import { ref, computed, nextTick, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { WS_URL, chatType, messageType } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import GroupAvatar from '@/components/messenger/GroupAvatar.vue'
import MessageContent from '@/components/messenger/MessageContent.vue'

const emit = defineEmits(['msgViewed'])

const route = useRoute()
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const chatDataLoading = ref(false)
const chatData = ref({
  uuid: '',
  chat_type: null,
  details: {
    uuid: '',
    name: '',
    avatar: '',
    status: null,
    profile_url: null
  }
})

const groupChatDataLoading = ref(false)
const groupChatData = ref({
  uuid: '',
  members: [],
  group_details: {
    owner: '',
    name: '',
    image: null
  }
})

const messageListLoading = ref(false)
const messageList = ref([])
const nextURL = ref(null)

const chatSocket = ref(null)
const chatSocketConnect = ref(false)

const messageSending = ref(false)
const textContent = ref('')

const { getLocaleDateTimeString } = useLocaleDateTime()

const errors = ref(null)
const errorStatus = ref(null)

const messageListArea = ref(null)
const msgTextarea = ref(null)

const groupDetailModal = ref(null)
const groupDetailModalBootstrap = ref(null)
const removeChatModalChoice = ref(null)
const leaveChatModalChoice = ref(null)

const reversedMessages = computed(() => {
  return [...messageList.value].reverse()
})

const updateTextareaStyles = () => {
  const { style } = msgTextarea.value
  style.height = style.minHeight = 'auto'
  style.minHeight = `${
    Math.min(
      msgTextarea.value.scrollHeight,
      parseInt(style.maxHeight)
    )
  }px`
  style.height = `${msgTextarea.value.scrollHeight}px`
}

const getMessageList = async () => {
  messageListLoading.value = true
  try {
    const response = await axios.get(
      '/messenger/message/list/?chat='
        + chatData.value.uuid
    )
    messageList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    messageListLoading.value = false
    nextTick(() => {
      messageListArea.value.scrollTo({
        top: messageListArea.value.scrollHeight,
        behavior: 'instant'
      })
      msgTextarea.value.focus()
    })
  }
}

const getMoreMessageList = async () => {
  messageListLoading.value = true
  const scrollHeight = messageListArea.value.scrollHeight
  try {
    const response = await axios.get(nextURL.value)
    messageList.value = [...messageList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    messageListLoading.value = false
    nextTick(() => {
      messageListArea.value.scrollTo({
        top: messageListArea.value.scrollHeight - scrollHeight,
        behavior: 'instant'
      })
    })
  }
}

const openChatSocket = async () => {
  chatSocket.value = new WebSocket(
    WS_URL
      + '/ws/chat/'
      + chatData.value.uuid
      + '/?'
      + userStore.token
  )
  chatSocket.value.onopen = (event) => {
    chatSocketConnect.value = true
  }
  chatSocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.action == 'new_msg') {
      messageList.value.unshift(data.data)
      nextTick(() => {
        messageListArea.value.scrollTo({
          top: messageListArea.value.scrollHeight,
          behavior: 'smooth'
        })
      })
    } else if (data.action == 'viewed') {
      const foundIndex = messageList.value.findIndex((element) => {
        return element.uuid == data.data.msg_uuid
      })
      if (foundIndex != -1) {
        messageList.value[foundIndex].viewed = data.data.msg_viewed
      }
    }
  }
  chatSocket.value.onclose = (event) => {
    chatSocket.value = null
    chatSocketConnect.value = false
  }
  chatSocket.value.onerror = (error) => {
    chatSocket.value = null
    chatSocketConnect.value = false
  }
}

const closeChatSocket = () => {
  if (chatSocket.value) {
    chatSocket.value.close()
  }
}

const getChatData = async () => {
  chatDataLoading.value = true
  try {
    const response = await axios.get(
      '/messenger/chat/retrieve/'
        + route.params.uuid
        +'/'
    )
    chatData.value = response.data
    getMessageList()
    openChatSocket()
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    chatDataLoading.value = false
  }
}

const getGroupChatData = async () => {
  groupChatDataLoading.value = true
  try {
    const response = await axios.get(
      '/messenger/chat/group-retrieve/'
        + chatData.value.uuid
        +'/'
    )
    groupChatData.value = response.data
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    groupChatDataLoading.value = false
  }
}

const sendTextMessage = async () => {
  messageSending.value = true
  try {
    const response = await axios.post(
      '/messenger/message/new/'
        + chatData.value.uuid
        + '/'
        + messageType.TEXT
        + '/',
      {content: textContent.value}
    )
    textContent.value = ''
    nextTick(() => {
      updateTextareaStyles()
      msgTextarea.value.focus()
    })
  } catch (error) {
    errors.value = error.response.data
  } finally {
    messageSending.value = false
  }
}

const sendImageMessage = async (filelist) => {
  messageSending.value = true
  let formData = new FormData()
  for (let i = 0; i < filelist.length; i++) {
    formData.append('content', filelist[i], filelist[i].name)
  }
  try {
    const response = await axios.post(
      '/messenger/message/new/'
        + chatData.value.uuid
        + '/'
        + messageType.IMAGES
        + '/',
      formData
    )
    nextTick(() => {
      msgTextarea.value.focus()
    })
  } catch (error) {
    errors.value = error.response.data
  } finally {
    messageSending.value = false
  }
}

const sendFileMessage = async (filelist) => {
  messageSending.value = true
  let formData = new FormData()
  for (let i = 0; i < filelist.length; i++) {
    formData.append('content', filelist[i], filelist[i].name)
  }
  try {
    const response = await axios.post(
      '/messenger/message/new/'
        + chatData.value.uuid
        + '/'
        + messageType.FILES
        + '/',
      formData
    )
    nextTick(() => {
      msgTextarea.value.focus()
    })
  } catch (error) {
    errors.value = error.response.data
  } finally {
    messageSending.value = false
  }
}

const setMessageViewed = (msg_uuid) => {
  chatSocket.value.send(JSON.stringify({
    'action': 'viewed',
    'msg_uuid': msg_uuid
  }))
  emit('msgViewed')
}

const removeChat = async () => {
  try {
    const response = await axios.delete(
      '/messenger/chat/destroy/' + chatData.value.uuid +'/'
    )
  } catch (error) {
    console.error(error)
  }
}

const leaveChat = async () => {
  try {
    const response = await axios.delete(
      '/messenger/chat/leave/' + chatData.value.uuid +'/'
    )
  } catch (error) {
    console.error(error)
  }
}

const updateUserStatus = (mutation, state) => {
  if (chatData.value.details.uuid == state.user_uuid) {
    chatData.value.details.status = state.status
  }
  messageList.value.forEach((element) => {
    if (element.sender.uuid == state.user_uuid) {
      element.sender.status = state.status
    }
  })
}

watch(
  () => route.params.uuid,
  (newValue) => {
    if (route.name == 'Chat') {
      messageList.value = []
      errorStatus.value = null
      closeChatSocket()
      getChatData()
    }
  }
)

watch(textContent, (newValue) => {
  updateTextareaStyles()
})

onMounted(() => {
  updateTextareaStyles()
  getChatData()
  connectionBusStore.$subscribe(updateUserStatus)
  groupDetailModal.value.addEventListener('show.bs.modal', () => {
    getGroupChatData()
  })
  groupDetailModalBootstrap.value = new bootstrap.Modal(
    groupDetailModal.value
  )
})

onUnmounted(() => {
  closeChatSocket()
})
</script>

<template>
  <div class="chat-view">
    <LoadingIndicator v-if="chatDataLoading" />
    <div
      v-else-if="errorStatus == 404"
      class="d-flex justify-content-center align-items-center h-100"
      style="min-height: 75vh;"
    >
      <div class="text-center">
        <h3>{{ $t('errors.chat_not_found') }}</h3>
      </div>
    </div>
    <div
      v-else
      class="card border-0"
    >
      <div class="card-header bg-white">
        <div
          v-if="chatData.chat_type == chatType.DIALOG"
          class="d-flex align-items-center"
        >
          <UserAvatar
            :src="chatData.details.avatar"
            :width="48"
            :height="48"
          />
          <div class="flex-grow-1 ms-3">
            <h6 class="mt-1 mb-0">{{ chatData.details.name }}</h6>
            <span
              v-if="chatData.details.status == 'online'"
              class="text-dark"
            >
              <i class="fa-solid fa-circle fa-xs text-success"></i>
              {{ $t('user.online') }}
            </span>
            <span
              v-else
              class="text-secondary"
            >
              <i class="fa-solid fa-circle fa-xs"></i>
              {{ $t('user.last_visit') }}
              {{ getLocaleDateTimeString(chatData.details.status) }}
            </span>
          </div>
          <div class="dropdown">
            <button
              type="button"
              class="btn btn-light btn-sm"
              data-bs-toggle="dropdown"
              data-bs-auto-close="true"
              aria-expanded="false"
            >
              <i class="fa-solid fa-ellipsis-vertical"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <li v-if="chatData.details.profile_url">
                <LocaleRouterLink
                  routeName="OrganizerDetail"
                  :routeParams="{ profile_url: chatData.details.profile_url }"
                  class="dropdown-item"
                >
                  <i class="fa-solid fa-user"></i>
                  {{ $t('user.view_profile') }}
                </LocaleRouterLink>
              </li>
              <li>
                <button
                  type="button"
                  class="dropdown-item btn btn-link"
                  data-bs-toggle="modal"
                  data-bs-target="#remove_chat_modal_choice"
                >
                  <i class="fa-solid fa-trash"></i>
                  {{ $t('messenger.delete_chat') }}
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div
          v-else-if="chatData.chat_type == chatType.GROUP"
          class="d-flex align-items-center"
        >
          <GroupAvatar
            :src="chatData.details.image"
            :width="48"
            :height="48"
          />
          <div class="flex-grow-1 ms-3">
            <h6 class="mt-1 mb-0">{{ chatData.details.name }}</h6>
            <span class="text-secondary">
              {{ $t('messenger.member_count', {n: chatData.details.member_count}) }}
            </span>
          </div>
          <div class="dropdown">
            <button
              type="button"
              class="btn btn-light btn-sm"
              data-bs-toggle="dropdown"
              data-bs-auto-close="true"
              aria-expanded="false"
            >
              <i class="fa-solid fa-ellipsis-vertical"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <button
                  type="button"
                  class="dropdown-item btn btn-link"
                  data-bs-toggle="modal"
                  data-bs-target="#group_detail_modal"
                >
                  <i class="fa-solid fa-user-group"></i>
                  {{ $t('messenger.view_group_detail') }}
                </button>
              </li>
              <li v-if="chatData.details.owner == userStore.uuid">
                <button
                  type="button"
                  class="dropdown-item btn btn-link"
                  data-bs-toggle="modal"
                  data-bs-target="#remove_chat_modal_choice"
                >
                  <i class="fa-solid fa-trash"></i>
                  {{ $t('messenger.delete_and_leave_group') }}
                </button>
              </li>
              <li v-else>
                <button
                  type="button"
                  class="dropdown-item btn btn-link"
                  data-bs-toggle="modal"
                  data-bs-target="#leave_chat_modal_choice"
                >
                  <i class="fa-solid fa-trash"></i>
                  {{ $t('messenger.leave_group') }}
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div
          v-else
          class="d-flex align-items-center"
        >
          <img
            src="/chat.jpg"
            class="rounded-circle"
            width="48"
            height="48"
          >
        </div>
      </div>
      <div
        ref="messageListArea"
        class="card-body overflow-y-auto"
      >
        <LoadingIndicator v-if="messageListLoading" />
        <div
          v-if="nextURL"
          style="min-height: 1px; margin-top: 1px;"
          v-intersection="{
            'scrollArea': messageListArea,
            'callbackFunction': getMoreMessageList,
            'functionArguments': []
          }"
        ></div>
        <div
          v-if="messageList.length > 0"
          class="my-3"
        >
          <div
            v-for="msg in reversedMessages"
            class="my-3"
          >
            <div
              v-if="msg.sender.uuid == userStore.uuid"
              class="d-flex justify-content-end"
            >
              <div class="my-0">
                <div class="bg-primary rounded p-2">
                  <MessageContent
                    :msgType="msg.msg_type"
                    :msgContent="msg.content"
                    textClass="fs-6 text-white"
                  />
                  <div class="d-flex justify-content-end text-white mt-2">
                    <i
                      v-if="msg.viewed"
                      class="fa-solid fa-check-double fa-sm"
                    ></i>
                    <i
                      v-else
                      class="fa-solid fa-check fa-sm"
                    ></i>
                  </div>
                </div>
                <small class="d-flex justify-content-end text-muted">
                  {{ getLocaleDateTimeString(msg.created_at) }}
                </small>
              </div>
            </div>
            <div
              v-else
              class="d-flex justify-content-start"
            >
              <div class="my-0">
                <div
                  v-if="chatData.chat_type == chatType.GROUP"
                  class="d-flex align-items-start"
                >
                  <UserAvatarExtended
                    :src="msg.sender.avatar"
                    :width="36"
                    :height="36"
                    :online="msg.sender.status == 'online' ? true : false"
                  />
                  <div class="bg-light rounded p-2 ms-2">
                    <p class="fw-bold mb-0">{{ msg.sender.name }}</p>
                    <MessageContent
                      v-if="msg.viewed || !chatSocketConnect"
                      :msgType="msg.msg_type"
                      :msgContent="msg.content"
                    />
                    <MessageContent
                      v-else
                      :msgType="msg.msg_type"
                      :msgContent="msg.content"
                      v-intersection="{
                        'scrollArea': messageListArea,
                        'callbackFunction': setMessageViewed,
                        'functionArguments': [msg.uuid]
                      }"
                    />
                  </div>
                </div>
                <div
                  v-else
                  class="bg-light rounded p-2"
                >
                  <MessageContent
                    v-if="msg.viewed || !chatSocketConnect"
                    :msgType="msg.msg_type"
                    :msgContent="msg.content"
                  />
                  <MessageContent
                    v-else
                    :msgType="msg.msg_type"
                    :msgContent="msg.content"
                    v-intersection="{
                      'scrollArea': messageListArea,
                      'callbackFunction': setMessageViewed,
                      'functionArguments': [msg.uuid]
                    }"
                  />
                </div>
                <small class="text-muted">
                  {{ getLocaleDateTimeString(msg.created_at) }}
                </small>
              </div>
            </div>
          </div>
        </div>
        <div
          v-else-if="!messageListLoading"
          class="d-flex justify-content-center align-items-center h-100"
        >
          <div class="text-center">
            <i class="fa-regular fa-message fa-2xl"></i>
            <p class="lead mt-3">{{ $t('messenger.no_messages') }}</p>
          </div>
        </div>
        <div
          v-if="messageSending"
          class="d-flex justify-content-end"
        >
          <div
            role="status"
            class="spinner-border spinner-border-sm"
          >
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
      <div class="card-footer bg-white">
        <div class="d-flex align-items-end gap-2">
          <FileInputButton
            @selectedFiles="sendImageMessage"
            buttonClass="btn btn-light"
            accept="image/*"
            multiple
          >
            <i class="fa-solid fa-file-image"></i>
          </FileInputButton>
          <FileInputButton
            @selectedFiles="sendFileMessage"
            buttonClass="btn btn-light"
            multiple
          >
            <i class="fa-solid fa-file"></i>
          </FileInputButton>
          <div class="d-flex align-items-center border rounded w-100">
            <textarea
              ref="msgTextarea"
              v-model="textContent"
              @keyup.ctrl.enter="sendTextMessage()"
              :placeholder="$t('messenger.type_message')"
              rows="1"
              class="form-control border-0"
              style="max-height: 150px;"
            ></textarea>
            <button
              @click="sendTextMessage()"
              type="button"
              class="btn btn-link"
              :disabled="!textContent"
            >
              <i class="fa-solid fa-paper-plane"></i>
            </button>
          </div>
        </div>
        <small>{{ $t('form_help.textarea_message') }}</small>
      </div>
    </div>

    <Teleport to="body">
      <div
        ref="groupDetailModal"
        id="group_detail_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="group_detail_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="group_detail_modal_label"
                class="modal-title"
              >
                {{ $t('messenger.group_chat_details') }}
              </h5>
              <button
                class="btn-close"
                type="button"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <LoadingIndicator v-if="groupChatDataLoading" />
              <div v-else>
                <div class="d-flex align-items-center">
                  <GroupAvatar
                    :src="groupChatData.group_details.image"
                    :width="64"
                    :height="64"
                  />
                  <div class="ms-3">
                    <p class="h4 mb-0">{{ groupChatData.group_details.name }}</p>
                    <span class="text-secondary">
                      {{ $t('messenger.member_count', {n: groupChatData.members.length}) }}
                    </span>
                  </div>
                </div>

                <p class="lead mt-3">{{ $t('messenger.members') }}:</p>
                <div class="border rounded overflow-y-auto">
                  <div
                    v-if="groupChatData.members.length > 0"
                    class="list-group list-group-flush"
                  >
                    <label
                      v-for="user in groupChatData.members"
                      class="list-group-item list-group-item-action"
                    >
                      <LocaleRouterLink
                        v-if="user.profile_url"
                        routeName="OrganizerDetail"
                        :routeParams="{ profile_url: user.profile_url }"
                        @click="groupDetailModalBootstrap.hide()"
                        class="text-decoration-none link-dark d-flex align-items-center gap-2"
                      >
                        <UserAvatarExtended
                          :src="user.avatar"
                          :width="32"
                          :height="32"
                          :online="user.status == 'online' ? true : false"
                        />
                        <span class="fw-medium">
                          {{ user.name }}
                        </span>
                        <i
                          v-if="user.uuid == groupChatData.group_details.owner"
                          class="fa-solid fa-star"
                        ></i>
                      </LocaleRouterLink>
                      <div
                        v-else
                        class="d-flex align-items-center gap-2"
                      >
                        <UserAvatarExtended
                          :src="user.avatar"
                          :width="32"
                          :height="32"
                          :online="user.status == 'online' ? true : false"
                        />
                        <span class="fw-medium">
                          {{ user.name }}
                        </span>
                      </div>
                    </label>
                  </div>
                  <div
                    v-else
                    class="lead d-flex justify-content-center py-3"
                  >
                    {{ $t('follow.no_followers_and_following') }}
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button
                class="btn btn-light"
                type="button"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.close') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        ref="removeChatModalChoice"
        id="remove_chat_modal_choice"
        class="modal fade"
        role="dialog"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div
          class="modal-dialog modal-dialog-centered"
          role="document"
        >
          <div class="modal-content rounded-3 shadow">
            <div class="modal-body p-4 text-center">
              <h5 class="mb-0">{{ $t('messenger.you_want_remove_chat') }}</h5>
              <p class="mb-0">{{ $t('messenger.chat_messages_will_lost') }}</p>
            </div>
            <div class="modal-footer flex-nowrap p-0">
              <button
                @click="removeChat()"
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0 border-end"
                type="button"
                data-bs-dismiss="modal"
              >
                <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
              </button>
              <button
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0"
                type="button"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.no_cancel') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        ref="leaveChatModalChoice"
        id="leave_chat_modal_choice"
        class="modal fade"
        role="dialog"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div
          class="modal-dialog modal-dialog-centered"
          role="document"
        >
          <div class="modal-content rounded-3 shadow">
            <div class="modal-body p-4 text-center">
              <h5 class="mb-0">{{ $t('messenger.you_want_leave_chat') }}</h5>
              <p class="mb-0">{{ $t('messenger.you_will_lose_access_chat_messages') }}</p>
            </div>
            <div class="modal-footer flex-nowrap p-0">
              <button
                @click="leaveChat()"
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0 border-end"
                type="button"
                data-bs-dismiss="modal"
              >
                <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
              </button>
              <button
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0"
                type="button"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.no_cancel') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.card-body.overflow-y-auto {
  height: 65vh;
}
.border.rounded.overflow-y-auto {
  max-height: 50vh;
}
.card-body.overflow-y-auto::-webkit-scrollbar,
.border.rounded.overflow-y-auto::-webkit-scrollbar {
  width: 0.3em;
}
textarea {
  resize: none;
}
textarea::-webkit-scrollbar {
  width: 0.2em;
}
.card-body.overflow-y-auto::-webkit-scrollbar-track,
.border.rounded.overflow-y-auto::-webkit-scrollbar-track,
textarea::-webkit-scrollbar-track {
  background-color: #f5f5f5;
}
.card-body.overflow-y-auto::-webkit-scrollbar-thumb,
.border.rounded.overflow-y-auto::-webkit-scrollbar-thumb,
textarea::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 1em;
}
.card-body.overflow-y-auto::-webkit-scrollbar-thumb:hover,
.border.rounded.overflow-y-auto::-webkit-scrollbar-thumb:hover,
textarea::-webkit-scrollbar-thumb:hover {
  background-color: #e72a26;
}

.d-flex.align-items-center.border.rounded.w-100:hover,
.d-flex.align-items-center.border.rounded.w-100:focus-within {
  border-color: #e72a26 !important;
}
</style>

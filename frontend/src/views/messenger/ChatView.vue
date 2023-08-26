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

const route = useRoute()
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const chatLoading = ref(false)
const chat = ref({
  uuid: '',
  chat_type: null,
  details: {
    uuid: '',
    name: '',
    avatar: '',
    online: null,
    profile_url: null
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

const scrollArea = ref(null)
const msgTextarea = ref(null)

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
        + chat.value.uuid
    )
    messageList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    messageListLoading.value = false
    nextTick(() => {
      scrollArea.value.scrollTo({
        top: scrollArea.value.scrollHeight,
        behavior: 'instant'
      })
      msgTextarea.value.focus()
    })
  }
}

const getMoreMessageList = async () => {
  messageListLoading.value = true
  const scrollHeight = scrollArea.value.scrollHeight
  try {
    const response = await axios.get(nextURL.value)
    messageList.value = [...messageList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    messageListLoading.value = false
    nextTick(() => {
      scrollArea.value.scrollTo({
        top: scrollArea.value.scrollHeight - scrollHeight,
        behavior: 'instant'
      })
    })
  }
}

const openConvoSocket = async () => {
  chatSocket.value = new WebSocket(
    WS_URL
      + '/ws/messenger/'
      + chat.value.uuid
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
        scrollArea.value.scrollTo({
          top: scrollArea.value.scrollHeight,
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

const closeConvoSocket = () => {
  if (chatSocket.value) {
    chatSocket.value.close()
  }
}

const getChatData = async () => {
  chatLoading.value = true
  try {
    const response = await axios.get(
      '/messenger/chat/retrieve/'
        + route.params.uuid
        +'/'
    )
    chat.value = response.data
    getMessageList()
    openConvoSocket()
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    chatLoading.value = false
  }
}

const sendTextMessage = async () => {
  messageSending.value = true
  try {
    const response = await axios.post('/messenger/message/text/', {
      chat: chat.value.uuid,
      content: textContent.value
    })
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
  const imagesData = new FormData()
  imagesData.append('chat', chat.value.uuid)
  for (let i = 0; i < filelist.length; i++) {
    imagesData.append('content', filelist[i], filelist[i].name)
  }
  try {
    const response = await axios.post('/messenger/message/images/', imagesData)
  } catch (error) {
    errors.value = error.response.data
  } finally {
    messageSending.value = false
  }
}

const sendFileMessage = async (filelist) => {
  messageSending.value = true
  const filesData = new FormData()
  filesData.append('chat', chat.value.uuid)
  for (let i = 0; i < filelist.length; i++) {
    filesData.append('content', filelist[i], filelist[i].name)
  }
  try {
    const response = await axios.post('/messenger/message/files/', filesData)
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
}

const updateUserStatus = (mutation, state) => {
  messageList.value.forEach((element) => {
    if (element.sender.uuid == state.user_uuid) {
      element.sender.online = state.online
    }
  })
}

const vIntersectionMessages = {
  mounted(el) {
    const options = {
      root: scrollArea.value,
      rootMargin: '0px',
      threshold: 1.0
    }
    const callback = (entries, observer) => {
      if (entries[0].isIntersecting) {
        getMoreMessageList()
      }
    }
    const observer = new IntersectionObserver(callback, options)
    observer.observe(el)
  }
}
const vIntersectionMessage = {
  mounted(el, binding) {
    const options = {
      root: scrollArea.value,
      rootMargin: '0px',
      threshold: 1.0
    }
    const callback = (entries, observer) => {
      if (entries[0].isIntersecting) {
        setMessageViewed(binding.value)
      }
    }
    const observer = new IntersectionObserver(callback, options)
    observer.observe(el)
  }
}

watch(
  () => route.params.uuid,
  (newValue) => {
    if (route.name == 'Chat') {
      messageList.value = []
      errorStatus.value = null
      closeConvoSocket()
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
})

onUnmounted(() => {
  closeConvoSocket()
})
</script>

<template>
  <div class="chat-view">
    <LoadingIndicator v-if="chatLoading" />
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
        <div class="d-flex align-items-center">
          <div class="flex-shrink-0">
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
          </div>
          <div class="flex-grow-1 ms-3">
            <strong>{{ chat.details.name }}</strong>
          </div>
        </div>
      </div>
      <div
        ref="scrollArea"
        class="card-body overflow-auto"
      >
        <LoadingIndicator v-if="messageListLoading" />
        <div v-if="nextURL" v-intersection-messages></div>
        <div
          v-if="messageList.length > 0"
          class="my-3"
        >
          <div v-for="msg in reversedMessages">
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
                  v-if="chat.chat_type == chatType.GROUP"
                  class="d-flex align-items-start"
                >
                  <UserAvatarExtended
                    :src="msg.sender.avatar"
                    :width="48"
                    :height="48"
                    :online="msg.sender.online"
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
                      v-intersection-message="msg.uuid"
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
                    v-intersection-message="msg.uuid"
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
  </div>
</template>

<style scoped>
.card-body.overflow-auto {
  height: 60vh;
}
.card-body.overflow-auto::-webkit-scrollbar {
  width: 0.3em;
}
textarea {
  resize: none;
}
textarea::-webkit-scrollbar {
  width: 0.2em;
}
.card-body.overflow-auto::-webkit-scrollbar-track,
textarea::-webkit-scrollbar-track {
  background-color: #f5f5f5;
}
.card-body.overflow-auto::-webkit-scrollbar-thumb,
textarea::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 1em;
}
.card-body.overflow-auto::-webkit-scrollbar-thumb:hover,
textarea::-webkit-scrollbar-thumb:hover {
  background-color: #e72a26;
}

.d-flex.align-items-center.border.rounded.w-100:hover,
.d-flex.align-items-center.border.rounded.w-100:focus-within {
  border-color: #e72a26 !important;
}
</style>

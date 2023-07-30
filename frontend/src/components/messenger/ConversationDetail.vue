<script setup>
import axios from 'axios'
import { ref, computed, nextTick, watch, onMounted, onUnmounted } from 'vue'
import { WS_URL, conversationType, messageType } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import GroupAvatar from './GroupAvatar.vue'
import MessageContent from './MessageContent.vue'

const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const props = defineProps({
  conversation: {
    type: Object,
    required: true
  }
})

const messageListLoading = ref(true)
const messageList = ref([])
const nextURL = ref(null)

const convoSocket = ref(null)
const convoSocketConnect = ref(false)

const message = ref('')

const { getLocaleDateTimeString } = useLocaleDateTime()

const scrollArea = ref(null)
const msgTextarea = ref(null)

const reversedMessages = computed(() => {
  return [...messageList.value].reverse()
})

const getMessageList = async () => {
  messageList.value = true
  try {
    const response = await axios.get(
      '/messenger/messages/'
      + props.conversation.uuid
      + '/'
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
  convoSocket.value = new WebSocket(
    WS_URL
    + '/ws/messenger/'
    + props.conversation.uuid
    + '/?'
    + userStore.token
  )
  convoSocket.value.onopen = (event) => {
    convoSocketConnect.value = true
  }
  convoSocket.value.onmessage = (event) => {
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
  convoSocket.value.onclose = (event) => {
    convoSocket.value = null
    convoSocketConnect.value = false
  }
  convoSocket.value.onerror = (error) => {
    convoSocket.value = null
    convoSocketConnect.value = false
  }
}

const closeConvoSocket = () => {
  if (convoSocket.value) {
    convoSocket.value.close()
  }
}

const sendMessage = () => {
  if (message.value) {
    convoSocket.value.send(JSON.stringify({
      'action': 'new_msg',
      'msg_type': messageType.TEXT,
      'content': message.value
    }))
    message.value = ''
    nextTick(() => {
      updateTextareaStyles()
      msgTextarea.value.focus()
    })
  }
}

const sendImages = async (filelist) => {
  const imagesData = new FormData()
  imagesData.append('conversation', props.conversation.uuid)
  for (let i = 0; i < filelist.length; i++) {
    imagesData.append('content', filelist[i], filelist[i].name)
  }
  try {
    const response = await axios.post('/messenger/message/images/', imagesData)
    convoSocket.value.send(JSON.stringify({
      'action': 'new_msg',
      'msg_type': messageType.IMAGES,
      'data': response.data
    }))
  } catch (error) {
    console.error(error)
  }
}

const sendFiles = async (filelist) => {
  const filesData = new FormData()
  filesData.append('conversation', props.conversation.uuid)
  for (let i = 0; i < filelist.length; i++) {
    filesData.append('content', filelist[i], filelist[i].name)
  }
  try {
    const response = await axios.post('/messenger/message/files/', filesData)
    convoSocket.value.send(JSON.stringify({
      'action': 'new_msg',
      'msg_type': messageType.FILES,
      'data': response.data
    }))
  } catch (error) {
    console.error(error)
  }
}

const setMessageViewed = (msg_uuid) => {
  convoSocket.value.send(JSON.stringify({
    'action': 'viewed',
    'msg_uuid': msg_uuid
  }))
}

const updateTextareaStyles = () => {
  const { style } = msgTextarea.value
  style.height = style.minHeight = 'auto'
  style.minHeight = `${
    Math.min(msgTextarea.value.scrollHeight,
      parseInt(style.maxHeight))
  }px`
  style.height = `${ msgTextarea.value.scrollHeight }px`
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

watch(() => props.conversation, (newValue) => {
  messageList.value = []
  closeConvoSocket()
  getMessageList()
  openConvoSocket()
})

watch(message, (newValue) => {
  updateTextareaStyles()
})

onMounted(() => {
  getMessageList()
  openConvoSocket()
  updateTextareaStyles()
  connectionBusStore.$subscribe(updateUserStatus)
})

onUnmounted(() => {
  closeConvoSocket()
})
</script>

<template>
  <div class="conversation-detail">
    <div class="card border-0">
      <div class="card-header bg-white">
        <div class="d-flex align-items-center">
          <div class="flex-shrink-0">
            <UserAvatarExtended
              v-if="conversation.convo_type == conversationType.DIALOG"
              :src="conversation.details.avatar"
              :width="48"
              :height="48"
              :online="conversation.details.online"
            />
            <GroupAvatar
              v-else-if="conversation.convo_type == conversationType.GROUP"
              :src="conversation.details.image"
              :width="48"
              :height="48"
            />
            <img
              v-else
              src="/conversation.jpg"
              class="rounded-circle"
              width="48"
              height="48"
            >
          </div>
          <div class="flex-grow-1 ms-3">
            <strong>{{ this.conversation.details.name }}</strong>
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
                  v-if="conversation.convo_type == conversationType.GROUP"
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
                      v-if="msg.viewed || !convoSocketConnect"
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
                    v-if="msg.viewed || !convoSocketConnect"
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
      </div>
      <div class="card-footer bg-white">
        <div class="d-flex align-items-end gap-2">
          <FileInputButton
            @selectedFiles="sendImages"
            buttonClass="btn btn-light"
            accept="image/*"
            multiple
          >
            <i class="fa-solid fa-file-image"></i>
          </FileInputButton>
          <FileInputButton
            @selectedFiles="sendFiles"
            buttonClass="btn btn-light"
            multiple
          >
            <i class="fa-solid fa-file"></i>
          </FileInputButton>
          <div class="d-flex align-items-center border rounded w-100">
            <textarea
              ref="msgTextarea"
              v-model="message"
              @keyup.ctrl.enter="sendMessage()"
              :placeholder="$t('messenger.type_message')"
              rows="1"
              class="form-control border-0"
              style="max-height: 150px;"
            ></textarea>
            <button
              @click="sendMessage()"
              type="button"
              class="btn btn-link"
              :disabled="!convoSocketConnect || !message"
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

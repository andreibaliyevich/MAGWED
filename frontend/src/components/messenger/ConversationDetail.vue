<script setup>
import axios from 'axios'
import { ref, nextTick, watch, onMounted, onUnmounted } from 'vue'
import { API_URL, WS_URL, conversationType, messageType } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import UserAvatar from '@/components/auth/UserAvatar.vue'
import GroupAvatar from '@/components/auth/GroupAvatar.vue'
import MessageContent from '@/components/messenger/MessageContent.vue'

const { getLocaleDateTimeString } = useLocaleDateTime()
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const props = defineProps({
  conversation: {
    type: Object,
    required: true
  }
})

const messagesLoading = ref(true)
const convoSocket = ref(null)
const messages = ref([])
const message = ref('')

const cardBody = ref(null)
const msgTextarea = ref(null)

const closeConversation = () => {
  if (convoSocket.value) {
    convoSocket.value.close()
  }
}

const openConversation = async () => {
  messagesLoading.value = true
  try {
    const response = await axios.get('/accounts/auth/wstoken/')
    convoSocket.value = new WebSocket(
      WS_URL
      + '/ws/messenger/'
      + props.conversation.id
      + '/?'
      + response.data.wstoken
    )
    convoSocket.value.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.messages) {
        messages.value = data.messages
        nextTick(() => {
          cardBody.value.scrollTop = cardBody.value.scrollHeight
          msgTextarea.value.focus()
        })
      } else {
        messages.value.push(data)
        nextTick(() => {
          cardBody.value.scrollTo({
            top: cardBody.value.scrollHeight,
            behavior: 'smooth'
          })
        })
      }
    }
    convoSocket.value.onerror = (event) => {
      convoSocket.value = null
      conversation.value = {}
      messages.value = []
    }
  } catch (error) {
    console.error(error)
  } finally {
    messagesLoading.value = false
  }
}

const sendMessage = () => {
  convoSocket.value.send(JSON.stringify({
    'msg_type': messageType.TEXT,
    'content': message.value
  }))
  message.value = ''
}

const sendImages = async (filelist) => {
  const imagesData = new FormData()
  imagesData.append('conversation', props.conversation.id)
  for (let i = 0; i < filelist.length; i++) {
    imagesData.append('content', filelist[i], filelist[i].name)
  }
  try {
    const response = await axios.post('/messenger/message/images/', imagesData)
    convoSocket.value.send(JSON.stringify({
      'msg_type': messageType.IMAGES,
      'msg_data': response.data
    }))
  } catch (error) {
    console.error(error)
  }
}

const sendFiles = async (filelist) => {
  const filesData = new FormData()
  filesData.append('conversation', props.conversation.id)
  for (let i = 0; i < filelist.length; i++) {
    filesData.append('content', filelist[i], filelist[i].name)
  }
  try {
    const response = await axios.post('/messenger/message/files/', filesData)
    convoSocket.value.send(JSON.stringify({
      'msg_type': messageType.FILES,
      'msg_data': response.data
    }))
  } catch (error) {
    console.error(error)
  }
}

const updateUserStatus = (mutation, state) => {
  messages.value.forEach((element) => {
    if (element.sender.id == state.user_id) {
      element.sender.online = state.online
    }
  })
}

watch(() => props.conversation, (newValue) => {
  messages.value = []
  closeConversation()
  openConversation()
})

watch(message, (newValue) => {
  msgTextarea.value.rows = message.value.split('\n').length
})

onMounted(() => {
  openConversation()
  connectionBusStore.$subscribe(updateUserStatus)
})

onUnmounted(() => {
  closeConversation()
})
</script>

<template>
  <div class="conversation-detail">
    <div class="card border-0">
      <div class="card-header bg-white">
        <div class="d-flex align-items-center">
          <div class="flex-shrink-0">
            <div v-if="conversation.convo_type == conversationType.DIALOG">
              <UserAvatar
                :src="conversation.details.avatar"
                :width="48"
                :height="48"
                :online="conversation.details.online"
              />
            </div>
            <div v-else-if="conversation.convo_type == conversationType.GROUP">
              <GroupAvatar
                :src="conversation.details.image"
                :width="48"
                :height="48"
              />
            </div>
            <div v-else>
              <img
                src="/conversation.jpg"
                class="rounded-circle"
                width="48"
                height="48"
              >
            </div>
          </div>
          <div class="flex-grow-1 ms-3">
            <strong>{{ this.conversation.details.name }}</strong>
          </div>
        </div>
      </div>
      <div
        ref="cardBody"
        class="card-body overflow-auto"
      >
        <LoadingIndicator v-if="messagesLoading" />
        <div
          v-else
          v-for="msg in messages"
          class="my-3"
        >
          <div
            v-if="msg.sender.id == userStore.id"
            class="d-flex justify-content-end"
          >
            <div class="my-0">
              <div class="bg-primary rounded p-2">
                <MessageContent
                  :msgType="msg.msg_type"
                  :msgContent="msg.content"
                  textClass="fs-6 text-white"
                />
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
                <UserAvatar
                  :src="`${ API_URL }${ msg.sender.avatar }`"
                  :width="32"
                  :height="32"
                  :online="msg.sender.online"
                />
                <div class="bg-light rounded p-2 ms-2">
                  <p class="fw-bold mb-0">{{ msg.sender.name }}</p>
                  <MessageContent
                    :msgType="msg.msg_type"
                    :msgContent="msg.content"
                  />
                </div>
              </div>
              <div
                v-else
                class="bg-light rounded p-2"
              >
                <MessageContent
                  :msgType="msg.msg_type"
                  :msgContent="msg.content"
                />
              </div>
              <small class="text-muted">
                {{ getLocaleDateTimeString(msg.created_at) }}
              </small>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer bg-white">
        <div class="hstack gap-2">
          <FileInputButton
            @updateFile="sendImages"
            buttonClass="btn btn-light"
            accept="image/*"
            multiple
          >
            <i class="fa-solid fa-file-image"></i>
          </FileInputButton>
          <FileInputButton
            @updateFile="sendFiles"
            buttonClass="btn btn-light"
            multiple
          >
            <i class="fa-solid fa-file"></i>
          </FileInputButton>
          <textarea
            ref="msgTextarea"
            v-model="message"
            class="form-control me-auto"
            :placeholder="$t('messenger.type_message')"
            rows="1"
          ></textarea>
          <button
            v-if="message"
            @click="sendMessage()"
            class="btn btn-primary"
            type="button"
          >
            <i class="fa-solid fa-paper-plane"></i>
          </button>
          <button
            v-else
            class="btn btn-primary"
            type="button"
            disabled
          >
            <i class="fa-solid fa-paper-plane"></i>
          </button>
        </div>
      </div>
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

.card-body {
  height: 60vh;
}
.text-sm.mb-0 {
  white-space: pre-line;
}

textarea {
  resize: none;
}
</style>

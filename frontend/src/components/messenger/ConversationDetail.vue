<script setup>
import axios from 'axios'
import { nextTick } from 'vue'

import { API_URL, WS_URL } from '@/config.js'

import useLocaleDateTime from '@/composables/useLocaleDateTime.js'
const getLocaleDateTimeString = useLocaleDateTime()

import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()

import { useConnectionBusStore } from '@/stores/connectionBus.js'
const connectionBusStore = useConnectionBusStore()

import UserAvatar from '@/components/auth/UserAvatar.vue'
import GroupAvatar from '@/components/auth/GroupAvatar.vue'
import MessageContent from '@/components/messenger/MessageContent.vue'
</script>

<script>
export default {
  props: {
    conversationType: {
      type: Object,
      required: true
    },
    messageType: {
      type: Object,
      required: true
    },
    conversation: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      convoSocket: null,
      messages: [],
      messagesLoading: false,
      message: ''
    }
  },
  methods: {
    closeConversation() {
      if (this.convoSocket) {
        this.convoSocket.close()
      }
    },
    openConversation() {
      this.closeConversation()
      axios.get('/accounts/auth/wstoken/')
      .then((response) => {
        this.convoSocket = new WebSocket(
          WS_URL
          + '/ws/messenger/'
          + this.conversation.id
          + '/?'
          + response.data.wstoken
        )

        this.convoSocket.onopen = (event) => {
          this.messagesLoading = true
        }

        this.convoSocket.onmessage = (event) => {
          const data = JSON.parse(event.data)
          if (data.messages) {
            this.messages = data.messages
            this.messagesLoading = false
            nextTick(() => {
              this.$refs.cardBody.scrollTop = this.$refs.cardBody.scrollHeight
              this.$refs.msgTextarea.focus()
            })
          } else {
            this.messages.push(data)
            nextTick(() => {
              this.$refs.cardBody.scrollTo({
                top: this.$refs.cardBody.scrollHeight,
                behavior: 'smooth'
              })
            })
          }
        }

        this.convoSocket.onerror = (event) => {
          this.convoSocket = null
          this.conversation = {}
          this.messages = []
        }

        this.status = 'wstoken'
        this.errors = null
      })
      .catch((error) => {
        this.status = null
        this.errors = error.data
      })
    },
    sendMessage() {
      this.convoSocket.send(JSON.stringify({
        'msg_type': this.messageType.TEXT,
        'content': this.message
      }))
      this.message = ''
    },
    sendImages(filelist) {
      const imagesData = new FormData()
      imagesData.append('conversation', this.conversation.id)
      for (let i = 0; i < filelist.length; i++) {
        imagesData.append('content', filelist[i], filelist[i].name)
      }

      axios.post('/messenger/message/images/', imagesData)
      .then((response) => {
        this.convoSocket.send(JSON.stringify({
          'msg_type': 2,
          'msg_data': response.data
        }))
      })
    },
    sendFiles(filelist) {
      const filesData = new FormData()
      filesData.append('conversation', this.conversation.id)
      for (let i = 0; i < filelist.length; i++) {
        filesData.append('content', filelist[i], filelist[i].name)
      }

      axios.post('/messenger/message/files/', filesData)
      .then((response) => {
        this.convoSocket.send(JSON.stringify({
          'msg_type': 3,
          'msg_data': response.data
        }))
      })
    },
    updateUserStatus(mutation, state) {
      this.messages.forEach((element) => {
        if (element.sender.id == state.user_id) {
          element.sender.online = state.online
        }
      })
    }
  },
  watch: {
    conversation(newValue) {
      this.openConversation()
    },
    message(newValue) {
      this.$refs.msgTextarea.rows = this.message.split('\n').length
    }
  },
  mounted() {
    this.openConversation()
    this.connectionBusStore.$subscribe(this.updateUserStatus)
  },
  unmounted() {
    this.closeConversation()
  }
}
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
                :width="50"
                :height="50"
                :online="conversation.details.online"
              />
            </div>
            <div v-else-if="conversation.convo_type == conversationType.GROUP">
              <GroupAvatar
                :src="conversation.details.image"
                :width="50"
                :height="50"
              />
            </div>
            <div v-else>
              <img
                src="/conversation.jpg"
                class="rounded-circle"
                width="50"
                height="50"
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
        <ActionProcessingIndicator v-if="messagesLoading" />
        <div
          v-else
          v-for="msg in messages"
          class="mt-1"
        >
          <div
            v-if="msg.sender.id == userStore.id"
            class="d-flex justify-content-end"
          >
            <div class="my-0">
              <div class="bg-primary rounded p-2 mb-2">
                <p class="text-sm mb-0 text-white">
                  <MessageContent
                    :messageType="messageType"
                    :msgType="msg.msg_type"
                    :msgContent="msg.content"
                  />
                </p>
              </div>
              <p class="d-flex justify-content-end small text-muted">
                {{ getLocaleDateTimeString($i18n.locale, msg.created_at) }}
              </p>
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
                  :width="35"
                  :height="35"
                  :online="msg.sender.online"
                />
                <div class="bg-light rounded p-2 ms-2 mb-2">
                  <p class="fw-bold mb-0">{{ msg.sender.name }}</p>
                  <p class="text-sm mb-0">
                    <MessageContent
                      :messageType="messageType"
                      :msgType="msg.msg_type"
                      :msgContent="msg.content"
                    />
                  </p>
                </div>
              </div>
              <div
                v-else
                class="bg-light rounded p-2 mb-2"
              >
                <p class="text-sm mb-0 text-dark">
                  <MessageContent
                    :messageType="messageType"
                    :msgType="msg.msg_type"
                    :msgContent="msg.content"
                  />
                </p>
              </div>
              <p class="small text-muted">
                {{ getLocaleDateTimeString($i18n.locale, msg.created_at) }}
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer bg-white">
        <div class="hstack gap-2">
          <FileInputButton
            @updateFile="sendImages"
            accept="image/*"
            multiple
            classButton="btn btn-light"
          >
            <i class="fa-solid fa-file-image"></i>
          </FileInputButton>
          <FileInputButton
            @updateFile="sendFiles"
            multiple
            classButton="btn btn-light"
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
            @click="sendMessage"
            type="button"
            class="btn btn-primary"
          >
            <i class="fa-solid fa-paper-plane"></i>
          </button>
          <button
            v-else
            type="button"
            class="btn btn-primary"
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

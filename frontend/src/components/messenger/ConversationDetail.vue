<script setup>
import axios from 'axios'
import { nextTick } from 'vue'

import ToLocaleDateTimeString from '@/mixins/ToLocaleDateTimeString.js'

import UserAvatar from '@/components/auth/UserAvatar.vue'
import MessageContent from '@/components/messenger/MessageContent.vue'

import { useBaseStore } from '@/stores/base.js'
import { useUserStore } from '@/stores/user.js'
const baseStore = useBaseStore()
const userStore = useUserStore()
</script>

<script>
export default {
  mixins: [ToLocaleDateTimeString],
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
      isMessagesLoading: false,
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

      axios.get('/' + this.$i18n.locale + '/accounts/auth/wstoken/')
      .then((response) => {
        this.convoSocket = new WebSocket(
          this.baseStore.wsURL
          + '/ws/messenger/' + this.conversation.id
          + '/?' + response.data.wstoken
        )

        this.convoSocket.onopen = (event) => {
          this.isMessagesLoading = true
        }

        this.convoSocket.onmessage = (event) => {
          const data = JSON.parse(event.data)
          if (data.messages) {
            this.messages = data.messages
            this.isMessagesLoading = false
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
        this.errors = error.response.data
      })
    },
    sendMessage() {
      this.convoSocket.send(JSON.stringify({
        'msg_type': this.messageType.TEXT,
        'content': this.message
      }))
      this.message = ''
    },
    sendImages(event) {
      const imagesData = new FormData()
      imagesData.append('conversation', this.conversation.id)
      for (let i = 0; i < event.target.files.length; i++) {
        imagesData.append('content', event.target.files[i], event.target.files[i].name)
      }

      axios.post('/' + this.$i18n.locale + '/messenger/message/images/', imagesData)
      .then((response) => {
        this.convoSocket.send(JSON.stringify({
          'msg_type': 2,
          'msg_data': response.data
        }))
      })
    },
    sendFiles(event) {
      const filesData = new FormData()
      filesData.append('conversation', this.conversation.id)
      for (let i = 0; i < event.target.files.length; i++) {
        filesData.append('content', event.target.files[i], event.target.files[i].name)
      }

      axios.post('/' + this.$i18n.locale + '/messenger/message/files/', filesData)
      .then((response) => {
        this.convoSocket.send(JSON.stringify({
          'msg_type': 3,
          'msg_data': response.data
        }))
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
              <img
                v-if="conversation.details.image"
                :src="conversation.details.image"
                class="rounded-circle"
                width="50"
                height="50"
              >
              <img
                v-else
                src="/group-avatar.jpg"
                class="rounded-circle"
                width="50"
                height="50"
              >
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
        <div
          v-if="isMessagesLoading"
          class="text-center h-100"
        >
          <div
            class="spinner-grow text-dark"
            role="status"
          >
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
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
                {{ toLocaleDateTimeString(msg.created_at) }}
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
                  :src="`${ baseStore.apiURL }${ msg.sender.avatar }`"
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
                {{ toLocaleDateTimeString(msg.created_at) }}
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer bg-white">
        <div class="hstack gap-2">
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
          <div
            v-else
            class="dropup"
          >
            <button
              type="button"
              class="btn btn-light"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <i class="fa-solid fa-paper-plane"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <input
                ref="imagesInput"
                @change="sendImages"
                type="file"
                accept="image/*"
                multiple
                class="visually-hidden"
              >
              <li
                @click="$refs.imagesInput.click()"
                class="dropdown-item"
              >
                <i class="fa-solid fa-file-image"></i>
                Images
              </li>
              <input
                ref="filesInput"
                @change="sendFiles"
                type="file"
                multiple
                class="visually-hidden"
              >
              <li
                @click="$refs.filesInput.click()"
                class="dropdown-item"
              >
                <i class="fa-solid fa-file"></i>
                Files
              </li>
            </ul>
          </div>
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

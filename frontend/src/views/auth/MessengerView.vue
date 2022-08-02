<script setup>
import { nextTick } from 'vue'
import axios from 'axios'

import { useBaseStore } from '@/stores/base.js'
import { useUserStore } from '@/stores/user.js'
const baseStore = useBaseStore()
const userStore = useUserStore()
</script>

<script>
export default {
  data() {
    return {
      convoList: [],
      convoId: null,
      convoType: null,
      convoDetails: {},
      convoSocket: null,
      convoMessages: [],
      isMessagesLoading: false,
      message: '',
      status: null,
      errors: null
    }
  },
  methods: {
    closeConversation() {
      if (this.convoSocket) {
        this.convoSocket.close()
      }
    },
    openConversation(convo) {
      this.convoId = convo.id
      this.convoType = convo.convo_type
      this.convoDetails = convo.details
      this.closeConversation()

      axios.get('/' + this.$i18n.locale + '/accounts/auth/wstoken/')
      .then((response) => {
        this.convoSocket = new WebSocket(
          this.baseStore.wsURL
          + '/ws/messenger/' + convo.id
          + '/?' + response.data.wstoken
        )

        this.convoSocket.onopen = (event) => {
          this.isMessagesLoading = true
        }

        this.convoSocket.onmessage = (event) => {
          const data = JSON.parse(event.data)
          if (data.messages) {
            this.convoMessages = data.messages
            this.isMessagesLoading = false
            nextTick(() => {
              this.$refs.cardBody.scrollTop = this.$refs.cardBody.scrollHeight
              this.$refs.msgTextarea.focus()
            })
          } else {
            this.convoMessages.push(data)
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
          this.convoId = null
          this.convoType = null
          this.convoDetails = {}
          this.convoMessages = []
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
        'content': this.message
      }))
      this.message = ''
    },
    toLocaleDateTimeString(dateTimeString) {
      const dateTime = new Date(dateTimeString)
      const localeDateTime = dateTime.toLocaleTimeString(this.$i18n.locale, { timeStyle: 'short' })
        + " | " + dateTime.toLocaleDateString(this.$i18n.locale, { dateStyle: 'medium' })
      return localeDateTime
    }
  },
  watch: {
    message(newValue) {
      this.$refs.msgTextarea.rows = this.message.split('\n').length
    }
  },
  mounted() {
    axios.get('/' + this.$i18n.locale + '/messenger/conversations/')
    .then((response) => {
      this.convoList = response.data
      this.status = 'gotten_chats'
      this.errors = null
    })
    .catch((error) => {
      this.status = null
      this.errors = error.response.data
    })
  },
  unmounted() {
    this.closeConversation()
  }
}
</script>

<template>
  <div class="messenger container">
    <div class="row">
      <div class="col-lg-4 border-end py-4" style="min-height: 70vh;">

        <h4 class="mb-3">{{ $t('messenger.chats') }}</h4>

        <div class="list-group list-group-flush">
          <a v-for="convo in convoList" href="#" class="list-group-item list-group-item-action p-0">
            <div v-if="convo.id == convoId" class="d-flex gap-3 p-3 text-dark" style="background-color: #efefef;">
              <div v-if="convo.convo_type == 1">
                <img v-if="convo.details.avatar" :src="`${ convo.details.avatar }`" class="rounded-circle" width="48" height="48">
                <img v-else src="/user-avatar.jpg" class="rounded-circle" width="48" height="48">
              </div>
              <div v-else-if="convo.convo_type == 2">
                <img v-if="convo.details.image" :src="`${ convo.details.image }`" class="rounded-circle" width="48" height="48">
                <img v-else src="/group-avatar.jpg" class="rounded-circle" width="48" height="48">
              </div>
              <div v-else>
                <img src="/conversation.jpg" class="rounded-circle" width="48" height="48">
              </div>
              <div class="flex-grow-1 ms-3">
                <div class="d-flex justify-content-between">
                  <div v-if="convo.convo_type == 2" class="d-flex align-items-center">
                    <i class="fa-solid fa-user-group"></i>
                    &nbsp;
                    <strong class="mb-0">{{ convo.details.name }}</strong>
                  </div>
                  <strong v-else class="mb-0">{{ convo.details.name }}</strong>
                  <small>{{ toLocaleDateTimeString(convo.last_message.created_at) }}</small>
                </div>
                <p v-if="convo.last_message.msg_type == 1" class="mb-0 opacity-75">{{ convo.last_message.content }}</p>
                <p v-else-if="convo.last_message.msg_type == 2" class="mb-0 opacity-75">{{ convo.last_message.content.length }} Images</p>
                <p v-else-if="convo.last_message.msg_type == 3" class="mb-0 opacity-75">{{ convo.last_message.content.length }} Files</p>
              </div>
            </div>
            <div v-else @click="openConversation(convo)" class="d-flex gap-3 p-3">
              <div v-if="convo.convo_type == 1">
                <img v-if="convo.details.avatar" :src="`${ convo.details.avatar }`" class="rounded-circle" width="48" height="48">
                <img v-else src="/user-avatar.jpg" class="rounded-circle" width="48" height="48">
              </div>
              <div v-else-if="convo.convo_type == 2">
                <img v-if="convo.details.image" :src="`${ convo.details.image }`" class="rounded-circle" width="48" height="48">
                <img v-else src="/group-avatar.jpg" class="rounded-circle" width="48" height="48">
              </div>
              <div v-else>
                <img src="/conversation.jpg" class="rounded-circle" width="48" height="48">
              </div>
              <div class="flex-grow-1 ms-3">
                <div class="d-flex justify-content-between">
                  <div v-if="convo.convo_type == 2" class="d-flex align-items-center">
                    <i class="fa-solid fa-user-group"></i>
                    &nbsp;
                    <strong class="mb-0">{{ convo.details.name }}</strong>
                  </div>
                  <strong v-else class="mb-0">{{ convo.details.name }}</strong>
                  <small>{{ toLocaleDateTimeString(convo.last_message.created_at) }}</small>
                </div>
                <p v-if="convo.last_message.msg_type == 1" class="mb-0 opacity-75">{{ convo.last_message.content }}</p>
                <p v-else-if="convo.last_message.msg_type == 2" class="mb-0 opacity-75">{{ convo.last_message.content.length }} Images</p>
                <p v-else-if="convo.last_message.msg_type == 3" class="mb-0 opacity-75">{{ convo.last_message.content.length }} Files</p>
              </div>
            </div>
          </a>
        </div>

      </div>
      <div class="col-lg-8 pb-5 p-lg-3">
        <div v-if="convoId" class="card border-0">
          <div class="card-header bg-white">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div v-if="convoType == 1">
                  <img v-if="convoDetails.avatar" :src="`${ convoDetails.avatar }`" class="rounded-circle" width="50" height="50">
                  <img v-else src="/user-avatar.jpg" class="rounded-circle" width="50" height="50">
                </div>
                <div v-else-if="convoType == 2">
                  <img v-if="convoDetails.image" :src="`${ convoDetails.image }`" class="rounded-circle" width="50" height="50">
                  <img v-else src="/group-avatar.jpg" class="rounded-circle" width="50" height="50">
                </div>
                <div v-else>
                  <img src="/conversation.jpg" class="rounded-circle" width="50" height="50">
                </div>
              </div>
              <div class="flex-grow-1 ms-3">
                <strong>{{ this.convoDetails.name }}</strong>
              </div>
            </div>
          </div>
          <div ref="cardBody" class="card-body overflow-auto">
            <div v-if="isMessagesLoading" class="text-center h-100">
              <div class="spinner-grow text-dark" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else v-for="msg in convoMessages" class="mt-1">
              <div v-if="msg.sender.id == userStore.id" class="d-flex justify-content-end">
                <div class="my-0">
                  <div class="bg-primary rounded p-2 mb-2">
                    <p class="text-sm mb-0 text-white">{{ msg.content }}</p>
                  </div>
                  <p class="d-flex justify-content-end small text-muted">
                    {{ toLocaleDateTimeString(msg.created_at) }}
                  </p>
                </div>
              </div>
              <div v-else class="d-flex justify-content-start">
                <div class="my-0">
                  <div v-if="convoType == 2" class="d-flex align-items-start">
                    <img v-if="msg.sender.avatar" :src="`${ baseStore.apiURL }${ msg.sender.avatar }`" class="rounded-circle" width="35" height="35">
                    <img v-else src="/user-avatar.jpg" class="rounded-circle" width="35" height="35">
                    <div class="bg-light rounded p-2 ms-2 mb-2">
                      <p class="fw-bold mb-0">{{ msg.sender.name }}</p>
                      <p class="text-sm mb-0">{{ msg.content }}</p>
                    </div>
                  </div>
                  <div v-else class="bg-light rounded p-2 mb-2">
                    <p class="text-sm mb-0">{{ msg.content }}</p>
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
              <textarea ref="msgTextarea" v-model="message" class="form-control me-auto" :placeholder="$t('messenger.type_message')" rows="1"></textarea>
              <button v-if="message" @click="sendMessage" type="button" class="btn btn-primary">
                <i class="fa-solid fa-paper-plane"></i>
              </button>
              <div v-else class="dropup">
                <button type="button" class="btn btn-light" data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="fa-solid fa-paper-plane"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                  <li class="dropdown-item">
                    <i class="fa-solid fa-file-image"></i>
                    Images
                  </li>
                  <li class="dropdown-item">
                    <i class="fa-solid fa-file"></i>
                    Files
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center h-100">
          <div class="my-0">
            <i class="fa-solid fa-comments fa-2xl"></i>
            <p class="lead mt-3">{{ $t('messenger.select_chat') }}</p>
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

.mb-0.opacity-75 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-body {
  height: 60vh;
}
.text-sm.mb-0 {
  white-space: pre-line;
}
.text-center.h-100 {
  display: grid;
  place-items: center;
}

textarea {
  resize: none;
}
</style>

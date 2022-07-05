<script setup>
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
      chatList: [],
      chatId: null,
      chatSocket: null,
      chatUser: {},
      chatMessages: [],
      cardBody: null,
      status: null,
      errors: null
    }
  },
  methods: {
    openChat(chatId) {
      this.chatId = chatId

      if (this.chatSocket) {
        this.chatSocket.close(1000, 'unmounted')
      }

      const chat = this.chatList.find(obj => obj.id == chatId)
      this.chatUser = chat.members.find(obj => obj.id != this.userStore.id)

      axios.get('/' + this.$i18n.locale + '/accounts/auth/wstoken/')
      .then((response) => {
        this.chatSocket = new WebSocket(
          this.baseStore.wsURL
          + '/ws/messenger/' + this.chatId
          + '/?' + response.data.wstoken
        )

        this.chatSocket.onmessage = (e) => {
          const data = JSON.parse(e.data)
          if (data.messages) {
            this.chatMessages = data.messages
          } else {
            this.chatMessages.push(data)
          }
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
      const msgTextarea = this.$el.querySelector('#msg-textarea')

      this.chatSocket.send(JSON.stringify({
        'content': msgTextarea.value
      }))

      msgTextarea.value = ''
    },
    toLocaleDateTimeString(dateTimeString) {
      const dateTime = new Date(dateTimeString)
      const localeDateTime = dateTime.toLocaleTimeString(this.$i18n.locale, { timeStyle: 'short' })
        + " | " + dateTime.toLocaleDateString(this.$i18n.locale, { dateStyle: 'medium' })
      return localeDateTime
    }
  },
  mounted() {
    axios.get('/' + this.$i18n.locale + '/messenger/chats/')
    .then((response) => {
      this.chatList = response.data
      this.status = 'gotten_chats'
      this.errors = null
    })
    .catch((error) => {
      this.status = null
      this.errors = error.response.data
    })
  },
  unmounted() {
    if (this.chatSocket) {
      this.chatSocket.close(1000, 'unmounted')
    }
  }
}
</script>

<template>
  <div class="messenger container">
    <div class="row">
      <div class="col-lg-4 border-end py-5">

        <h4 class="mb-3">{{ $t('messenger.chats') }}</h4>

        <ul class="nav nav-pills flex-column">
          <li v-for="chat in chatList" class="nav-item">
            <a v-if="chat.id == chatId" class="nav-link active" aria-current="true" href="#">
              <div class="d-flex align-items-center">
                <div class="flex-shrink-0">
                  <div v-for="member in chat.members">
                    <div v-if="member.id != userStore.id" >
                      <img v-if="member.avatar" :src="`${ member.avatar }`" class="rounded-circle" width="50" height="50">
                      <img v-else src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                    </div>
                  </div>
                </div>
                <div class="flex-grow-1 ms-3">
                  <div class="d-flex w-100 justify-content-between">
                    <div v-for="member in chat.members">
                      <strong v-if="member.id != userStore.id" class="mb-1">{{ member.name }}</strong>
                    </div>
                    <small>{{ toLocaleDateTimeString(chat.last_message.created_at) }}</small>
                  </div>
                  <div class="my-1 small">{{ chat.last_message.content }}</div>
                </div>
              </div>
            </a>
            <a v-else @click="openChat(chat.id)" class="nav-link text-dark" href="#">
              <div class="d-flex align-items-center">
                <div class="flex-shrink-0">
                  <div v-for="member in chat.members">
                    <div v-if="member.id != userStore.id" >
                      <img v-if="member.avatar" :src="`${ member.avatar }`" class="rounded-circle" width="50" height="50">
                      <img v-else src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                    </div>
                  </div>
                </div>
                <div class="flex-grow-1 ms-3">
                  <div class="d-flex w-100 justify-content-between">
                    <div v-for="member in chat.members">
                      <strong v-if="member.id != userStore.id" class="mb-1">{{ member.name }}</strong>
                    </div>
                    <small>{{ toLocaleDateTimeString(chat.last_message.created_at) }}</small>
                  </div>
                  <div class="my-1 small">{{ chat.last_message.content }}</div>
                </div>
              </div>
            </a>
          </li>
        </ul>

      </div>
      <div class="col-lg-8 pb-5 p-lg-5">
        <div v-if="chatId" class="card border-0">
          <div class="card-header bg-white">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <img v-if="this.chatUser.avatar" :src="`${ this.chatUser.avatar }`" class="rounded-circle" width="50" height="50">
                <img v-else src="/avatar.jpg" class="rounded-circle" width="50" height="50">
              </div>
              <div class="flex-grow-1 ms-3">
                <strong>{{ this.chatUser.name }}</strong>
              </div>
            </div>
          </div>
          <div id="card-body" class="card-body overflow-auto">
            <div v-for="msg in chatMessages" class="mt-1">
              <div v-if="msg.sender == userStore.id" class="d-flex justify-content-end">
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
                  <div class="bg-light rounded p-2 mb-2">
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
            <div class="d-sm-flex align-items-end">
              <textarea id="msg-textarea" class="form-control" :placeholder="$t('messenger.type_message')" rows="1"></textarea>
              <button @click="sendMessage" type="button" class="btn btn-primary ms-2">{{ $t('messenger.send') }}</button>
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
  width: 0.4em;
  height: 0.4em;
  background-color: #f5f5f5;
}
::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 4em;
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
.text-center.h-100 {
  display: grid;
  place-items: center;
}
</style>

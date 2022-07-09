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
      convoList: [],
      convoId: null,
      convoType: null,
      convoDetails: {},
      convoSocket: null,
      convoMessages: [],
      // cardBody: null,
      status: null,
      errors: null
    }
  },
  methods: {
    openConversation(convo) {
      this.convoId = convo.id
      this.convoType = convo.convo_type
      this.convoDetails = convo.details

      if (this.convoSocket) {
        this.convoSocket.close(1000, 'unmounted')
      }

      axios.get('/' + this.$i18n.locale + '/accounts/auth/wstoken/')
      .then((response) => {
        this.convoSocket = new WebSocket(
          this.baseStore.wsURL
          + '/ws/messenger/' + this.convoId
          + '/?' + response.data.wstoken
        )

        this.convoSocket.onmessage = (e) => {
          const data = JSON.parse(e.data)
          if (data.messages) {
            this.convoMessages = data.messages
          } else {
            this.convoMessages.push(data)
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
      const msgTextarea = this.$el.querySelector('#msgTextarea')

      this.convoSocket.send(JSON.stringify({
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
    if (this.convoSocket) {
      this.convoSocket.close(1000, 'unmounted')
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
          <li v-for="convo in convoList" class="nav-item">
            <a v-if="convo.id == convoId" class="nav-link active" aria-current="true" href="#">
              <div class="d-flex align-items-center">
                <div class="flex-shrink-0">
                  <div v-if="convo.convo_type == 1">
                    <img v-if="convo.details.avatar" :src="`${ convo.details.avatar }`" class="rounded-circle" width="50" height="50">
                    <img v-else src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                  </div>
                  <div v-else-if="convo.convo_type == 2">
                    <img v-if="convo.details.image" :src="`${ convo.details.image }`" class="rounded-circle" width="50" height="50">
                    <img v-else src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                  </div>
                  <div v-else>
                    <img src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                  </div>
                </div>
                <div class="flex-grow-1 ms-3">
                  <div class="d-flex w-100 justify-content-between">
                    <div v-if="convo.convo_type == 2" class="d-flex align-items-center">
                      <i class="fa-solid fa-user-group"></i>
                      &nbsp;
                      <strong class="mb-1">{{ convo.details.name }}</strong>
                    </div>
                    <strong v-else class="mb-1">{{ convo.details.name }}</strong>
                    <small>{{ toLocaleDateTimeString(convo.last_message.created_at) }}</small>
                  </div>
                  <div class="my-1 small">{{ convo.last_message.content }}</div>
                </div>
              </div>
            </a>
            <a v-else @click="openConversation(convo)" class="nav-link text-dark" href="#">
              <div class="d-flex align-items-center">
                <div class="flex-shrink-0">
                  <div v-if="convo.convo_type == 1">
                    <img v-if="convo.details.avatar" :src="`${ convo.details.avatar }`" class="rounded-circle" width="50" height="50">
                    <img v-else src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                  </div>
                  <div v-else-if="convo.convo_type == 2">
                    <img v-if="convo.details.image" :src="`${ convo.details.image }`" class="rounded-circle" width="50" height="50">
                    <img v-else src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                  </div>
                  <div v-else>
                    <img src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                  </div>
                </div>
                <div class="flex-grow-1 ms-3">
                  <div class="d-flex w-100 justify-content-between">
                    <div v-if="convo.convo_type == 2" class="d-flex align-items-center">
                      <i class="fa-solid fa-user-group"></i>
                      &nbsp;
                      <strong class="mb-1">{{ convo.details.name }}</strong>
                    </div>
                    <strong v-else class="mb-1">{{ convo.details.name }}</strong>
                    <small>{{ toLocaleDateTimeString(convo.last_message.created_at) }}</small>
                  </div>
                  <div class="my-1 small">{{ convo.last_message.content }}</div>
                </div>
              </div>
            </a>
          </li>
        </ul>

      </div>
      <div class="col-lg-8 pb-5 p-lg-5">
        <div v-if="convoId" class="card border-0">
          <div class="card-header bg-white">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div v-if="convoType == 1">
                  <img v-if="convoDetails.avatar" :src="`${ convoDetails.avatar }`" class="rounded-circle" width="50" height="50">
                  <img v-else src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                </div>
                <div v-else-if="convoType == 2">
                  <img v-if="convoDetails.image" :src="`${ convoDetails.image }`" class="rounded-circle" width="50" height="50">
                  <img v-else src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                </div>
                <div v-else>
                  <img src="/avatar.jpg" class="rounded-circle" width="50" height="50">
                </div>
              </div>
              <div class="flex-grow-1 ms-3">
                <strong>{{ this.convoDetails.name }}</strong>
              </div>
            </div>
          </div>
          <div id="cardBody" class="card-body overflow-auto">
            <div v-for="msg in convoMessages" class="mt-1">
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
                    <img v-else src="/avatar.jpg" class="rounded-circle" width="35" height="35">
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
            <div class="d-sm-flex align-items-end">
              <textarea id="msgTextarea" class="form-control" :placeholder="$t('messenger.type_message')" rows="1"></textarea>
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
.text-center.h-100 {
  display: grid;
  place-items: center;
}
</style>

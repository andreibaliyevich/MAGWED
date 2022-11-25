<script setup>
import axios from 'axios'

import useLocaleDateTime from '@/composables/useLocaleDateTime.js'
const getLocaleDateTimeString = useLocaleDateTime()

import { useConnectionBusStore } from '@/stores/connectionBus.js'
const connectionBusStore = useConnectionBusStore()

import UserAvatar from '@/components/auth/UserAvatar.vue'
import GroupAvatar from '@/components/auth/GroupAvatar.vue'
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
    convoId: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      convoList: [],
      status: null,
      errors: null
    }
  },
  methods: {
    getConversations() {
      axios.get('/messenger/conversations/')
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
    updateUserStatus(mutation, state) {
      this.convoList.forEach((element) => {
        if (
          element.convo_type == this.conversationType.DIALOG &&
          element.details.id == state.user_id
        ) {
          element.details.online = state.online
        }
      })
    }
  },
  mounted() {
    this.getConversations()
    this.connectionBusStore.$subscribe(this.updateUserStatus)
  }
}
</script>

<template>
  <div class="conversation-list">
    <h4 class="mb-3">{{ $t('messenger.chats') }}</h4>

    <div class="list-group list-group-flush">
      <a
        v-for="convo in convoList"
        href="#"
        class="list-group-item list-group-item-action p-0"
      >
        <div
          v-if="convo.id == convoId"
          class="d-flex gap-3 p-3 text-dark"
          style="background-color: #efefef;"
        >
          <div v-if="convo.convo_type == conversationType.DIALOG">
            <UserAvatar
              :src="convo.details.avatar"
              :width="48"
              :height="48"
              :online="convo.details.online"
            />
          </div>
          <div v-else-if="convo.convo_type == conversationType.GROUP">
            <GroupAvatar
              :src="convo.details.image"
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
          <div class="flex-grow-1 ms-3">
            <div class="d-flex justify-content-between">
              <div
                v-if="convo.convo_type == conversationType.GROUP"
                class="d-flex align-items-center"
              >
                <i class="fa-solid fa-user-group"></i>
                &nbsp;
                <strong class="mb-0">{{ convo.details.name }}</strong>
              </div>
              <strong
                v-else
                class="mb-0"
              >
                {{ convo.details.name }}
              </strong>
              <small v-if="convo.last_message.created_at">
                {{ getLocaleDateTimeString($i18n.locale, convo.last_message.created_at) }}
              </small>
            </div>
            <p
              v-if="convo.last_message.msg_type == messageType.TEXT"
              class="mb-0 opacity-75"
            >
              {{ convo.last_message.content }}
            </p>
            <p
              v-else-if="convo.last_message.msg_type == messageType.IMAGES"
              class="mb-0 opacity-75"
            >
              {{ convo.last_message.content.length }} Images
            </p>
            <p
              v-else-if="convo.last_message.msg_type == messageType.FILES"
              class="mb-0 opacity-75"
            >
              {{ convo.last_message.content.length }} Files
            </p>
          </div>
        </div>
        <div
          v-else
          @click="$emit('setConversation', convo)"
          class="d-flex gap-3 p-3"
        >
          <div v-if="convo.convo_type == conversationType.DIALOG">
            <UserAvatar
              :src="convo.details.avatar"
              :width="48"
              :height="48"
              :online="convo.details.online"
            />
          </div>
          <div v-else-if="convo.convo_type == conversationType.GROUP">
            <GroupAvatar
              :src="convo.details.image"
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
          <div class="flex-grow-1 ms-3">
            <div class="d-flex justify-content-between">
              <div
                v-if="convo.convo_type == conversationType.GROUP"
                class="d-flex align-items-center"
              >
                <i class="fa-solid fa-user-group"></i>
                &nbsp;
                <strong class="mb-0">{{ convo.details.name }}</strong>
              </div>
              <strong
                v-else
                class="mb-0"
              >
                {{ convo.details.name }}
              </strong>
              <small v-if="convo.last_message.created_at">
                {{ getLocaleDateTimeString($i18n.locale, convo.last_message.created_at) }}
              </small>
            </div>
            <p
              v-if="convo.last_message.msg_type == messageType.TEXT"
              class="mb-0 opacity-75"
            >
              {{ convo.last_message.content }}
            </p>
            <p
              v-else-if="convo.last_message.msg_type == messageType.IMAGES"
              class="mb-0 opacity-75"
            >
              {{ convo.last_message.content.length }} Images
            </p>
            <p
              v-else-if="convo.last_message.msg_type == messageType.FILES"
              class="mb-0 opacity-75"
            >
              {{ convo.last_message.content.length }} Files
            </p>
          </div>
        </div>
      </a>
    </div>
  </div>
</template>

<style scoped>
.mb-0.opacity-75 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

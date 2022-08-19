<script setup>
import axios from 'axios'

import ToLocaleDateTimeString from '@/mixins/ToLocaleDateTimeString.js'
</script>

<script>
export default {
  mixins: [ToLocaleDateTimeString],
  props: {
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
  }
}
</script>

<template>
  <div class="conversation-list">
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
              <small v-if="convo.last_message.created_at">{{ toLocaleDateTimeString(convo.last_message.created_at) }}</small>
            </div>
            <p v-if="convo.last_message.msg_type == 1" class="mb-0 opacity-75">{{ convo.last_message.content }}</p>
            <p v-else-if="convo.last_message.msg_type == 2" class="mb-0 opacity-75">{{ convo.last_message.content.length }} Images</p>
            <p v-else-if="convo.last_message.msg_type == 3" class="mb-0 opacity-75">{{ convo.last_message.content.length }} Files</p>
          </div>
        </div>
        <div v-else @click="$emit('setConversation', convo)" class="d-flex gap-3 p-3">
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
              <small v-if="convo.last_message.created_at">{{ toLocaleDateTimeString(convo.last_message.created_at) }}</small>
            </div>
            <p v-if="convo.last_message.msg_type == 1" class="mb-0 opacity-75">{{ convo.last_message.content }}</p>
            <p v-else-if="convo.last_message.msg_type == 2" class="mb-0 opacity-75">{{ convo.last_message.content.length }} Images</p>
            <p v-else-if="convo.last_message.msg_type == 3" class="mb-0 opacity-75">{{ convo.last_message.content.length }} Files</p>
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

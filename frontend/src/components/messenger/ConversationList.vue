<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { conversationType, messageType } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'

const { getLocaleDateTimeString } = useLocaleDateTime()
const connectionBusStore = useConnectionBusStore()

const props = defineProps({
  convoId: {
    type: Number,
    default: 0
  }
})

const convoLoading = ref(true)
const convoList = ref([])

const getConversations = async () => {
  try {
    const response = await axios.get('/messenger/conversations/')
    convoList.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    convoLoading.value = false
  }
}

const updateUserStatus = (mutation, state) => {
  convoList.value.forEach((element) => {
    if (
      element.convo_type == conversationType.DIALOG &&
      element.details.id == state.user_id
    ) {
      element.details.online = state.online
    }
  })
}

onMounted(() => {
  getConversations()
  connectionBusStore.$subscribe(updateUserStatus)
})
</script>

<template>
  <div class="conversation-list">
    <h4 class="mb-3">{{ $t('messenger.chats') }}</h4>

    <LoadingIndicator v-if="convoLoading" />
    <div
      v-else
      class="list-group list-group-flush"
    >
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
            <div class="position-relative">
              <UserAvatar
                :src="convo.details.avatar"
                :width="48"
                :height="48"
              />
              <span
                v-if="convo.details.online"
                class="position-absolute top-0 start-100 translate-middle p-1 bg-primary rounded-circle"
              >
                <span class="visually-hidden">Online</span>
              </span>
            </div>
          </div>
          <div v-else-if="convo.convo_type == conversationType.GROUP">
            <img
              v-if="convo.details.image"
              :src="convo.details.image"
              width="48"
              height="48"
              class="rounded-circle"
            >
            <img
              v-else
              src="/group-avatar.jpg"
              width="48"
              height="48"
              class="rounded-circle"
            >
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
                {{ getLocaleDateTimeString(convo.last_message.created_at) }}
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
            <div class="position-relative">
              <UserAvatar
                :src="convo.details.avatar"
                :width="48"
                :height="48"
              />
              <span
                v-if="convo.details.online"
                class="position-absolute top-0 start-100 translate-middle p-1 bg-primary rounded-circle"
              >
                <span class="visually-hidden">Online</span>
              </span>
            </div>
          </div>
          <div v-else-if="convo.convo_type == conversationType.GROUP">
            <img
              v-if="convo.details.image"
              :src="convo.details.image"
              width="48"
              height="48"
              class="rounded-circle"
            >
            <img
              v-else
              src="/group-avatar.jpg"
              width="48"
              height="48"
              class="rounded-circle"
            >
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
                {{ getLocaleDateTimeString(convo.last_message.created_at) }}
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
strong,
small,
.mb-0.opacity-75 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

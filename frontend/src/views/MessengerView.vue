<script setup>
import { ref } from 'vue'
import ConversationList from '@/components/messenger/ConversationList.vue'
import ConversationDetail from '@/components/messenger/ConversationDetail.vue'

const conversation = ref({})

const setConversation = (convo) => {
  conversation.value = convo
}
</script>

<template>
  <div class="messenger-view">
    <div class="container">
      <div class="row d-lg-none">
        <div
          v-if="!conversation.uuid"
          class="col py-4"
        >
          <ConversationList @setConversation="setConversation" />
        </div>
        <div
          v-else
          class="col pt-1 pb-4"
        >
          <button
            @click="conversation = {}"
            class="btn btn-light w-100"
            type="button"
          >
            <i class="fa-solid fa-arrow-left-long"></i>
          </button>
          <ConversationDetail :conversation="conversation" />
        </div>
      </div>

      <div class="row d-none d-lg-flex">
        <div class="col-4 border-end py-4">
          <ConversationList
            :convoUuid="conversation.uuid"
            @setConversation="setConversation"
          />
        </div>
        <div class="col-8 p-3">
          <ConversationDetail
            v-if="conversation.uuid" 
            :conversation="conversation"
          />
          <div
            v-else
            class="text-center h-100"
            style="min-height: 60vh;"
          >
            <div class="my-0">
              <i class="fa-solid fa-comments fa-2xl"></i>
              <p class="lead mt-3">{{ $t('messenger.select_chat') }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-center.h-100 {
  display: grid;
  place-items: center;
}
</style>

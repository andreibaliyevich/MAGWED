<script setup>
import ConversationList from '@/components/messenger/ConversationList.vue'
import ConversationDetail from '@/components/messenger/ConversationDetail.vue'
</script>

<script>
export default {
  data() {
    return {
      conversationType: {
        DIALOG: 1,
        GROUP: 2
      },
      messageType: {
        TEXT: 1,
        IMAGES: 2,
        FILES: 3
      },
      conversation: {}
    }
  },
  methods: {
    setConversation(convo) {
      this.conversation = convo
    }
  }
}
</script>

<template>
  <div class="messenger container">
    <div class="row d-lg-none">
      <div
        v-if="!conversation.id"
        class="col py-4"
      >
        <ConversationList
          :conversationType="conversationType"
          :messageType="messageType"
          @setConversation="setConversation"
        />
      </div>
      <div
        v-else
        class="col pt-1 pb-4"
      >
        <button
          @click="conversation = {}"
          type="button"
          class="btn btn-light w-100"
        >
          <i class="fa-solid fa-arrow-left-long"></i>
        </button>
        <ConversationDetail
          :conversationType="conversationType"
          :messageType="messageType"
          :conversation="conversation"
        />
      </div>
    </div>
    <div class="row d-none d-lg-flex">
      <div class="col-4 border-end py-4">
        <ConversationList
          :conversationType="conversationType"
          :messageType="messageType"
          :convoId="conversation.id"
          @setConversation="setConversation"
        />
      </div>
      <div class="col-8 p-3">
        <ConversationDetail
          v-if="conversation.id" 
          :conversationType="conversationType"
          :messageType="messageType"
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
</template>

<style scoped>
.text-center.h-100 {
  display: grid;
  place-items: center;
}
</style>

<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useSendComment } from '@/composables/sendComment.js'
import SubmitContent from './SubmitContent.vue'
import ReportDropdownItemModal from '../ReportDropdownItemModal.vue'

const userStore = useUserStore()

const props = defineProps({
  commentItem: {
    type: Object,
    required: true
  }
})

const replyComment = ref(false)
const {
  newCommentSending,
  newCommentContent,
  newCommentErrors,
  sendComment
} = useSendComment('comment', props.commentItem.uuid)

const { getLocaleDateTimeString } = useLocaleDateTime()

watch(newCommentContent, (newValue) => {
  if (!newValue) {
    replyComment.value = false
  }
})
</script>

<template>
  <div class="comment-item">
    <div class="d-flex gap-3">
      <router-link
        v-if="commentItem.author.profile_url"
        :to="{
          name: 'OrganizerDetail',
          params: { profile_url: commentItem.author.profile_url }
        }"
      >
        <UserAvatarExtended
          :src="commentItem.author.avatar"
          :width="32"
          :height="32"
          :online="commentItem.author.status === 'online' ? true : false"
        />
      </router-link>
      <UserAvatarExtended
        v-else
        :src="commentItem.author.avatar"
        :width="32"
        :height="32"
        :online="commentItem.author.status === 'online' ? true : false"
      />
      <div class="flex-grow-1 ms-1">
        <div class="d-flex justify-content-between">
          <router-link
            v-if="commentItem.author.profile_url"
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: commentItem.author.profile_url }
            }"
            class="text-decoration-none link-dark"
          >
            <strong class="mb-0">
              {{ commentItem.author.name }}
            </strong>
          </router-link>
          <strong
            v-else
            class="mb-0"
          >
            {{ commentItem.author.name }}
          </strong>
          <small class="text-secondary">
            {{ getLocaleDateTimeString(commentItem.created_at) }}
          </small>
        </div>
        <div class="d-flex justify-content-between">
          <div class="text-pre-line">{{ commentItem.content }}</div>
          <div class="d-flex justify-content-end">
            <div class="dropdown">
              <button
                type="button"
                class="btn btn-link link-dark"
                data-bs-toggle="dropdown"
                data-bs-auto-close="true"
                aria-expanded="false"
              >
                <i class="fa-solid fa-ellipsis"></i>
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li v-if="userStore.isLoggedIn">
                  <button
                    @click="replyComment = true"
                    type="button"
                    class="dropdown-item btn btn-link"
                  >
                    <i class="fa-solid fa-reply"></i>
                    {{ $t('btn.reply') }}
                  </button>
                </li>
                <li>
                  <ReportDropdownItemModal
                    contentType="comment"
                    :objectUUID="commentItem.uuid"
                  />
                </li>
              </ul>
            </div>
          </div>
        </div>
        <form
          v-if="replyComment"
          @submit.prevent="sendComment()"
        >
          <SubmitContent
            v-model="newCommentContent"
            :loadingStatus="newCommentSending"
            :autofocus="true"
            :id="`id_new_content_${commentItem.uuid}`"
            :placeholder="$t('comments.add_comment')"
            :errors="newCommentErrors?.content ? newCommentErrors.content : []"
          />
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-pre-line {
  white-space: pre-line;
}
</style>

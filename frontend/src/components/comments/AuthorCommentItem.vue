<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useSendComment } from '@/composables/sendComment.js'
import SubmitContent from './SubmitContent.vue'
import ReportDropdownItemModal from '../ReportDropdownItemModal.vue'

const props = defineProps({
  commentItem: {
    type: Object,
    required: true
  }
})

const oldCommentUpdating = ref(false)
const oldCommentContent = ref('')
const oldCommentErrors = ref(null)

const replyComment = ref(false)
const {
  newCommentSending,
  newCommentContent,
  newCommentErrors,
  sendComment
} = useSendComment('comment', props.commentItem.uuid)

const { getLocaleDateTimeString } = useLocaleDateTime()

const updateCommentModal = ref(null)
const updateCommentModalBootstrap = ref(null)

const updateComment = async () => {
  oldCommentUpdating.value = true
  try {
    const response = await axios.put(
      '/comments/'
        + props.commentItem.uuid
        +'/',
      { content: oldCommentContent.value }
    )
    updateCommentModalBootstrap.value.hide()
  } catch (error) {
    oldCommentErrors.value = error.response.data
  } finally {
    oldCommentUpdating.value = false
  }
}

const removeComment = async () => {
  try {
    const response = axios.delete(
      '/comments/'
        + props.commentItem.uuid
        +'/'
    )
  } catch (error) {
    console.error(error)
  }
}

watch(newCommentContent, (newValue) => {
  if (!newValue) {
    replyComment.value = false
  }
})

onMounted(() => {
  updateCommentModalBootstrap.value = new bootstrap.Modal(
    updateCommentModal.value
  )
  updateCommentModal.value.addEventListener('hidden.bs.modal', () => {
    oldCommentContent.value = ''
    oldCommentErrors.value = null
  })
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
                <li>
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
                <li>
                  <button
                    @click="oldCommentContent = commentItem.content"
                    type="button"
                    class="dropdown-item btn btn-link"
                    data-bs-toggle="modal"
                    :data-bs-target="`#update_comment_modal_${commentItem.uuid}`"
                  >
                    <i class="fa-solid fa-pen"></i>
                    {{ $t('btn.edit') }}
                  </button>
                </li>
                <li>
                  <button
                    type="button"
                    class="dropdown-item btn btn-link"
                    data-bs-toggle="modal"
                    :data-bs-target="`#remove_comment_modal_choice_${commentItem.uuid}`"
                  >
                    <i class="fa-solid fa-trash"></i>
                    {{ $t('btn.delete') }}
                  </button>
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

    <Teleport to="body">
      <div
        ref="updateCommentModal"
        :id="`update_comment_modal_${commentItem.uuid}`"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        :aria-labelledby="`update_comment_modal_label_${commentItem.uuid}`"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                :id="`update_comment_modal_label_${commentItem.uuid}`"
                class="modal-title"
              >
                {{ $t('comments.updating_comment') }}
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form
                @submit.prevent="updateComment()"
                :id="`review_modal_form_${commentItem.uuid}`"
              >
                <BaseTextarea
                  v-model="oldCommentContent"
                  :id="`id_old_comment_${commentItem.uuid}`"
                  name="comment"
                  :label="$t('comments.content')"
                  :errors="
                    oldCommentErrors?.content
                    ? oldCommentErrors.content
                    : []
                  "
                />
              </form>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-light"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.cancel') }}
              </button>
              <SubmitButton
                :loadingStatus="oldCommentUpdating"
                buttonClass="btn btn-brand"
                :form="`review_modal_form_${commentItem.uuid}`"
                :disabled="!oldCommentContent"
              >
                {{ $t('btn.update') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>

      <div
        :id="`remove_comment_modal_choice_${commentItem.uuid}`"
        class="modal fade"
        role="dialog"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div
          class="modal-dialog modal-dialog-centered"
          role="document"
        >
          <div class="modal-content rounded-3 shadow">
            <div class="modal-body p-4 text-center">
              <h5 class="mb-0">{{ $t('comments.you_want_remove_comment') }}</h5>
              <p class="mb-0">{{ $t('comments.you_can_update_this_comment') }}</p>
            </div>
            <div class="modal-footer flex-nowrap p-0">
              <button
                @click="removeComment()"
                type="button"
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0 border-end"
                data-bs-dismiss="modal"
              >
                <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
              </button>
              <button
                type="button"
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.no_cancel') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.text-pre-line {
  white-space: pre-line;
}
</style>

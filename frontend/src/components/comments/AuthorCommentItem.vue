<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useSendComment } from '@/composables/sendComment.js'
import SubmitContent from './SubmitContent.vue'

const props = defineProps({
  commentItem: {
    type: Object,
    required: true
  }
})

const { getLocaleDateTimeString } = useLocaleDateTime()

const replyComment = ref(false)

const {
  newCommentSending,
  newCommentContent,
  newCommentErrors,
  sendComment
} = useSendComment('comment', props.commentItem.uuid)

const oldCommentUpdating = ref(false)
const oldCommentContent = ref('')

const oldCommentErrors = ref(null)

const commentDropdown = ref(null)
const commentDropdownBootstrap = ref(null)

const updateCommentModal = ref(null)
const updateCommentModalBootstrap = ref(null)
const removeCommentModalChoice = ref(null)

const updateComment = async () => {
  oldCommentUpdating.value = true
  try {
    const response = await axios.put(
      '/comments/'
        + props.commentItem.uuid
        +'/',
      { content: oldCommentContent.value }
    )
    oldCommentErrors.value = null
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
  commentDropdownBootstrap.value = new bootstrap.Dropdown(
    commentDropdown.value
  )
  updateCommentModalBootstrap.value = new bootstrap.Modal(
    updateCommentModal.value
  )
  updateCommentModal.value.addEventListener('hidden.bs.modal', () => {
    oldCommentContent.value = ''
  })
  removeCommentModalChoice.value.addEventListener('hidden.bs.modal', () => {
  })
})
</script>

<template>
  <div class="comment-item">
    <div class="d-flex gap-3">
      <LocaleRouterLink
        v-if="commentItem.author.profile_url"
        routeName="OrganizerDetail"
        :routeParams="{ profile_url: commentItem.author.profile_url }"
      >
        <UserAvatarExtended
          :src="commentItem.author.avatar"
          :width="32"
          :height="32"
          :online="commentItem.author.online"
        />
      </LocaleRouterLink>
      <UserAvatarExtended
        v-else
        :src="commentItem.author.avatar"
        :width="32"
        :height="32"
        :online="commentItem.author.online"
      />
      <div class="flex-grow-1 ms-1">
        <div class="d-flex justify-content-between">
          <LocaleRouterLink
            v-if="commentItem.author.profile_url"
            routeName="OrganizerDetail"
            :routeParams="{ profile_url: commentItem.author.profile_url }"
            class="text-decoration-none link-dark"
          >
            <strong class="mb-0">
              {{ commentItem.author.name }}
            </strong>
          </LocaleRouterLink>
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
                ref="commentDropdown"
                type="button"
                class="btn btn-link link-dark"
                data-bs-toggle="dropdown"
                data-bs-auto-close="outside"
                aria-expanded="false"
              >
                <i class="fa-solid fa-ellipsis"></i>
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li>
                  <button
                    @click="() => {
                      commentDropdownBootstrap.hide()
                      replyComment = true
                    }"
                    type="button"
                    class="dropdown-item btn btn-link"
                  >
                    <i class="fa-solid fa-reply"></i>
                    {{ $t('btn.reply') }}
                  </button>
                </li>
                <li>
                  <button
                    type="button"
                    class="dropdown-item btn btn-link"
                  >
                    <i class="fa-solid fa-flag"></i>
                    {{ $t('btn.report') }}
                  </button>
                </li>
                <li>
                  <button
                    @click="() => {
                      commentDropdownBootstrap.hide()
                      oldCommentContent = commentItem.content
                    }"
                    type="button"
                    class="dropdown-item btn btn-link"
                    data-bs-toggle="modal"
                    :data-bs-target="`#updateCommentModal_${commentItem.uuid}`"
                  >
                    <i class="fa-solid fa-pen"></i>
                    {{ $t('btn.edit') }}
                  </button>
                </li>
                <li>
                  <button
                    @click="commentDropdownBootstrap.hide()"
                    type="button"
                    class="dropdown-item btn btn-link"
                    data-bs-toggle="modal"
                    :data-bs-target="`#removeCommentModalChoice_${commentItem.uuid}`"
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
        :id="`updateCommentModal_${commentItem.uuid}`"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="updateCommentModalLabel"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="updateCommentModalLabel"
                class="modal-title"
              >
                {{ $t('comments.updating_comment') }}
              </h5>
              <button
                class="btn-close"
                type="button"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form
                @submit.prevent="updateComment()"
                :id="`reviewModalForm_${commentItem.uuid}`"
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
                class="btn btn-light"
                type="button"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.cancel') }}
              </button>
              <SubmitButton
                :loadingStatus="oldCommentUpdating"
                buttonClass="btn btn-brand"
                :form="`reviewModalForm_${commentItem.uuid}`"
                :disabled="!oldCommentContent"
              >
                {{ $t('btn.update') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>

      <div
        ref="removeCommentModalChoice"
        :id="`removeCommentModalChoice_${commentItem.uuid}`"
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
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0 border-end"
                type="button"
                data-bs-dismiss="modal"
              >
                <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
              </button>
              <button
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0"
                type="button"
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

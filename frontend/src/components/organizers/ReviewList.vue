<script setup>
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { ref, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import ReportDropdownItemModal from '../ReportDropdownItemModal.vue'

const { t, locale } = useI18n({ useScope: 'global' })
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const props = defineProps({
  userUUID: {
    type: String,
    required: true
  }
})

const reviewListLoading = ref(true)
const reviewList = ref([])
const nextURL = ref(null)

const newReviewSending = ref(false)
const newReviewRating = ref(null)
const newReviewComment = ref('')

const oldReviewUpdating = ref(false)
const oldReviewUuid = ref(null)
const oldReviewRating = ref(null)
const oldReviewComment = ref('')

const reviewRatingOptions = ref([])

const { getLocaleDateTimeString } = useLocaleDateTime()

const newReviewErrors = ref(null)
const oldReviewErrors = ref(null)

const updateReviewModal = ref(null)
const updateReviewModalBootstrap = ref(null)
const removeReviewModalChoice = ref(null)

const getReviewList = async () => {
  try {
    const response = await axios.get('/reviews/', {
      params: {
        user: props.userUUID
      }
    })
    reviewList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    reviewListLoading.value = false
  }
}

const getMoreReviewList = async () => {
  reviewListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    reviewList.value = [...reviewList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    reviewListLoading.value = false
  }
}

const setReviewRatingOptions = () => {
  reviewRatingOptions.value = [
    { value: '5', text: t('reviews.rating_options', { n: 5 }) },
    { value: '4', text: t('reviews.rating_options', { n: 4 }) },
    { value: '3', text: t('reviews.rating_options', { n: 3 }) },
    { value: '2', text: t('reviews.rating_options', { n: 2 }) },
    { value: '1', text: t('reviews.rating_options', { n: 1 }) }
  ]
}

const sendReview = async () => {
  newReviewSending.value = true
  try {
    const response = await axios.post('/reviews/', {
      user: props.userUUID,
      rating: newReviewRating.value,
      comment: newReviewComment.value
    })
    reviewList.value.unshift(response.data)
    newReviewRating.value = null
    newReviewComment.value = ''
    newReviewErrors.value = null
  } catch (error) {
    newReviewErrors.value = error.response.data
  } finally {
    newReviewSending.value = false
  }
}

const updateReview = async () => {
  oldReviewUpdating.value = true
  try {
    const response = await axios.put(
      '/reviews/'
        + oldReviewUuid.value
        +'/',
      {
        rating: oldReviewRating.value,
        comment: oldReviewComment.value
      }
    )
    const foundIndex = reviewList.value.findIndex((element) => {
      return element.uuid === oldReviewUuid.value
    })
    reviewList.value[foundIndex].rating = response.data.rating
    reviewList.value[foundIndex].comment = response.data.comment
    updateReviewModalBootstrap.value.hide()
  } catch (error) {
    oldReviewErrors.value = error.response.data
  } finally {
    oldReviewUpdating.value = false
  }
}

const removeReview = async () => {
  try {
    const response = axios.delete('/reviews/' + oldReviewUuid.value +'/')
    reviewList.value = reviewList.value.filter((element) => {
      return element.uuid !== oldReviewUuid.value
    })
  } catch (error) {
    console.error(error)
  }
}

const updateUserStatus = (mutation, state) => {
  reviewList.value.forEach((element) => {
    if (element.author.uuid === state.user_uuid) {
      element.author.status = state.status
    }
  })
}

watch(locale, () => {
  setReviewRatingOptions()
})

onMounted(() => {
  getReviewList()
  setReviewRatingOptions()
  connectionBusStore.$subscribe(updateUserStatus)
  updateReviewModal.value.addEventListener('hidden.bs.modal', () => {
    oldReviewUuid.value = null
    oldReviewRating.value = null
    oldReviewComment.value = ''
    oldReviewErrors.value = null
  })
  updateReviewModalBootstrap.value = new bootstrap.Modal(
    updateReviewModal.value
  )
  removeReviewModalChoice.value.addEventListener('hidden.bs.modal', () => {
    oldReviewUuid.value = null
  })
})
</script>

<template>
  <div class="review-list">
    <div class="row flex-lg-row-reverse g-5 mt-3">
      <div class="col-lg-6">
        <div
          v-if="userStore.isLoggedIn"
          class="card border border-light shadow-sm"
        >
          <div class="card-body m-sm-3 m-md-4">
            <h5 class="card-title">{{ $t('reviews.write_review') }}</h5>
            <form
              @submit.prevent="sendReview()"
              class="row g-3 mt-3"
            >
              <div class="col-12">
                <BaseSelect
                  v-model="newReviewRating"
                  :options="reviewRatingOptions"
                  id="id_new_rating"
                  name="rating"
                  :label="$t('reviews.rating')"
                  :errors="
                    newReviewErrors?.rating
                    ? newReviewErrors.rating
                    : []
                  "
                />
              </div>
              <div class="col-12">
                <BaseTextarea
                  v-model="newReviewComment"
                  id="id_new_comment"
                  name="comment"
                  :label="$t('reviews.comment')"
                  :errors="
                    newReviewErrors?.comment
                    ? newReviewErrors.comment
                    : []
                  "
                />
              </div>
              <div class="col-12">
                <SubmitButton
                  :loadingStatus="newReviewSending"
                  buttonClass="btn btn-brand"
                  :disabled="!newReviewRating || !newReviewComment"
                >
                  {{ $t('btn.send') }}
                </SubmitButton>
                <small
                  v-if="newReviewErrors?.create"
                  class="text-danger"
                >
                  {{ newReviewErrors.create }}
                </small>
              </div>
            </form>
          </div>
        </div>
        <div
          v-else
          class="alert alert-info" role="alert"
        >
          {{ $t('reviews.need_log_in') }}
          <router-link
            :to="{
              name: 'Login',
              query: { redirect: $route.path }
            }"
            class="alert-link"
          >
            {{ $t('auth.log_in') }}
          </router-link>
        </div>
      </div>
      <div class="col-lg-6">
        <div v-if="reviewList.length > 0">
          <TransitionGroup
            tag="ul"
            name="list-group"
            class="list-group list-group-flush"
          >
            <li
              v-for="reviewItem in reviewList"
              :key="reviewItem.uuid"
              class="list-group-item"
            >
              <div
                v-if="reviewItem.author"
                class="d-flex gap-3 py-3"
              >
                <router-link
                  v-if="reviewItem.author.profile_url"
                  :to="{
                    name: 'OrganizerDetail',
                    params: { profile_url: reviewItem.author.profile_url }
                  }"
                >
                  <UserAvatarExtended
                    :src="reviewItem.author.avatar"
                    :width="48"
                    :height="48"
                    :online="reviewItem.author.status === 'online' ? true : false"
                  />
                </router-link>
                <UserAvatarExtended
                  v-else
                  :src="reviewItem.author.avatar"
                  :width="48"
                  :height="48"
                  :online="reviewItem.author.status === 'online' ? true : false"
                />
                <div class="flex-grow-1 ms-1">
                  <div class="d-flex justify-content-between">
                    <router-link
                      v-if="reviewItem.author.profile_url"
                      :to="{
                        name: 'OrganizerDetail',
                        params: { profile_url: reviewItem.author.profile_url }
                      }"
                      class="text-decoration-none link-dark"
                    >
                      <strong class="mb-0">
                        {{ reviewItem.author.name }}
                      </strong>
                    </router-link>
                    <strong
                      v-else
                      class="mb-0"
                    >
                      {{ reviewItem.author.name }}
                    </strong>
                    <small class="text-secondary">
                      {{ getLocaleDateTimeString(reviewItem.created_at) }}
                    </small>
                  </div>
                  <div v-if="reviewItem.rating === 1">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                  </div>
                  <div v-else-if="reviewItem.rating === 2">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                  </div>
                  <div v-else-if="reviewItem.rating === 3">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                  </div>
                  <div v-else-if="reviewItem.rating === 4">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                  </div>
                  <div v-else-if="reviewItem.rating === 5">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                  </div>
                </div>
              </div>
              <p>{{ reviewItem.comment }}</p>
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
                      <ReportDropdownItemModal
                        contentType="review"
                        :objectUUID="reviewItem.uuid"
                      />
                    </li>
                    <li v-if="userStore.uuid === reviewItem.author.uuid">
                      <button
                        @click="() => {
                          oldReviewUuid = reviewItem.uuid
                          oldReviewRating = reviewItem.rating
                          oldReviewComment = reviewItem.comment
                        }"
                        type="button"
                        class="dropdown-item btn btn-link"
                        data-bs-toggle="modal"
                        data-bs-target="#update_review_modal"
                      >
                        <i class="fa-solid fa-pen"></i>
                        {{ $t('btn.edit') }}
                      </button>
                    </li>
                    <li v-if="userStore.uuid === reviewItem.author.uuid">
                      <button
                        @click="oldReviewUuid = reviewItem.uuid"
                        type="button"
                        class="dropdown-item btn btn-link"
                        data-bs-toggle="modal"
                        data-bs-target="#remove_review_modal_choice"
                      >
                        <i class="fa-solid fa-trash"></i>
                        {{ $t('btn.delete') }}
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
            </li>
          </TransitionGroup>
        </div>
        <div
          v-else-if="!reviewListLoading"
          class="lead d-flex justify-content-center py-3"
        >
          {{ $t('reviews.no_reviews_yet') }}
        </div>
        <div
          v-if="nextURL"
          style="min-height: 1px; margin-bottom: 1px;"
          v-intersection="{
            'scrollArea': null,
            'callbackFunction': getMoreReviewList,
            'functionArguments': []
          }"
        ></div>
        <LoadingIndicator v-if="reviewListLoading" />
      </div>
    </div>

    <Teleport to="body">
      <div
        ref="updateReviewModal"
        id="update_review_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="update_review_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="update_review_modal_label"
                class="modal-title"
              >
                {{ $t('reviews.updating_review') }}
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
                @submit.prevent="updateReview()"
                id="reviewModalForm"
                class="row g-3"
              >
                <div class="col-md-12">
                  <BaseSelect
                    v-model="oldReviewRating"
                    :options="reviewRatingOptions"
                    id="id_old_rating"
                    name="rating"
                    :label="$t('reviews.rating')"
                    :errors="
                      oldReviewErrors?.rating
                      ? oldReviewErrors.rating
                      : []
                    "
                  />
                </div>
                <div class="col-md-12">
                  <BaseTextarea
                    v-model="oldReviewComment"
                    id="id_old_comment"
                    name="comment"
                    :label="$t('reviews.comment')"
                    :errors="
                      oldReviewErrors?.comment
                      ? oldReviewErrors.comment
                      : []
                    "
                  />
                </div>
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
                :loadingStatus="oldReviewUpdating"
                buttonClass="btn btn-brand"
                form="reviewModalForm"
                :disabled="!oldReviewRating || !oldReviewComment"
              >
                {{ $t('btn.update') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>

      <div
        ref="removeReviewModalChoice"
        id="remove_review_modal_choice"
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
              <h5 class="mb-0">{{ $t('reviews.you_want_remove_review') }}</h5>
              <p class="mb-0">{{ $t('reviews.organizer_rating_will_be_updated') }}</p>
            </div>
            <div class="modal-footer flex-nowrap p-0">
              <button
                @click="removeReview()"
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
.list-group-enter-active,
.list-group-leave-active {
  transition: all 0.5s;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
}
.list-group-enter-from,
.list-group-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style>

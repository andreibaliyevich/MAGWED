<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useUserStore } from '@/stores/user.js'
import WriteReview from '@/components/organizers/WriteReview.vue'

const userStore = useUserStore()

const props = defineProps({
  userUUID: {
    type: String,
    required: true
  }
})

const reviewLoading = ref(true)
const reviewMoreLoading = ref(false)
const reviewList = ref([])
const nextURL = ref(null)

const { getLocaleDateTimeString } = useLocaleDateTime()

const getOrganizerReviews = async () => {
  try {
    const response = await axios.get(
      '/social/reviews/'
        + '?user='
        + props.userUUID
    )
    reviewList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    reviewLoading.value = false
  }
}

const getMoreOrganizerReviews = async () => {
  reviewMoreLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    reviewList.value = [...reviewList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    reviewMoreLoading.value = false
  }
}

onMounted(() => {
  getOrganizerReviews()
})
</script>

<template>
  <div class="review-list">
    <div class="row flex-lg-row-reverse g-5 mt-3">
      <div class="col-lg-6">
        <WriteReview
          v-if="userStore.isLoggedIn"
          :userUUID="props.userUUID"
          @reviewCreated="(review) => reviewList.unshift(review)"
        />
        <div
          v-else
          class="alert alert-info" role="alert"
        >
          {{ $t('organizers.need_log_in') }}
          <LocaleRouterLink
            routeName="Login"
            :routeQuery="{ redirect: this.$route.path }"
            class="alert-link"
          >
            {{ $t('auth.log_in') }}
          </LocaleRouterLink>
        </div>
      </div>
      <div class="col-lg-6">
        <LoadingIndicator v-if="reviewLoading" />
        <div v-else-if="reviewList.length > 0">
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
                <LocaleRouterLink
                  v-if="reviewItem.author.profile_url"
                  routeName="OrganizerDetail"
                  :routeParams="{ profile_url: reviewItem.author.profile_url }"
                >
                  <UserAvatarExtended
                    :src="reviewItem.author.avatar"
                    :width="48"
                    :height="48"
                    :online="reviewItem.author.online"
                  />
                </LocaleRouterLink>
                <UserAvatarExtended
                  v-else
                  :src="reviewItem.author.avatar"
                  :width="48"
                  :height="48"
                  :online="reviewItem.author.online"
                />
                <div class="flex-grow-1 ms-1">
                  <div class="d-flex justify-content-between">
                    <LocaleRouterLink
                      v-if="reviewItem.author.profile_url"
                      routeName="OrganizerDetail"
                      :routeParams="{ profile_url: reviewItem.author.profile_url }"
                      class="text-decoration-none link-dark"
                    >
                      <strong class="mb-0">
                        {{ reviewItem.author.name }}
                      </strong>
                    </LocaleRouterLink>
                    <strong
                      v-else
                      class="mb-0"
                    >
                      {{ reviewItem.author.name }}
                    </strong>
                    <small>
                      {{ getLocaleDateTimeString(reviewItem.created_at) }}
                    </small>
                  </div>
                  <div v-if="reviewItem.rating == 1">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                  </div>
                  <div v-else-if="reviewItem.rating == 2">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                  </div>
                  <div v-else-if="reviewItem.rating == 3">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                  </div>
                  <div v-else-if="reviewItem.rating == 4">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                  </div>
                  <div v-else-if="reviewItem.rating == 5">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                  </div>
                </div>
              </div>
              <p>{{ reviewItem.comment }}</p>
            </li>
          </TransitionGroup>
          <div v-if="nextURL" v-intersection="getMoreOrganizerReviews"></div>
          <LoadingIndicator v-if="reviewMoreLoading" />
        </div>
        <div
          v-else
          class="lead d-flex justify-content-center py-3"
        >
          {{ $t('organizers.no_reviews') }}
        </div>
      </div>
    </div>
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

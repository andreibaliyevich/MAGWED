<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()

const followingLoading = ref(true)
const followingMoreLoading = ref(false)
const followingList = ref([])
const followingCount = ref(0)
const nextURL = ref(null)

const getFollowing = async () => {
  try {
    const response = await axios.get(
      '/social/follow/list/'
        + '?follower='
        + userStore.uuid
    )
    followingList.value = response.data.results
    followingCount.value = response.data.count
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    followingLoading.value = false
  }
}

const getMoreFollowing = async () => {
  followingMoreLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    followingList.value = [...followingList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    followingMoreLoading.value = false
  }
}

onMounted(() => {
  getFollowing()
})
</script>

<template>
  <div class="following-view">
    <div class="container my-5">
      <h1 class="display-6 mb-5">
        {{ $t('follow.following') }} ({{ followingCount }})
      </h1>
      <LoadingIndicator v-if="followingLoading" />
      <div
        v-else-if="followingList.length > 0"
        class="row"
      >
        <div
          v-for="follow in followingList"
          :key="follow.user.uuid"
          class="col-12 col-md-6 col-lg-4 col-xl-3"
        >
          <LocaleRouterLink
            routeName="OrganizerDetail"
            :routeParams="{ profile_url: follow.user.profile_url }"
          >
            <UserAvatarExtended
              :src="follow.user.avatar"
              :width="180"
              :height="180"
              :online="follow.user.online"
            />
          </LocaleRouterLink>
          <LocaleRouterLink
            routeName="OrganizerDetail"
            :routeParams="{ profile_url: follow.user.profile_url }"
            class="text-decoration-none link-dark"
          >
            <h2 class="fw-normal">{{ follow.user.name }}</h2>
          </LocaleRouterLink>
        </div>
        <div v-if="nextURL" v-intersection="getMoreFollowing"></div>
        <LoadingIndicator v-if="followingMoreLoading" />
      </div>
      <div
        v-else
        class="lead fs-3 d-flex justify-content-center py-3"
      >
        {{ $t('follow.no_following') }}
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()

const followersLoading = ref(true)
const followersMoreLoading = ref(false)
const followersList = ref([])
const nextURL = ref(null)

const getFollowers = async () => {
  try {
    const response = await axios.get(
      '/social/follow/list/'
        + '?user='
        + userStore.uuid
    )
    followersList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    followersLoading.value = false
  }
}

const getMoreFollowers = async () => {
  followersMoreLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    followersList.value = [...followersList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    followersMoreLoading.value = false
  }
}

onMounted(() => {
  getFollowers()
})
</script>

<template>
  <div class="followers-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">
        {{ $t('auth.followers') }}
      </h1>
      <LoadingIndicator v-if="followersLoading" />
      <div
        v-else-if="followersList.length > 0"
        class="row"
      >
        <div
          v-for="follow in followersList"
          :key="follow.follower.uuid"
          class="col-12 col-sm-6 col-xl-4 text-center"
        >
          <LocaleRouterLink
            v-if="follow.follower.profile_url"
            routeName="OrganizerDetail"
            :routeParams="{ profile_url: follow.follower.profile_url }"
          >
            <UserAvatarExtended
              :src="follow.follower.avatar"
              :width="180"
              :height="180"
              :online="follow.follower.online"
            />
          </LocaleRouterLink>
          <UserAvatarExtended
            v-else
            :src="follow.follower.avatar"
            :width="180"
            :height="180"
            :online="follow.follower.online"
          />
          <LocaleRouterLink
            v-if="follow.follower.profile_url"
            routeName="OrganizerDetail"
            :routeParams="{ profile_url: follow.follower.profile_url }"
            class="text-decoration-none link-dark"
          >
            <h2 class="fw-normal">{{ follow.follower.name }}</h2>
          </LocaleRouterLink>
          <h2
            v-else
            class="fw-normal"
          >
            {{ follow.follower.name }}
          </h2>
        </div>
        <div v-if="nextURL" v-intersection="getMoreFollowers"></div>
        <LoadingIndicator v-if="followersMoreLoading" />
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'

const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const followingListLoading = ref(true)
const followingList = ref([])
const followingCount = ref(0)
const nextURL = ref(null)

const getFollowingList = async () => {
  try {
    const response = await axios.get('/social/follow/list/', {
      params: {
        follower: userStore.uuid
      }
    })
    followingList.value = response.data.results
    followingCount.value = response.data.count
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    followingListLoading.value = false
  }
}

const getMoreFollowingList = async () => {
  followingListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    followingList.value = [...followingList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    followingListLoading.value = false
  }
}

const updateUserStatus = (mutation, state) => {
  followingList.value.forEach((element) => {
    if (element.user.uuid === state.user_uuid) {
      element.user.status = state.status
    }
  })
}

onMounted(() => {
  getFollowingList()
  connectionBusStore.$subscribe(updateUserStatus)
})
</script>

<template>
  <div class="following-view">
    <div class="container my-5">
      <h1 class="display-6 text-center mb-5">
        {{ $t('follow.following') }} ({{ followingCount }})
      </h1>

      <div
        v-if="followingList.length > 0"
        class="row g-3"
      >
        <div
          v-for="follow in followingList"
          :key="follow.user.uuid"
          class="col-12 col-md-6 col-lg-4 col-xl-3 text-center"
        >
          <router-link
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: follow.user.profile_url }
            }"
          >
            <UserAvatarExtended
              :src="follow.user.avatar"
              :width="180"
              :height="180"
              :online="follow.user.status === 'online' ? true : false"
            />
          </router-link>
          <router-link
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: follow.user.profile_url }
            }"
            class="text-decoration-none link-dark"
          >
            <h2 class="fw-normal">{{ follow.user.name }}</h2>
          </router-link>
        </div>
      </div>
      <div
        v-else-if="!followingListLoading"
        class="lead fs-3 d-flex justify-content-center py-3"
      >
        {{ $t('follow.no_following') }}
      </div>
      <div
        v-if="nextURL"
        style="min-height: 1px; margin-bottom: 1px;"
        v-intersection="{
          'scrollArea': null,
          'callbackFunction': getMoreFollowingList,
          'functionArguments': []
        }"
      ></div>
      <LoadingIndicator v-if="followingListLoading" />
    </div>
  </div>
</template>

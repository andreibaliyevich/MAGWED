<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()

const followersListLoading = ref(true)
const followersList = ref([])
const followersCount = ref(0)
const nextURL = ref(null)

const getFollowersList = async () => {
  try {
    const response = await axios.get('/social/follow/list/', {
      params: {
        user: userStore.uuid
      }
    })
    followersList.value = response.data.results
    followersCount.value = response.data.count
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    followersListLoading.value = false
  }
}

const getMoreFollowersList = async () => {
  followersListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    followersList.value = [...followersList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    followersListLoading.value = false
  }
}

onMounted(() => {
  getFollowersList()
})
</script>

<template>
  <div class="followers-view">
    <div class="container my-5">
      <h1 class="display-6 text-center mb-5">
        {{ $t('follow.followers') }} ({{ followersCount }})
      </h1>

      <div
        v-if="followersList.length > 0"
        class="row g-3"
      >
        <div
          v-for="follow in followersList"
          :key="follow.follower.uuid"
          class="col-12 col-md-6 col-lg-4 col-xl-3 text-center"
        >
          <router-link
            v-if="follow.follower.profile_url"
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: follow.follower.profile_url }
            }"
          >
            <UserAvatarExtended
              :src="follow.follower.avatar"
              :width="180"
              :height="180"
              :online="follow.follower.status == 'online' ? true : false"
            />
          </router-link>
          <UserAvatarExtended
            v-else
            :src="follow.follower.avatar"
            :width="180"
            :height="180"
            :online="follow.follower.status == 'online' ? true : false"
          />
          <router-link
            v-if="follow.follower.profile_url"
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: follow.follower.profile_url }
            }"
            class="text-decoration-none link-dark"
          >
            <h2 class="fw-normal">{{ follow.follower.name }}</h2>
          </router-link>
          <h2
            v-else
            class="fw-normal"
          >
            {{ follow.follower.name }}
          </h2>
        </div>
      </div>
      <div
        v-else-if="!followersListLoading"
        class="lead fs-3 d-flex justify-content-center py-3"
      >
        {{ $t('follow.no_followers') }}
      </div>
      <div
        v-if="nextURL"
        style="min-height: 1px; margin-bottom: 1px;"
        v-intersection="{
          'scrollArea': null,
          'callbackFunction': getMoreFollowersList,
          'functionArguments': []
        }"
      ></div>
      <LoadingIndicator v-if="followersListLoading" />
    </div>
  </div>
</template>

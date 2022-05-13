<script setup>
import ProfileMenu from '@/components/auth/ProfileMenu.vue'

import { useBaseStore } from '@/stores/base.js'
import { useUserStore } from '@/stores/user.js'
const baseStore = useBaseStore()
const userStore = useUserStore()
</script>

<template>
  <div class="container my-5">
    <div class="row">
      <div class="col-lg-4">
        <ProfileMenu />
      </div>
      <div class="col-lg-8 px-5">
        <h1>This is a Messages page</h1>
        <div>
          Username: {{ userStore.username }}<br>
          Email: {{ userStore.email }}<br>
          Name: {{ userStore.name }}<br>
          <img v-if="userStore.avatar" :src="`${ baseStore.apiURL }${ userStore.avatar }`" width="100" height="100" class="bg-dark">
          <img v-else src="/avatar.png" width="100" height="100" class="bg-dark">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { API_URL } from '@/config.js'

import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<template>
  <div class="notifications">
    <h1>This is a Notifications page</h1>
    <div>
      Username: {{ userStore.username }}<br>
      Email: {{ userStore.email }}<br>
      Name: {{ userStore.name }}<br>
      <img v-if="userStore.avatar" :src="`${ API_URL }${ userStore.avatar }`" width="100" height="100" class="bg-dark">
      <img v-else src="/avatar.png" width="100" height="100" class="bg-dark">
    </div>
  </div>
</template>

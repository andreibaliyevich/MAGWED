<script setup>
import { API_URL } from '@/config.js'

import { useUserStore } from '@/stores/user.js'
const user = useUserStore()
</script>

<template>
  <div class="notifications-view">
    <h1>This is a Notifications page</h1>
    <div>
      Username: {{ user.username }}<br>
      Email: {{ user.email }}<br>
      Name: {{ user.name }}<br>
      <img v-if="user.avatar" :src="`${ API_URL }${ user.avatar }`" width="100" height="100" class="bg-dark">
      <img v-else src="/avatar.png" width="100" height="100" class="bg-dark">
    </div>
  </div>
</template>

<script setup>
import { useBaseStore } from '@/stores/base.js'
import { useUserStore } from '@/stores/user.js'
const baseStore = useBaseStore()
const userStore = useUserStore()
</script>

<template>
  <div class="notifications">
    <h1>This is a Notifications page</h1>
    <div>
      Username: {{ userStore.username }}<br>
      Email: {{ userStore.email }}<br>
      Name: {{ userStore.name }}<br>
      <img v-if="userStore.avatar" :src="`${ baseStore.apiURL }${ userStore.avatar }`" width="100" height="100" class="bg-dark">
      <img v-else src="/avatar.png" width="100" height="100" class="bg-dark">
    </div>
  </div>
</template>

<style>

</style>

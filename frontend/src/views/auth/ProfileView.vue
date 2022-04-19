<script setup>
import { useBaseStore } from '@/stores/base.js'
import { useUserStore } from '@/stores/user.js'
const baseStore = useBaseStore()
const userStore = useUserStore()
</script>

<template>
  <div class="profile">
    <h1>This is a profile page</h1>
    <div>
      Username: {{ userStore.username }}<br>
      Email: {{ userStore.email }}<br>
      Name: {{ userStore.name }}<br>
      <img v-if="userStore.avatar" :src="`${ baseStore.apiURL }${ userStore.avatar }`">
      <img v-else src="/avatar.png">
    </div>
  </div>
</template>

<style>

</style>

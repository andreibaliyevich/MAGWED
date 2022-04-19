<script setup>
import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<template>
  <div class="profile">
    <h1>This is a profile page</h1>
    <div>
      Username: {{ userStore.username }}<br>
      Email: {{ userStore.email }}<br>
      Name: {{ userStore.name }}<br>
      <img :src="'http://localhost:8000' + userStore.avatar">
    </div>
  </div>
</template>

<style>

</style>

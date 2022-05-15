<script setup>
import { RouterView } from 'vue-router'
import ProfileMenu from '@/components/auth/ProfileMenu.vue'
</script>

<template>
  <div class="container my-5">
    <div class="row">
      <div class="col-lg-4">
        <ProfileMenu />
      </div>
      <div class="col-lg-8 px-5">
        <RouterView />
      </div>
    </div>
  </div>
</template>

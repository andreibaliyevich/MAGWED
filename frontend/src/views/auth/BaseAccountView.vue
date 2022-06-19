<script setup>
import { RouterView } from 'vue-router'
import AccountMenu from '@/components/auth/AccountMenu.vue'
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col-lg-4 border-end py-5">
        <AccountMenu />
      </div>
      <div class="col-lg-8 pb-5 p-lg-5">
        <RouterView />
      </div>
    </div>
  </div>
</template>

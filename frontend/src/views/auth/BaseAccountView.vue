<script setup>
import { RouterView } from 'vue-router'
import AccountMenu from '@/components/auth/AccountMenu.vue'
</script>

<template>
  <div class="base-account-view">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 py-5">
          <AccountMenu />
        </div>
        <div class="col-lg-8 pb-5 p-lg-5">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media(min-width: 992px) {
  .col-lg-4.py-5 {
    border-right: 1px solid #dee2e6;
  }
}
</style>

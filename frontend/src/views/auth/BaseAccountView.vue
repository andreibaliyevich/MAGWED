<script setup>
import { RouterView } from 'vue-router'
import AccountMenu from '@/components/auth/AccountMenu.vue'
import AccountMenuLg from '@/components/auth/AccountMenuLg.vue'
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col-lg-4 pt-5 pb-3 d-lg-none">
        <AccountMenu />
      </div>
      <div class="col-lg-4 border-end py-5 d-none d-lg-block">
        <AccountMenuLg />
      </div>
      <div class="col-lg-8 pb-5 p-lg-5">
        <RouterView />
      </div>
    </div>
  </div>
</template>

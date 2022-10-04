<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="container-fluid">
    <section
      id="section-bg"
      class="row justify-content-center align-items-center py-5"
    >
      <div class="col-11 col-sm-10 col-md-8 col-lg-6 col-xl-5 col-xxl-4 bg-light border rounded-4 p-4 p-md-5">
        <RouterView />
      </div>
    </section>
  </div>
</template>

<style scoped>
#section-bg {
  background-image: url('/bg.jpg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  min-height: 85vh;
}
</style>

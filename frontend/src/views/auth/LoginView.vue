<script setup>
import axios from 'axios'
import { useUserStore } from '@/stores/user.js'
const userStore = useUserStore()
</script>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      error: null
    }
  },
  methods: {
    onSubmit() {
      this.userStore.login({
        username: this.username,
        password: this.password
      })
      .then(() => {
        this.$router.push({ name: 'home' })
      })
      .catch((error) => {
        this.error = error
      })
    }
  }
}
</script>

<template>
  <div class="login-view">
    <h4>{{ $t('auth.login') }}</h4>
    <div class="input-group">
      <form @submit.prevent="onSubmit">
        <input v-model="username" type="text" name="username" :placeholder="$t('auth.username')" class="form-control">
        <input v-model="password" type="password" name="password" :placeholder="$t('auth.password')" class="form-control">
        <button type="submit" class="btn btn-primary">{{ $t('auth.login') }}</button>
      </form>
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<style>
.login-view {
  width: 300px;
  margin: 0 auto;
}
</style>

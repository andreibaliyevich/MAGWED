<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      authToken: '',
      username: '',
      password: ''
    }
  },
  methods: {
    async onSubmit() {
      try {
        const response = await axios.post('/en/accounts/auth/login/', {
          username: this.username,
          password: this.password
        });
        this.authToken = response.data.token;
      } catch (error) {
        console.error(error);
      } finally {
        console.log(this.authToken);
      }
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
    </div>
  </div>
</template>

<style>
.login-view {
  width: 300px;
  margin: 0 auto;
}
</style>

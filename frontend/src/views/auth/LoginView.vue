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
    login() {
      axios.post('/en/accounts/auth/login/', {
        username: this.username,
        password: this.password
      })
      .then(({ data }) => {
        window.localStorage.setItem('user', JSON.stringify(data))
        axios.defaults.headers.common['Authorization'] = `Token ${ data.token }`
        this.userStore.setUserData(data)

        if (this.$route.query.redirect) {
          this.$router.push({ path: this.$route.query.redirect })
        } else {
          this.$router.push({ name: 'Home', params: { locale: `${ this.$i18n.locale }` }})
        }
      })
      .catch((error) => {
        this.error = error.response.data
      })
    }
  }
}
</script>

<template>
  <div class="login-view">
    <h4>{{ $t('auth.login') }}</h4>
    <div class="input-group">
      <form @submit.prevent="login">
        <input v-model="username" type="text" name="username" :placeholder="$t('auth.username_email')" class="form-control">
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

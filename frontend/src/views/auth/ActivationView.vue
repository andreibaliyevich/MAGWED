<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      status: null
    }
  },
  mounted() {
    axios.post('/en/accounts/auth/activation/', {
      uid: this.$route.params.uid,
      token: this.$route.params.token
    })
    .then((response) => {
      if (response.status === 204) {
        this.status = '204'
      }
    })
    .catch((error) => {
      this.status = error.response.data
    })
  }
}
</script>

<template>
  <div class="login-view">
    <h4>{{ $t('auth.activation') }}</h4>
    <p>{{ status }}</p>
  </div>
</template>

<style>
.login-view {
  width: 300px;
  margin: 0 auto;
}
</style>

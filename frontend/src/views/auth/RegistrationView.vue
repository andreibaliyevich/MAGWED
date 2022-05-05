<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: '',
      user_type: '',
      name: '',
      error: null
    }
  },
  methods: {
    login() {
      axios.post('/en/accounts/auth/registration/', {
        username: this.username,
        email: this.email,
        password: this.password,
        password2: this.password2,
        user_type: this.user_type,
        name: this.name
      })
      .then((response) => {
        if (response.status === 201) {
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
    <h4>{{ $t('auth.registration') }}</h4>
    <div class="input-group">
      <form @submit.prevent="login">
        <input v-model="username" type="text" name="username" :placeholder="$t('auth.username')" class="form-control">
        <input v-model="email" type="email" name="email" :placeholder="$t('auth.email')" class="form-control">
        <input v-model="password" type="password" name="password" :placeholder="$t('auth.password')" class="form-control">
        <input v-model="password2" type="password" name="password2" :placeholder="$t('auth.password2')" class="form-control">        
        <select v-model="user_type" name="user_type" id="pet-select" class="form-select">
          <option disabled value="">Please select a User Type</option>
          <option value="2">Customer</option>
          <option value="3">Organizer</option>
        </select>
        <input v-model="name" type="text" name="name" :placeholder="$t('auth.name')" class="form-control">
        <button type="submit" class="btn btn-primary">{{ $t('auth.registration') }}</button>
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

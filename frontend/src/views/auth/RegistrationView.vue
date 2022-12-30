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
      userType: '',
      name: '',
      userTypeOptions: [],
      actionProcessing: false,
      status: null,
      errors: null
    }
  },
  methods: {
    setUserTypeOptions() {
      this.userTypeOptions = [
        { value: 2, text: this.$t('auth.registration.customer') },
        { value: 3, text: this.$t('auth.registration.organizer') }
      ]
    },
    registration() {
      this.actionProcessing = true
      axios.post('/accounts/auth/registration/', {
        username: this.username,
        email: this.email,
        password: this.password,
        password2: this.password2,
        user_type: this.userType,
        name: this.name
      })
      .then((response) => {
        if (response.status === 201) {
          this.status = '201'
          this.errors = null
        }
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
      .then(() => {
        this.actionProcessing = false
        document.body.scrollTop = 0
        document.documentElement.scrollTop = 0
      })
    }
  },
  watch: {
    '$i18n.locale'(newValue) {
      this.setUserTypeOptions()
    },
  },
  mounted() {
    this.setUserTypeOptions()
  }
}
</script>

<template>
  <div class="registration-view">
    <h1 class="display-6 text-center">
      {{ $t('auth.registration.registration') }}
    </h1>

    <ActionProcessingIndicator v-if="actionProcessing" />

    <div
      v-if="status == '201'"
      class="mt-4"
    >
      <p class="lead fs-3 text-muted">{{ $t('auth.registration.success1') }}</p>
      <p class="lead fs-5">
        {{ $t('auth.registration.success2') }}<br>
        {{ $t('auth.registration.success3') }}
      </p>
    </div>

    <form
      v-else
      @submit.prevent="registration"
      :class="{ 'mt-4': !actionProcessing }"
    >
      <p class="fs-6 text-muted">
        {{ $t('auth.registration.have_account') }}
        <LocaleRouterLink
          routeName="Login"
          class="link-primary text-decoration-none"
        >
          {{ $t('auth.log_in') }}
        </LocaleRouterLink>
      </p>

      <div class="row g-3 mb-3">
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.username"
            v-model="username"
            :label="$t('auth.registration.username')"
            :errors="errors.username"
            id="id_username"
            name="username"
            type="text"
          />
          <BaseInput
            v-else
            v-model="username"
            :label="$t('auth.registration.username')"
            id="id_username"
            name="username"
            type="text"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.email"
            v-model="email"
            :label="$t('auth.registration.email')"
            :errors="errors.email"
            id="id_email"
            name="email"
            type="email"
            maxlength="254"
          />
          <BaseInput
            v-else
            v-model="email"
            :label="$t('auth.registration.email')"
            id="id_email"
            name="email"
            type="email"
            maxlength="254"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.password"
            v-model="password"
            :label="$t('auth.password.password')"
            :errors="errors.password"
            id="id_password"
            name="password"
            type="password"
          />
          <BaseInput
            v-else
            v-model="password"
            :label="$t('auth.password.password')"
            id="id_password"
            name="password"
            type="password"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.password2"
            v-model="password2"
            :label="$t('auth.registration.password2')"
            :errors="errors.password2"
            id="id_password2"
            name="password2"
            type="password"
          />
          <BaseInput
            v-else
            v-model="password2"
            :label="$t('auth.registration.password2')"
            id="id_password2"
            name="password2"
            type="password"
          />
        </div>
        <div class="col-md-12">
          <BaseSelect
            v-if="errors && errors.user_type"
            v-model="userType"
            :label="$t('auth.registration.user_type')"
            :options="userTypeOptions"
            :errors="errors.user_type"
            id="id_user_type"
            name="user_type"
          />
          <BaseSelect
            v-else
            v-model="userType"
            :label="$t('auth.registration.user_type')"
            :options="userTypeOptions"
            id="id_user_type"
            name="user_type"
          />
        </div>
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.name"
            v-model="name"
            :label="$t('auth.registration.name')"
            :errors="errors.name"
            id="id_name"
            name="name"
            type="text"
          />
          <BaseInput
            v-else
            v-model="name"
            :label="$t('auth.registration.name')"
            id="id_name"
            name="name"
            type="text"
          />
        </div>
      </div>

      <button
        type="submit"
        class="btn btn-brand btn-lg w-100"
      >
        {{ $t('auth.register') }}
      </button>

      <hr class="my-4">
      <div class="fs-6 text-muted">
        {{ $t('auth.registration.help') }}
      </div>
    </form>
  </div>
</template>

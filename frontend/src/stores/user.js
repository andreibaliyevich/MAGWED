import { defineStore } from 'pinia'

export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    token: null,
    username: null,
    email: null,
    user_type: null,
    name: null,
    avatar: null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  actions: {
    setUserData(data) {
      this.token = data.token
      this.username = data.username
      this.email = data.email
      this.user_type = data.user_type
      this.name = data.name
      this.avatar = data.avatar
    },
    updateUsername(value) {
      this.username = value
    },
    updateEmail(value) {
      this.email = value
    },
    updateName(value) {
      this.name = value
    },
    updateAvatar(value) {
      this.avatar = value
    }
  }
})

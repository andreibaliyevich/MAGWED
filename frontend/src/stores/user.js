import { defineStore } from 'pinia'

export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    token: null,
    username: null,
    user_type: null,
    avatar: null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  actions: {
    setUserData(data) {
      this.token = data.token
      this.username = data.username
      this.user_type = data.user_type
      this.avatar = data.avatar
    },
    updateUsername(value) {
      this.username = value
    },
    updateAvatar(value) {
      this.avatar = value
    }
  }
})

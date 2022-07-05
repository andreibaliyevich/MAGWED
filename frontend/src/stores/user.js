import { defineStore } from 'pinia'

export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    token: null,
    id: null,
    username: null,
    email: null,
    userType: null,
    name: null,
    avatar: null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  actions: {
    setUserData(data) {
      this.token = data.token
      this.id = data.id
      this.username = data.username
      this.email = data.email
      this.userType = data.user_type
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

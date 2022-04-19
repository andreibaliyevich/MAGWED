import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    token: null,
    username: null,
    email: null,
    name: null,
    avatar: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  actions: {
    setUserData(data) {
      this.token = data.token
      this.username = data.username
      this.email = data.email
      this.name = data.name
      this.avatar = data.avatar
    }
  }
})

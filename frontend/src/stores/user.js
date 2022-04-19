import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    token: null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  actions: {
    setUserData(data) {
      this.token = data.token
    }
  }
})

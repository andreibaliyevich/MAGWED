import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore({
  id: 'auth',
  state: () => ({
    token: null
  }),
  getters: {
    loggedIn: (state) => state.token ? true : false
  },
  actions: {
    setUserData(data) {
      this.token = data.token
      window.localStorage.setItem('AUTH_TOKEN', data.token)
      axios.defaults.headers.common['Authorization'] = 'Token ' + data.token
    },
    login(credentials) {
      return axios
        .post('/en/accounts/auth/login/', credentials)
        .then(({ data }) => {
          this.setUserData(data)
        })
    }
  }
})

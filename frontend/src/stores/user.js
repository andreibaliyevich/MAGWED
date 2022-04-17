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
    login(credentials) {
      return axios
        .post('/en/accounts/auth/login/', credentials)
        .then(({ data }) => {
          this.token = data.token
          window.localStorage.setItem('AUTH_TOKEN', data.token)
          axios.defaults.headers.common['Authorization'] = 'Token ' + data.token
        })
    },
    logout() {
      return axios
        .post('/en/accounts/auth/logout/')
        .catch((error) => {
          console.log(error)
        })
        .then(() => {
          this.token = null
          localStorage.removeItem('AUTH_TOKEN')
          axios.defaults.headers.common['Authorization'] = undefined
        })
    }
  }
})

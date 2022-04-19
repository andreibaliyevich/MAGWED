import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    user: null
  }),
  getters: {
    isLoggedIn: (state) => !!state.user
  },
  actions: {
    setUser(value) {
      this.user = value
    },
    login(credentials) {
      return axios
        .post('/en/accounts/auth/login/', credentials)
        .then(({ data }) => {
          this.user = data
          window.localStorage.setItem('AUTH_USER', JSON.stringify(data))
          axios.defaults.headers.common['Authorization'] = `Token ${ data.token }`
        })
    },
    logout() {
      return axios
        .post('/en/accounts/auth/logout/')
        .catch((error) => {
          console.log(error)
        })
        .then(() => {
          this.user = null
          window.localStorage.removeItem('AUTH_USER')
          axios.defaults.headers.common['Authorization'] = undefined
        })
    }
  }
})

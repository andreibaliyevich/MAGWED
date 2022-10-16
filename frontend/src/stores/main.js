import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    apiURL: 'http://localhost:8000',
    wsURL: 'ws://localhost:8000',
    currency: 'USD'
  }),
  actions: {
    setCurrency(value) {
      this.currency = value
    }
  }
})

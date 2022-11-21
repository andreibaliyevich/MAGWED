import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    currency: 'USD'
  }),
  actions: {
    setCurrency(value) {
      this.currency = value
    }
  }
})

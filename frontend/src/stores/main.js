import { defineStore } from 'pinia'

export const useMainStore = defineStore('mainStore', {
  state: () => ({
    currency: 'USD'
  }),
  actions: {
    setCurrency(value) {
      this.currency = value
    }
  }
})

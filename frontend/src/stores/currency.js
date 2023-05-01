import { defineStore } from 'pinia'

export const useCurrencyStore = defineStore('currencyStore', {
  state: () => ({
    currencyValue: 'USD'
  }),
  actions: {
    setCurrency(value) {
      this.currencyValue = value
    }
  }
})

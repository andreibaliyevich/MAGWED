import { defineStore } from 'pinia'
import { CURRENCIES } from '@/config.js'

export const useCurrencyStore = defineStore('currencyStore', {
  state: () => ({
    currencyValue: CURRENCIES[0].value,
    currencyText: CURRENCIES[0].text
  }),
  actions: {
    setCurrency(value) {
      this.currencyValue = value
      CURRENCIES.forEach((element) => {
        if (element.value == value) {
          this.currencyText = element.text
        }
      })
    }
  }
})

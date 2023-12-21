import axios from 'axios'
import { defineStore } from 'pinia'
import { CURRENCIES } from '@/config.js'

export const useCurrencyStore = defineStore('currencyStore', {
  state: () => ({
    currencyValue: CURRENCIES[0].value,
    currencyText: CURRENCIES[0].text,
    conversionRate: 1
  }),
  actions: {
    async setCurrency(value) {
      this.currencyValue = value

      CURRENCIES.forEach((element) => {
        if (element.value == value) {
          this.currencyText = element.text
        }
      })

      try {
        const response = await axios.get(
          '/main/currencies/'
            + value
            + '/'
        )
        this.conversionRate = response.data.conversion_rate
      } catch (error) {
        console.error(error)
      }
    },
    convertCurrency(value) {
      return (value * this.conversionRate).toFixed(2)
    }
  }
})

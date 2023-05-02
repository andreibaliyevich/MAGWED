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

      const EXCHANGERATE_API_KEY = import.meta.env.VITE_EXCHANGERATE_API_KEY
      const exchangerateAPI = axios.create({
        baseURL: 'https://v6.exchangerate-api.com/v6/'
      })

      try {
        const response = await exchangerateAPI.get(
          EXCHANGERATE_API_KEY
          + '/pair/'
          + CURRENCIES[0].value
          + '/'
          + value
        )
        this.conversionRate = response.data.conversion_rate
      } catch (error) {
        console.error(error)
      }
    }
  }
})

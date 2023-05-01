import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { CURRENCIES } from '@/config.js'
import { useCurrencyStore } from '@/stores/currency.js'

export function useCurrency() {
  const currencyStore = useCurrencyStore()
  const currencyText = ref(null)
  const conversionRate = ref(1.00)

  const EXCHANGERATE_API_KEY = import.meta.env.VITE_EXCHANGERATE_API_KEY
  const exchangerateAPI = axios.create({
    baseURL: 'https://v6.exchangerate-api.com/v6/'
  })

  const getAndSetCurrencyText = () => {
    CURRENCIES.forEach((element) => {
      if (element.value == currencyStore.currencyValue) {
        currencyText.value = element.text
      }
    })
  }

  const getAndSetConversionRate = async () => {
    try {
      const response = await exchangerateAPI.get(
        EXCHANGERATE_API_KEY
        + '/pair/'
        + CURRENCIES[0].value
        + '/'
        + currencyStore.currencyValue
      )
      conversionRate.value = response.data.conversion_rate
    } catch (error) {
      console.error(error)
    }
  }

  const getValueInCurrency = (valueString) => {
    return (Number(valueString) * conversionRate.value).toFixed(2)
  }

  watch(
    () => currencyStore.currencyValue,
    (newValue) => {
      if (newValue == CURRENCIES[0].value) {
        conversionRate.value = 1.00
      } else {
        getAndSetConversionRate()
      }
      getAndSetCurrencyText()
    }
  )

  onMounted(() => {
    getAndSetCurrencyText()
    if (currencyStore.currencyValue != CURRENCIES[0].value) {
      getAndSetConversionRate()
    }
  })

  return { currencyText, getValueInCurrency }
}

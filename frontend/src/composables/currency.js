import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { CURRENCIES } from '@/config.js'
import { useMainStore } from '@/stores/main.js'

export function useCurrency() {
  const mainStore = useMainStore()
  const { currency } = storeToRefs(mainStore)
  const currencyText = ref(null)
  const conversionRate = ref(1.00)

  const EXCHANGERATE_API_KEY = import.meta.env.VITE_EXCHANGERATE_API_KEY
  const exchangerateAPI = axios.create({
    baseURL: 'https://v6.exchangerate-api.com/v6/'
  })

  const getAndSetCurrencyText = () => {
    CURRENCIES.forEach((element) => {
      if (element.value == currency.value) {
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
        + currency.value
      )
      conversionRate.value = response.data.conversion_rate
    } catch (error) {
      console.error(error)
    }
  }

  const getValueInCurrency = (valueString) => {
    return (Number(valueString) * conversionRate.value).toFixed(2)
  }

  watch(currency, (newValue) => {
    if (newValue == CURRENCIES[0].value) {
      conversionRate.value = 1.00
    } else {
      getAndSetConversionRate()
    }
    getAndSetCurrencyText()
  })

  onMounted(() => {
    getAndSetCurrencyText()
    if (currency.value != CURRENCIES[0].value) {
      getAndSetConversionRate()
    }
  })

  return { currencyText, getValueInCurrency }
}

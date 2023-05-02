import { useCurrencyStore } from '@/stores/currency.js'

export function useCurrencyConversion() {
  const currencyStore = useCurrencyStore()

  const convertToCurrency = (value) => {
    return (value * currencyStore.conversionRate).toFixed(2)
  }

  return { convertToCurrency }
}

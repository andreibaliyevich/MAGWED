import { useCurrencyStore } from '@/stores/currency.js'

export function useCurrencyConversion() {
  const currencyStore = useCurrencyStore()

  const conversionToCurrency = (value) => {
    return (value * currencyStore.conversionRate).toFixed(2)
  }

  return { conversionToCurrency }
}

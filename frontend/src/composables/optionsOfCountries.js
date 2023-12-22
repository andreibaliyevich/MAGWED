import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { ref, watch, onMounted } from 'vue'

export function useOptionsOfCountries() {
  const { t, locale } = useI18n({ useScope: 'global' })
  const countryOptions = ref([])

  const setCountryOptions = () => {
    countryOptions.value = [
      { value: 'BY', text: t('countries.BY') },
      { value: 'RU', text: t('countries.RU') },
      { value: 'UA', text: t('countries.UA') }
    ]
  }

  watch(locale, () => {
    setCountryOptions()
  })

  onMounted(() => {
    setCountryOptions()
  })

  return { countryOptions }
}

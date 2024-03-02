import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { ref, watch, onMounted } from 'vue'

export function useOptionsOfCountries() {
  const { t, locale } = useI18n({ useScope: 'global' })
  const countryOptions = ref([])

  const setCountryOptions = () => {
    countryOptions.value = [
      { value: 'BY', title: t('countries.BY') },
      { value: 'RU', title: t('countries.RU') },
      { value: 'UA', title: t('countries.UA') }
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

import axios from 'axios'
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'

export function useOptionsOfCities(country) {
  const { t, locale } = useI18n({ useScope: 'global' })
  const cityValues = ref([])

  const cityOptions = computed(() => {
    return cityValues.value.map((element) => {
      return {
        'value': element.code,
        'text': t(`cities.${element.code}`)
      }
    })
  })

  const getAndSetCityOptions = async (countryValue) => {
    try {
      const response = await axios.get('/main/cities/', {
        params: {
          'country': countryValue
        }
      })
      cityValues.value = response.data
    } catch (error) {
      console.error(error)
    }
  }

  watch(country, (newValue) => {
    if (newValue) {
      getAndSetCityOptions(newValue)
    } else {
      cityValues.value = []
    }
  })

  watch(locale, () => {
    getAndSetCityOptions(country.value)
  })

  return { cityOptions }
}

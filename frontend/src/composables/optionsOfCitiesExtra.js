import axios from 'axios'
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'

export function useOptionsOfCitiesExtra(countries) {
  const { t, locale } = useI18n({ useScope: 'global' })
  const cityValuesExtra = ref([])

  const cityOptionsExtra = computed(() => {
    return cityValuesExtra.value.map((element) => {
      return {
        'value': element.code,
        'text': t(`cities.${element.code}`)
      }
    })
  })

  const getAndSetCityOptionsExtra = async (params) => {
    try {
      const response = await axios.get('/main/cities/', { params: params })
      cityValuesExtra.value = response.data
    } catch (error) {
      console.error(error)
    }
  }

  watch(countries, (newValue) => {
    if (newValue.length > 0) {
      let params = new URLSearchParams()
      newValue.forEach((element) => params.append('country', element))
      getAndSetCityOptionsExtra(params)
    } else {
      cityValuesExtra.value = []
    }
  })

  watch(locale, () => {
    let params = new URLSearchParams()
    countries.value.forEach((element) => params.append('country', element))
    getAndSetCityOptionsExtra(params)
  })

  return { cityOptionsExtra }
}

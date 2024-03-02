import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { ref, computed, watch } from 'vue'

export function useOptionsOfCitiesExtra(countries) {
  const { t, locale } = useI18n({ useScope: 'global' })
  const cityValuesExtra = ref([])

  const cityOptionsExtra = computed(() => {
    return cityValuesExtra.value.map((element) => {
      return {
        value: element.code,
        title: t(`cities.${element.code}`)
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

  return { cityOptionsExtra }
}

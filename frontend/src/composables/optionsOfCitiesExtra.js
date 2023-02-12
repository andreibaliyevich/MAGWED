import axios from 'axios'
import { ref, watch } from 'vue'

export function useOptionsOfCitiesExtra(countries) {
  const citiesExtraOptions = ref([])

  const getAndSetCitiesExtra = async (params) => {
    try {
      const response = await axios.get('/main/cities/', { params: params })
      citiesExtraOptions.value = []
      response.data.forEach((element) => {
        citiesExtraOptions.value.push({
          'value': element.code,
          'text': `${ element.name_local } (${ element.name })`
        })
      })
    } catch (error) {
      console.error(error)
    }
  }

  watch(countries, (newValue) => {
    if (newValue.length > 0) {
      let params = new URLSearchParams()
      newValue.forEach((element) => params.append('country', element))
      getAndSetCitiesExtra(params)
    } else {
      citiesExtraOptions.value = []
    }
  })

  return { citiesExtraOptions }
}

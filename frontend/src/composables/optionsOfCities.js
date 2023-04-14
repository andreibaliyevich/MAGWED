import axios from 'axios'
import { ref, watch } from 'vue'

export function useOptionsOfCities(country) {
  const cityOptions = ref([])

  const getAndSetCities = async (countryValue) => {
    try {
      const response = await axios.get('/main/cities/', {
        params: {
          country: countryValue
        }
      })
      cityOptions.value = []
      response.data.forEach((element) => {
        cityOptions.value.push({
          'value': element.code,
          'text': `${ element.name_local } (${ element.name })`
        })
      })
    } catch (error) {
      console.error(error)
    }
  }

  watch(country, (newValue) => {
    if (newValue) {
      getAndSetCities(newValue)
    } else {
      cityOptions.value = []
    }
  })

  return { cityOptions }
}

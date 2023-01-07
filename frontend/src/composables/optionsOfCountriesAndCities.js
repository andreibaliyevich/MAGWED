import { ref, watch, onMounted } from 'vue'
import axios from 'axios'

export function useOptionsOfCountriesAndCities(country) {
  const countriesOptions = ref([])
  const citiesOptions = ref([])

  const getAndSetCountries = async () => {
    try {
      const response = await axios.get('/main/countries/')
      response.data.forEach((element) => {
        countriesOptions.value.push({
          'value': element.code,
          'text': `${ element.name_local } (${ element.name })`
        })
      })
    } catch (error) {
      console.error(error)
    }
  }

  const getAndSetCities = async (countryValue) => {
    try {
      const response = await axios.get('/main/cities/', {
        params: {
          country: countryValue
        }
      })
      response.data.forEach((element) => {
        citiesOptions.value.push({
          'value': element.id,
          'text': `${ element.name_local } (${ element.name })`
        })
      })
    } catch (error) {
      console.error(error)
    }
  }

  watch(country, (newValue) => {
    citiesOptions.value = []
    if (newValue) {
      getAndSetCities(newValue)
    }
  })

  onMounted(() => {
    getAndSetCountries()
  })

  return {
    countriesOptions,
    citiesOptions
  }
}

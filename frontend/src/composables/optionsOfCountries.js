import axios from 'axios'
import { ref, onMounted } from 'vue'

export function useOptionsOfCountries() {
  const countriesOptions = ref([])

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

  onMounted(() => {
    getAndSetCountries()
  })

  return { countriesOptions }
}

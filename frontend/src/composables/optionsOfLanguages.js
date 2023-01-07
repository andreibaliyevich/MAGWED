import { ref, onMounted } from 'vue'
import axios from 'axios'

export function useOptionsOfLanguages() {
  const languagesOptions = ref([])

  const getAndSetLanguages = async () => {
    try {
      const response = await axios.get('/main/languages/')
      response.data.forEach((element) => {
        languagesOptions.value.push({
          'value': element.code,
          'text': `${ element.name_local } (${ element.name })`
        })
      })
    } catch (error) {
      console.error(error)
    }
  }

  onMounted(() => {
    getAndSetLanguages()
  })

  return { languagesOptions }
}

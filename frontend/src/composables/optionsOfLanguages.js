import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

export function useOptionsOfLanguages() {
  const { t, locale } = useI18n({ useScope: 'global' })
  const languageOptions = ref([])

  const setLanguageOptions = () => {
    languageOptions.value = [
      { value: 'be', text: t('languages.be') },
      { value: 'en', text: t('languages.en') },
      { value: 'fr', text: t('languages.fr') },
      { value: 'de', text: t('languages.de') },
      { value: 'pl', text: t('languages.pl') },
      { value: 'pt', text: t('languages.pt') },
      { value: 'ru', text: t('languages.ru') },
      { value: 'uk', text: t('languages.uk') }
    ]
  }

  watch(locale, () => {
    setLanguageOptions()
  })

  onMounted(() => {
    setLanguageOptions()
  })

  return { languageOptions }
}

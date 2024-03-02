import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { ref, watch, onMounted } from 'vue'

export function useOptionsOfLanguages() {
  const { t, locale } = useI18n({ useScope: 'global' })
  const languageOptions = ref([])

  const setLanguageOptions = () => {
    languageOptions.value = [
      { value: 'be', title: t('languages.be') },
      { value: 'en', title: t('languages.en') },
      { value: 'fr', title: t('languages.fr') },
      { value: 'de', title: t('languages.de') },
      { value: 'pl', title: t('languages.pl') },
      { value: 'pt', title: t('languages.pt') },
      { value: 'ru', title: t('languages.ru') },
      { value: 'uk', title: t('languages.uk') }
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

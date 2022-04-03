import { createI18n } from 'vue-i18n'
import en from '@/locales/en.json'
import ru from '@/locales/ru.json'
import be from '@/locales/be.json'
import uk from '@/locales/uk.json'


export default createI18n({
  legacy: false,
  globalInjection: true,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: en,
    ru: ru,
    be: be,
    uk: uk
  }
})

import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import ru from './locales/ru.json'
import be from './locales/be.json'
import uk from './locales/uk.json'

const availableLanguages = ['en', 'ru', 'be', 'uk'];

function getLanguage() {
  const navigatorLanguage =
    navigator.languages !== undefined
      ? navigator.languages[0]
      : navigator.language;

  if (!navigatorLanguage) {
    return availableLanguages[0];
  }

  const trimmedLanguage = navigatorLanguage.trim().split(/-|_/)[0];

  if (!availableLanguages.includes(trimmedLanguage)) {
    return availableLanguages[0];
  }

  return trimmedLanguage;
}

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: getLanguage(),
  fallbackLocale: 'en',
  messages: {
    en: en,
    ru: ru,
    be: be,
    uk: uk
  }
})

export default i18n

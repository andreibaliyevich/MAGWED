import axios from 'axios'
import { nextTick } from 'vue'
import { createI18n } from 'vue-i18n'
import { API_URL, LANGUAGES } from '@/config.js'
import { pluralSlavicRule } from './rules.js'

export const SUPPORT_LOCALES = Array.from(LANGUAGES, element => element.value)

function getStartingLocale() {
  const navigatorLocale =
    window.navigator.languages !== undefined
      ? window.navigator.languages[0]
      : window.navigator.language

  if (!navigatorLocale) {
    return SUPPORT_LOCALES[0]
  }

  const trimmedLocale = navigatorLocale.trim().split(/-|_/)[0]

  if (!SUPPORT_LOCALES.includes(trimmedLocale)) {
    return SUPPORT_LOCALES[0]
  }

  return trimmedLocale
}

export async function loadLocaleMessages(i18n, locale) {
  const messages = await import(`./locales/${ locale }.json`)
  i18n.global.setLocaleMessage(locale, messages.default)
  return nextTick()
}

export function setI18nLanguage(i18n, locale) {
  i18n.global.locale.value = locale
  axios.defaults.baseURL = `${ API_URL }/${ locale }`
  axios.defaults.headers.common['Accept-Language'] = locale
  document.querySelector('html').setAttribute('lang', locale)
}

const startingLocale = getStartingLocale()

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: startingLocale,
  fallbackLocale: 'en',
  pluralRules: {
    ru: pluralSlavicRule,
    be: pluralSlavicRule,
    uk: pluralSlavicRule
  }
})
await loadLocaleMessages(i18n, startingLocale)
setI18nLanguage(i18n, startingLocale)

export default i18n

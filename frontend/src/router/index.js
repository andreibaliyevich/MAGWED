import { createRouter, createWebHistory } from 'vue-router'
import Root from './Root.vue'
import i18n, {
  SUPPORT_LOCALES,
  loadLocaleMessages,
  setI18nLanguage
} from '@/i18n'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: i18n.global.locale.value
    },
    {
      path: '/:locale',
      component: Root,
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue')
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/AboutView.vue')
        },
        {
          path: 'login',
          name: 'login',
          component: () => import('@/views/auth/LoginView.vue')
        },
        {
          path: 'blog',
          name: 'blog',
          component: () => import('@/views/blog/ArticleListView.vue')
        }
      ]
    }
  ]
})

router.beforeEach(async (to, from) => {
  if (!to.params.locale) {
    return { name: 'home', params: { locale: i18n.global.locale.value }}
  }

  if (!SUPPORT_LOCALES.includes(to.params.locale)) {
    return '/' + i18n.global.locale.value + to.path
  }

  if (!i18n.global.availableLocales.includes(to.params.locale)) {
    await loadLocaleMessages(i18n, to.params.locale)
  }

  if (!(to.params.locale === i18n.global.locale.value)) {
    setI18nLanguage(i18n, to.params.locale)
  }
})

export default router

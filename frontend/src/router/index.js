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
      path: '/:locale',
      name: 'Root',
      component: Root,
      children: [
        {
          path: '',
          name: 'Home',
          component: () => import('@/views/HomeView.vue')
        },
        {
          path: 'about',
          name: 'About',
          component: () => import('@/views/AboutView.vue')
        },
        {
          path: 'blog',
          name: 'Blog',
          component: () => import('@/views/blog/ArticleListView.vue')
        },
        {
          path: 'login',
          name: 'Login',
          component: () => import('@/views/auth/LoginView.vue')
        },
        {
          path: 'registration',
          name: 'Registration',
          component: () => import('@/views/auth/RegistrationView.vue')
        },
        {
          path: 'activation/:uid/:token',
          name: 'Activation',
          component: () => import('@/views/auth/ActivationView.vue')
        },
        {
          path: '',
          name: 'BaseAuth',
          component: () => import('@/views/auth/BaseAuthView.vue'),
          meta: { requiresAuth: true },
          children: [
            {
              path: 'profile',
              name: 'Profile',
              component: () => import('@/views/auth/ProfileView.vue')
            },
            {
              path: 'externallinks',
              name: 'ExternalLinks',
              component: () => import('@/views/auth/ExternalLinksView.vue')
            },
            {
              path: 'messenger',
              name: 'Messenger',
              component: () => import('@/views/auth/MessengerView.vue')
            },
            {
              path: 'notifications',
              name: 'Notifications',
              component: () => import('@/views/auth/NotificationsView.vue')
            }
          ]
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: '404NotFound',
      component: () => import('@/views/404NotFoundView.vue')
    }
  ]
})

router.beforeEach(async (to, from) => {
  let to_locale = to.params.locale

  if (!to_locale) {
    const arg_from_path = to.path.split('/')[1]
    if (SUPPORT_LOCALES.includes(arg_from_path)) {
      to_locale = arg_from_path
    } else {
      return '/' + i18n.global.locale.value + to.path
    }
  } else if (!SUPPORT_LOCALES.includes(to_locale)) {
    return '/' + i18n.global.locale.value + to.path
  }

  if (!i18n.global.availableLocales.includes(to_locale)) {
    await loadLocaleMessages(i18n, to_locale)
  }

  if (!(to_locale === i18n.global.locale.value)) {
    setI18nLanguage(i18n, to_locale)
  }

  const loggedIn = window.localStorage.getItem('user')
  if (to.meta.requiresAuth  && !loggedIn) {
    return {
      name: 'Login',
      params: { locale: i18n.global.locale.value },
      query: { redirect: to.fullPath }
    }
  }
})

export default router

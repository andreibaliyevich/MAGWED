import { createRouter, createWebHistory } from 'vue-router'
import Root from './Root.vue'
import i18n, {
  SUPPORT_LOCALES,
  loadLocaleMessages,
  setI18nLanguage
} from '@/i18n'

function isAuthenticated(to, from) {
  const isLoggedIn = window.localStorage.getItem('user')
  if (!isLoggedIn) {
    return {
      name: 'Login',
      params: { locale: i18n.global.locale.value },
      query: { redirect: to.fullPath }
    }
  }
}

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
          path: '',
          name: 'BaseAuth',
          component: () => import('@/views/auth/BaseAuthView.vue'),
          beforeEnter: (to, from) => {
            const isLoggedIn = window.localStorage.getItem('user')
            if (isLoggedIn) {
              return {
                name: 'Profile',
                params: { locale: i18n.global.locale.value }
              }
            }
          },
          children: [
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
              path: 'password/reset',
              name: 'PasswordReset',
              component: () => import('@/views/auth/PasswordResetView.vue')
            },
            {
              path: 'password/reset/:uid/:token',
              name: 'PasswordResetConfirm',
              component: () => import('@/views/auth/PasswordResetConfirmView.vue')
            }
          ]
        },
        {
          path: '',
          name: 'BaseAccount',
          component: () => import('@/views/auth/BaseAccountView.vue'),
          beforeEnter: [isAuthenticated],
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
              path: 'password/change',
              name: 'PasswordChange',
              component: () => import('@/views/auth/PasswordChangeView.vue')
            },
            {
              path: 'notifications',
              name: 'Notifications',
              component: () => import('@/views/auth/NotificationsView.vue')
            }
          ]
        },
        {
          path: 'messenger',
          name: 'Messenger',
          component: () => import('@/views/MessengerView.vue'),
          beforeEnter: [isAuthenticated],
        },
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: '404NotFound',
      component: () => import('@/views/404NotFoundView.vue')
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  }
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
})

export default router

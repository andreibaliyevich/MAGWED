import { createRouter, createWebHistory } from 'vue-router'
import i18n, {
  SUPPORT_LOCALES,
  loadLocaleMessages,
  setI18nLanguage
} from '@/i18n'
import Root from './Root.vue'

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
              path: 'social-links',
              name: 'SocialLinks',
              component: () => import('@/views/auth/SocialLinksView.vue')
            },
            {
              path: 'portfolio',
              name: 'Portfolio',
              component: () => import('@/views/auth/portfolio/PortfolioView.vue')
            },
            {
              path: 'portfolio/albums',
              name: 'PortfolioAlbums',
              component: () => import('@/views/auth/portfolio/AlbumsView.vue')
            },
            {
              path: 'portfolio/photos',
              name: 'PortfolioPhotos',
              component: () => import('@/views/auth/portfolio/PhotosView.vue')
            },
            {
              path: 'portfolio/album/:uuid',
              name: 'PortfolioAlbum',
              component: () => import('@/views/auth/portfolio/AlbumView.vue')
            },
            {
              path: 'password/change',
              name: 'PasswordChange',
              component: () => import('@/views/auth/PasswordChangeView.vue')
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
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach(async (to, from) => {
  let paramsLocale = to.params.locale

  if (!paramsLocale) {
    const arg_from_path = to.path.split('/')[1]
    if (SUPPORT_LOCALES.includes(arg_from_path)) {
      paramsLocale = arg_from_path
    } else {
      return '/' + i18n.global.locale.value + to.path
    }
  } else if (!SUPPORT_LOCALES.includes(paramsLocale)) {
    return '/' + i18n.global.locale.value + to.path
  }

  if (!i18n.global.availableLocales.includes(paramsLocale)) {
    await loadLocaleMessages(i18n, paramsLocale)
  }

  if (paramsLocale !== i18n.global.locale.value) {
    setI18nLanguage(i18n, paramsLocale)
  }
})

export default router

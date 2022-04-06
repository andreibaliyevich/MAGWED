import { createRouter, createWebHistory } from 'vue-router'
import Root from './Root.vue'
import i18n from '@/i18n.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: i18n.global.locale.value
    },
    {
      path: '/:lang',
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

router.beforeEach((to, from) => {
  if (!to.params.lang) {
    return { name: 'home', params: { lang: i18n.global.locale.value }};
  } else if (!i18n.global.availableLocales.includes(to.params.lang)) {
    return '/' + i18n.global.locale.value + to.path;
  } else if (!(to.params.lang === from.params.lang)) {
    document.querySelector('html').setAttribute('lang', to.params.lang);
    i18n.global.locale.value = to.params.lang;
  }
})

export default router

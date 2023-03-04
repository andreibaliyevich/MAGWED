import axios from 'axios'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useUserStore } from '@/stores/user.js'

export function useLogout() {
  const router = useRouter()
  const { locale } = useI18n({ useScope: 'global' })
  const userStore = useUserStore()

  const logout = () => {
    axios.post('/accounts/auth/logout/')
    .then(() => {
      window.localStorage.removeItem('user')
      userStore.$reset()
      router.push({
        name: 'Home',
        params: { locale: locale.value }
      })
    })
  }

  return { logout }
}

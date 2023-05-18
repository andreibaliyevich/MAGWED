import { ref, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

export function useOptionsOfRoleTypes() {
  const { t, locale } = useI18n({ useScope: 'global' })
  const roleTypeOptions = ref([])

  const setRoleTypeOptions = () => {
    roleTypeOptions.value = [
      { value: 1, text: t('roles.1') },
      { value: 2, text: t('roles.2') },
      { value: 3, text: t('roles.3') },
      { value: 4, text: t('roles.4') },
      { value: 5, text: t('roles.5') },
      { value: 6, text: t('roles.6') },
      { value: 7, text: t('roles.7') },
      { value: 8, text: t('roles.8') },
      { value: 9, text: t('roles.9') },
      { value: 10, text: t('roles.10') },
      { value: 11, text: t('roles.11') }
    ]
  }

  watch(locale, () => {
    setRoleTypeOptions()
  })

  onMounted(() => {
    setRoleTypeOptions()
  })

  return { roleTypeOptions }
}

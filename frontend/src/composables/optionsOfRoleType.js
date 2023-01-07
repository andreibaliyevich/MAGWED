import { ref, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

export function useOptionsOfRoleType() {
  const { t, locale } = useI18n({ useScope: 'global' })
  const roleTypeOptions = ref([])

  const setRoleTypeOptions = () => {
    roleTypeOptions.value = [
      { value: 1, text: t('roles.photographer') },
      { value: 2, text: t('roles.videographer') },
      { value: 3, text: t('roles.leading') },
      { value: 4, text: t('roles.musician') },
      { value: 5, text: t('roles.dj') },
      { value: 6, text: t('roles.agency') },
      { value: 7, text: t('roles.salon') },
      { value: 8, text: t('roles.confectionery') },
      { value: 9, text: t('roles.decorator') },
      { value: 10, text: t('roles.visagiste') },
      { value: 11, text: t('roles.hairdresser') }
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

import { useI18n } from 'vue-i18n'
import { ref, watch, onMounted } from 'vue'

export function useOptionsOfRoleTypes(translationKey) {
  const { t, locale } = useI18n({ useScope: 'global' })
  const roleTypeOptions = ref([])

  const setRoleTypeOptions = () => {
    roleTypeOptions.value = [
      { value: 1, text: t(`${translationKey}.1`) },
      { value: 2, text: t(`${translationKey}.2`) },
      { value: 3, text: t(`${translationKey}.3`) },
      { value: 4, text: t(`${translationKey}.4`) },
      { value: 5, text: t(`${translationKey}.5`) },
      { value: 6, text: t(`${translationKey}.6`) },
      { value: 7, text: t(`${translationKey}.7`) },
      { value: 8, text: t(`${translationKey}.8`) },
      { value: 9, text: t(`${translationKey}.9`) },
      { value: 10, text: t(`${translationKey}.10`) },
      { value: 11, text: t(`${translationKey}.11`) }
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

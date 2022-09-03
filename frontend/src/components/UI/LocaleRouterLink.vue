<script setup>
import { RouterLink } from 'vue-router'
</script>

<script>
export default {
  name: 'LocaleRouterLink',
  props: {
    toName: {
      type: String,
      required: true
    },
    toParams: {
      type: Object,
      required: false
    }
  }
}
</script>

<template>
  <RouterLink
    :to="{
      name: `${ toName }`,
      params: {
        locale: `${ $i18n.locale }`,
        ...toParams
      }
    }"
  >
    <slot></slot>
  </RouterLink>
</template>

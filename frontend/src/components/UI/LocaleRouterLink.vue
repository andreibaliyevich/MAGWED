<script setup>
import { RouterLink } from 'vue-router'
</script>

<script>
export default {
  name: 'LocaleRouterLink',
  inheritAttrs: false,
  props: {
    toName: {
      type: String,
      required: true
    },
    toParams: {
      type: Object,
      default: {}
    }
  }
}
</script>

<template>
  <div class="locale-router-link">
    <RouterLink
      :to="{
        name: toName,
        params: {
          locale: $i18n.locale,
          ...toParams
        }
      }"
      v-bind="$attrs"
    >
      <slot></slot>
    </RouterLink>
  </div>
</template>

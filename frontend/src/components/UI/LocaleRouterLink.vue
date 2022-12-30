<script setup>
import { RouterLink } from 'vue-router'
</script>

<script>
export default {
  name: 'LocaleRouterLink',
  inheritAttrs: false,
  props: {
    routeName: {
      type: String,
      required: true
    },
    routeParams: {
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
        name: routeName,
        params: {
          locale: $i18n.locale,
          ...routeParams
        }
      }"
      v-bind="$attrs"
    >
      <slot></slot>
    </RouterLink>
  </div>
</template>

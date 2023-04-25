<script>
import { RouterLink } from 'vue-router'

export default {
  name: 'LocaleRouterLink',
  inheritAttrs: false,
  components: {
    RouterLink
  },
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

<style scoped>
.locale-router-link {
  display: inline;
}
</style>

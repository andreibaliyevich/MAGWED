<script>
export default {
  name: 'UserAvatar',
  inheritAttrs: false,
  props: {
    src: String,
    width: {
      type: Number,
      required: true
    },
    height: {
      type: Number,
      required: true
    },
    buttonClass: {
      type: String,
      default: 'rounded-circle'
    }
  }
}
</script>

<template>
  <div class="user-avatar">
    <img
      v-if="src"
      :src="src"
      :width="width"
      :height="height"
      :class="buttonClass"
      v-bind="$attrs"
    >
    <img
      v-else
      src="/user-avatar.jpg"
      :width="width"
      :height="height"
      :class="buttonClass"
      v-bind="$attrs"
    >
  </div>
</template>

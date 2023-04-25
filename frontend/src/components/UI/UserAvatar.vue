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
    imgClass: {
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
      v-bind="$attrs"
      :class="imgClass"
    >
    <img
      v-else
      src="/user-avatar.jpg"
      :width="width"
      :height="height"
      v-bind="$attrs"
      :class="imgClass"
    >
  </div>
</template>

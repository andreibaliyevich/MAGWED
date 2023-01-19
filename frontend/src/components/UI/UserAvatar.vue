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
      class="rounded-circle"
    >
    <img
      v-else
      src="/user-avatar.jpg"
      :width="width"
      :height="height"
      class="rounded-circle"
    >
  </div>
</template>

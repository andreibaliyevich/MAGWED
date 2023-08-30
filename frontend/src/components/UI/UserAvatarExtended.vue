<script>
export default {
  name: 'UserAvatarExtended',
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
    online: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    statusWidth() {
      return parseInt((this.width / 33) + (116 / 11))
    },
    statusHeight() {
      return parseInt((this.height / 33) + (116 / 11))
    },
    statusMarginRight() {
      return parseInt((this.width * 3 / 22) - (72 / 11))
    },
    statusMarginBottom() {
      return parseInt((this.height * 3 / 22) - (72 / 11))
    }
  }
}
</script>

<template>
  <div class="user-avatar-extended">
    <div class="position-relative">
      <img
        v-if="src"
        :src="src"
        :width="width"
        :height="height"
        v-bind="$attrs"
        class="rounded-circle"
      >
      <img
        v-else
        src="/user-avatar.jpg"
        :width="width"
        :height="height"
        v-bind="$attrs"
        class="rounded-circle"
      >
      <span
        :class="[
          'position-absolute bottom-0 end-0 border border-light border-2 rounded-circle',
          online ? 'bg-success' : 'bg-secondary'
        ]"
        :style="{
          'width': statusWidth + 'px',
          'height': statusHeight + 'px',
          'margin-right': statusMarginRight + 'px',
          'margin-bottom': statusMarginBottom + 'px'
        }"
      >
        <span class="visually-hidden">Online</span>
      </span>
    </div>
  </div>
</template>

<style scoped>
.user-avatar-extended {
  display: inline-block;
}
</style>

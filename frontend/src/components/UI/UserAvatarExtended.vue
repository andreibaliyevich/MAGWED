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
        class="rounded-circle"
      >
      <img
        v-else
        src="/user-avatar.jpg"
        :width="width"
        :height="height"
        class="rounded-circle"
      >
      <span
        v-if="online"
        class="position-absolute top-0 start-100 translate-middle p-1 bg-primary rounded-circle"
      >
        <span class="visually-hidden">Online</span>
      </span>
    </div>
  </div>
</template>

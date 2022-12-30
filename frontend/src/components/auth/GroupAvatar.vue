<script>
export default {
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
  <div class="group-avatar">
    <img
      v-if="src"
      :src="src"
      :width="width"
      :height="height"
      class="rounded-circle"
    >
    <img
      v-else
      src="/group-avatar.jpg"
      :width="width"
      :height="height"
      class="rounded-circle"
    >
  </div>
</template>

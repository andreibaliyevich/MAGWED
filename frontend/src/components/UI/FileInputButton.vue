<script>
export default {
  name: 'FileInputButton',
  inheritAttrs: false,
  props: {
    classButton: {
      type: String,
      default: ''
    }
  },
  methods: {
    changeInput(event) {
      if (event.target.files.length > 0) {
        this.$emit('updateFile', event.target.files)
      }
    }
  }
}
</script>

<template>
  <input
    ref="fileInput"
    @change="changeInput"
    v-bind="$attrs"
    type="file"
    class="visually-hidden"
  >
  <button
    @click="$refs.fileInput.click()"
    type="button"
    :class="classButton"
  >
    <slot></slot>
  </button>
</template>

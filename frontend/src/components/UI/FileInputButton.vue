<script>
export default {
  name: 'FileInputButton',
  inheritAttrs: false,
  props: {
    buttonClass: {
      type: String,
      default: 'btn'
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
  <div class="file-input-button">
    <input
      ref="fileInput"
      @change="changeInput"
      v-bind="$attrs"
      class="visually-hidden"
      type="file"
    >
    <button
      @click="$refs.fileInput.click()"
      :class="buttonClass"
      type="button"
    >
      <slot></slot>
    </button>
  </div>
</template>

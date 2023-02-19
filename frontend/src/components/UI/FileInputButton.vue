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
      this.$emit('selectedFiles', event.target.files)
      event.target.value = null
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

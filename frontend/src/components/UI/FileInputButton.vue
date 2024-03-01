<script>
export default {
  name: 'FileInputButton',
  inheritAttrs: false,
  props: {
    accept: {
      type: String,
      default: ''
    }
  },
  methods: {
    changeInput(event) {
      const filelist = [...event.target.files]
      this.$emit('selectedFiles', filelist)
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
      type="file"
      :accept="accept"
      class="visually-hidden"
    >
    <v-btn
      @click="$refs.fileInput.click()"
      v-bind="$attrs"
    >
      <slot></slot>
    </v-btn>
  </div>
</template>

<style scoped>
.visually-hidden {
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  white-space: nowrap !important;
  border: 0 !important;
}
</style>

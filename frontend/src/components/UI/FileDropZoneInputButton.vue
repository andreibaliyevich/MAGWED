<script>
export default {
  name: 'FileDropZoneInputButton',
  inheritAttrs: false,
  props: {
    buttonClass: {
      type: String,
      default: 'btn'
    }
  },
  methods: {
    dropHandler(event) {
      const filelist = [...event.dataTransfer.files]
      this.$emit('selectedFiles', filelist)
      this.$refs.dropArea.classList.remove('drop-area-over')
    },
    changeInput(event) {
      const filelist = [...event.target.files]
      this.$emit('selectedFiles', filelist)
      event.target.value = null
    }
  }
}
</script>

<template>
  <div class="file-drop-zone-input-button">
    <div
      ref="dropArea"
      @dragover.prevent="$refs.dropArea.classList.add('drop-area-over')"
      @dragleave.prevent="$refs.dropArea.classList.remove('drop-area-over')"
      @drop.prevent="dropHandler"
      class="d-flex justify-content-center align-items-center rounded-4"
    >
      <div class="text-center">
        <i class="fa-solid fa-cloud-arrow-up fa-2xl"></i>
        <slot></slot>
        <input
          ref="fileInput"
          @change="changeInput"
          type="file"
          v-bind="$attrs"
          class="visually-hidden"
        >
        <button
          @click="$refs.fileInput.click()"
          type="button"
          :class="buttonClass"
        >
          <slot name="button"></slot>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.d-flex.justify-content-center.align-items-center {
  width: 100%;
  height: 220px;
  background-color: #f8f9fa;
  border-width: 3px;
  border-style: dashed;
  border-color: #adb5bd;
}
.drop-area-over {
  background-color: #e2e3e5 !important;
  border-style: solid !important;
  border-color: #e72a26 !important;
}
</style>

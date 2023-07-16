<script>
export default {
  name: 'BaseTextarea',
  inheritAttrs: false,
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    id: {
      type: String,
      required: true
    },
    label: {
      type: String,
      default: ''
    },
    maxHeight: {
      type: Number,
      default: 150
    },
    errors: {
      type: Array,
      default: []
    }
  },
  methods: {
    updateTextareaStyles() {
      const { style } = this.$refs.modelTextarea
      style.height = style.minHeight = 'auto'
      style.minHeight = `${
        Math.min(this.$refs.modelTextarea.scrollHeight + 4,
          parseInt(this.maxHeight))
      }px`
      style.height = `${ this.$refs.modelTextarea.scrollHeight + 4 }px`
    }
  },
  watch: {
    modelValue(newValue) {
      this.updateTextareaStyles()
    }
  },
  mounted() {
    this.updateTextareaStyles()
  }
}
</script>

<template>
  <div class="base-textarea">
    <div class="form-floating">
      <textarea
        ref="modelTextarea"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        rows="1"
        :placeholder="label"
        :id="id"
        v-bind="$attrs"
        :class="['form-control', { 'is-invalid': errors.length }]"
        :style="{ 'max-height': maxHeight + 'px' }"
        :aria-invalid="errors.length ? true : null"
        :aria-describedby="errors.length ? `${ id }_errors` : null"
      ><i class="fa-solid fa-paper-plane"></i></textarea>
      <label
        v-if="label"
        :for="id"
      >
        {{ label }}
      </label>
      <div
        v-if="errors.length"
        :id="`${ id }_errors`"
        class="invalid-feedback"
        aria-live="assertive"
      >
        <div v-for="error in errors">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
textarea {
  resize: vertical;
}
textarea::-webkit-scrollbar {
  width: 0.2em;
}
textarea::-webkit-scrollbar-track {
  background-color: #f5f5f5;
}
textarea::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 1em;
}
textarea::-webkit-scrollbar-thumb:hover {
  background-color: #e72a26;
}
</style>

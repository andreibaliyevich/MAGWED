<script setup>
import { ref, nextTick, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  loadingStatus: {
    type: Boolean,
    required: true
  },
  autofocus: {
    type: Boolean,
    default: false
  },
  id: {
    type: String,
    required: true
  },
  placeholder: {
    type: String,
    default: ''
  },
  errors: {
    type: Array,
    default: []
  }
})

const valueTextarea = ref(null)

const updateTextareaHeight = () => {
  valueTextarea.value.style.height = 'auto'
  valueTextarea.value.style.height = `${valueTextarea.value.scrollHeight}px`
}

watch(() => props.modelValue, (newValue) => {
  nextTick(() => {
    updateTextareaHeight()
  })
})

onMounted(() => {
  updateTextareaHeight()
  if (props.autofocus) {
    valueTextarea.value.focus()
  }
})
</script>

<template>
  <div class="submit-content">
    <div
      :class="[
        'd-flex align-items-center border rounded w-100',
        { 'border-danger': errors.length }
      ]"
    >
      <textarea
        ref="valueTextarea"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :placeholder="placeholder"
        :id="id"
        name="content"
        rows="1"
        :class="[
          'form-control border-0',
          { 'is-invalid': errors.length }
        ]"
        :aria-invalid="errors.length ? true : null"
        :aria-describedby="errors.length ? `${id}_errors` : null"
      ></textarea>
      <button
        v-if="loadingStatus"
        type="button"
        class="btn btn-link"
        disabled
      >
        <span
          class="spinner-border spinner-border-sm"
          role="status"
        ></span>
      </button>
      <button
        v-else
        type="submit"
        class="btn btn-link"
        :disabled="!modelValue"
      >
        <i class="fa-solid fa-paper-plane"></i>
      </button>
    </div>
    <div
      v-if="errors.length"
      :id="`${id}_errors`"
      class="text-danger"
      aria-live="assertive"
    >
      <small v-for="error in errors">
        {{ error }}
      </small>
    </div>
  </div>
</template>

<style scoped>
.d-flex.align-items-center.border.rounded.w-100:hover,
.d-flex.align-items-center.border.rounded.w-100:focus-within {
  border-color: #e72a26 !important;
}
textarea {
  resize: none;
}
</style>

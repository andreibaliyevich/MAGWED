<script>
export default {
  name: 'BaseInput',
  inheritAttrs: false,
  props: {
    modelValue: {
      type: [String, Number],
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
    errors: {
      type: Object,
      default: null
    }
  }
}
</script>

<template>
  <div class="form-floating">
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :id="id"
      :placeholder="label"
      v-bind="$attrs"
      :class="['form-control', { 'is-invalid': errors }]"
      :aria-invalid="errors ? true : null"
      :aria-describedby="errors ? `${id}-error` : null"
    >
    <label
      v-if="label"
      :for="id"
    >
      {{ label }}
    </label>
    <div
      v-if="errors"
      v-for="error in errors"
      :id="`${id}-errors`"
      class="invalid-feedback"
      aria-live="assertive"
    >
      {{ error }}
    </div>
  </div>
</template>

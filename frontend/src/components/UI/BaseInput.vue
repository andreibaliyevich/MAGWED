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
      type: Array,
      default: []
    }
  }
}
</script>

<template>
  <div class="base-input">
    <div class="form-floating">
      <input
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :placeholder="label"
        :id="id"
        v-bind="$attrs"
        :class="['form-control', { 'is-invalid': errors.length }]"
        :aria-invalid="errors.length ? true : null"
        :aria-describedby="errors.length ? `${id}-errors` : null"
      >
      <label
        v-if="label"
        :for="id"
      >
        {{ label }}
      </label>
      <div
        v-if="errors.length"
        :id="`${id}-errors`"
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

<script>
export default {
  name: 'BaseInput',
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    id: {
      type: String,
      default: ''
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
  <div
    v-if="errors"
    class="form-floating"
  >
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :id="id"
      :placeholder="label"
      v-bind="$attrs"
      class="form-control is-invalid"
    >
    <label v-if="label" :for="id">{{ label }}</label>
    <div
      v-for="error in errors"
      class="invalid-feedback"
    >
      {{ error }}
    </div>
  </div>
  <div
    v-else
    class="form-floating"
  >
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :id="id"
      :placeholder="label"
      v-bind="$attrs"
      class="form-control"
    >
    <label v-if="label" :for="id">{{ label }}</label>
  </div>
</template>

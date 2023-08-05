<script>
export default {
  name: 'BaseSelect',
  inheritAttrs: false,
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    options: {
      type: Array,
      required: true
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
  <div class="base-select">
    <div class="form-floating">
      <select
        :value="modelValue"
        @change="$emit('update:modelValue', $event.target.value)"
        :id="id"
        v-bind="$attrs"
        :class="['form-select', { 'is-invalid': errors.length }]"
        :aria-invalid="errors.length ? true : null"
        :aria-describedby="errors.length ? `${id}_errors` : null"
      >
        <option disabled value="">{{ $t('form_help.select_option') }}</option>
        <option
          v-for="option in options"
          :value="option.value"
          :key="option.value"
          :selected="option.value === modelValue"
        >
          {{ option.text }}
        </option>
      </select>
      <label
        v-if="label"
        :for="id"
      >
        {{ label }}
      </label>
      <div
        v-if="errors.length"
        :id="`${id}_errors`"
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

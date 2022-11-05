<script>
export default {
  name: 'BaseSelect',
  inheritAttrs: false,
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    id: {
      type: String,
      default: ''
    },
    options: {
      type: Array,
      required: true
    },
    label: {
      type: String,
      default: ''
    }
  }
}
</script>

<template>
  <div class="form-floating">
    <select
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      :id="id"
      v-bind="$attrs"
      class="form-select"
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
  </div>
</template>

<script>
export default {
  name: 'CheckboxMultipleSelect',
  inheritAttrs: false,
  props: {
    modelValue: {
      type: Array,
      default: []
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
  },
  methods: {
    updateModelValue(value) {
      let newModelValue = []
      if (this.modelValue.includes(value)) {
        newModelValue = this.modelValue.filter(element => element !== value)
      } else {
        newModelValue = [...this.modelValue, value]
      }
      this.$emit('update:modelValue', newModelValue)
    }
  }
}
</script>

<template>
  <div class="checkbox-multiple-select">
    <label
      v-if="label"
      :for="id"
      class="fw-bold"
    >
      {{ label }}
    </label>
    <div
      :id="id"
      v-bind="$attrs"
      class="overflow-auto p-1"
      :aria-invalid="errors.length ? true : null"
      :aria-describedby="errors.length ? `${id}-errors` : null"
      style="max-height: 135px"
    >
      <div
        v-for="option in options"
        :key="option.value"
        class="form-check"
      >
        <input
          :value="option.value"
          :checked="modelValue.includes(option.value)"
          @change="updateModelValue(option.value)"
          :id="option.value"
          class="form-check-input"
          type="checkbox"
        >
        <label
          class="form-check-label"
          :for="option.value"
        >
          {{ option.text }}
        </label>
      </div>
    </div>
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
</template>

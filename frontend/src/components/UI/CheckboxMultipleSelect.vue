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
      class="fw-bold mb-2"
    >
      {{ label }}
    </label>
    <div
      :id="id"
      v-bind="$attrs"
      class="overflow-auto p-1"
      style="max-height: 135px"
      :aria-invalid="errors.length ? true : null"
      :aria-describedby="errors.length ? `${id}_errors` : null"
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
          type="checkbox"
          :id="option.value"
          class="form-check-input"
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
      :id="`${id}_errors`"
      class="invalid-feedback"
      aria-live="assertive"
    >
      <div
        v-for="(error, index) in errors"
        :key="`${id}_error_${index}`"
      >
        {{ error }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.overflow-auto.p-1::-webkit-scrollbar {
  width: 0.2em;
}
.overflow-auto.p-1::-webkit-scrollbar-track {
  background-color: #f5f5f5;
}
.overflow-auto.p-1::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 1em;
}
.overflow-auto.p-1::-webkit-scrollbar-thumb:hover {
  background-color: #e72a26;
}
</style>

<script>
export default {
  name: 'NumberRangeInput',
  inheritAttrs: false,
  props: {
    minValue: {
      type: Number,
      default: 0
    },
    maxValue: {
      type: Number,
      default: 100
    },
    min: {
      type: Number,
      default: 0
    },
    max: {
      type: Number,
      default: 100
    },
    step: {
      type: Number,
      default: 1
    },
    id: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    label: {
      type: String,
      default: ''
    },
    minLabel: {
      type: String,
      default: 'min'
    },
    maxLabel: {
      type: String,
      default: 'max'
    },
    errors: {
      type: Array,
      default: []
    }
  }
}
</script>

<template>
  <div class="number-range-input">
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
      class="row p-1 g-1"
      :aria-invalid="errors.length ? true : null"
      :aria-describedby="errors.length ? `${ id }_errors` : null"
    >
      <div class="col-6">
        <div class="input-group input-group-sm">
          <span class="input-group-text">{{ minLabel }}</span>
          <input
            :value="minValue"
            @input="$emit('update:minValue', parseFloat($event.target.value))"
            type="number"
            :min="min"
            :max="maxValue"
            :step="step"
            :id="`${ id }_min`"
            :name="`${ name }_min`"
            class="form-control"
          >
        </div>
      </div>
      <div class="col-6">
        <div class="input-group input-group-sm">
          <span class="input-group-text">{{ maxLabel }}</span>
          <input
            :value="maxValue"
            @input="$emit('update:maxValue', parseFloat($event.target.value))"
            type="number"
            :min="minValue"
            :max="max"
            :step="step"
            :id="`${ id }_max`"
            :name="`${ name }_max`"
            class="form-control"
          >
        </div>
      </div>
    </div>
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
</template>

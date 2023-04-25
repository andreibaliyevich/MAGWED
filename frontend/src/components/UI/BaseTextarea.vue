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
    errors: {
      type: Array,
      default: []
    }
  }
}
</script>

<template>
  <div class="base-textarea">
    <div class="form-floating">
      <textarea
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :placeholder="label"
        :id="id"
        v-bind="$attrs"
        :class="['form-control', { 'is-invalid': errors.length }]"
        style="height: 100px"
        :aria-invalid="errors.length ? true : null"
        :aria-describedby="errors.length ? `${id}-errors` : null"
      ></textarea>
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

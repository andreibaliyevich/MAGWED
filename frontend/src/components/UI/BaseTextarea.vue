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
    }
  }
}
</script>

<template>
  <div class="form-floating">
    <textarea
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :id="id"
      :placeholder="label"
      v-bind="$attrs"
      class="form-control"
      style="height: 100px"
    ></textarea>
    <label
      v-if="label"
      :for="id"
    >
      {{ label }}
    </label>
  </div>
</template>

<script>
export default {
  name: 'SubmitButton',
  inheritAttrs: false,
  props: {
    loadingStatus: {
      type: Boolean,
      required: true
    },
    buttonClass: {
      type: String,
      default: 'btn'
    }
  }
}
</script>

<template>
  <div class="submit-button">
    <button
      v-if="loadingStatus"
      :class="buttonClass"
      type="submit"
      disabled
    >
      <span
        class="spinner-border spinner-border-sm"
        role="status"
        aria-hidden="true"
      ></span>
      {{ $t('btn.loading') }}
    </button>
    <button
      v-else
      :class="buttonClass"
      v-bind="$attrs"
      type="submit"
    >
      <slot></slot>
    </button>
  </div>
</template>

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
      type="button"
      :class="buttonClass"
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
      type="submit"
      v-bind="$attrs"
      :class="buttonClass"
    >
      <slot></slot>
    </button>
  </div>
</template>

<script>
export default {
  name: 'LoadingIndicator',
  inheritAttrs: false,
  props: {
    actionInfo : {
      type: String,
      default: ''
    }
  }
}
</script>

<template>
  <div class="action-processing-indicator">
    <div
      v-if="actionInfo"
      v-bind="$attrs"
      class="d-flex align-items-center p-5"
    >
      <strong>{{ actionInfo }}</strong>
      <div
        class="spinner-border text-dark ms-auto"
        role="status"
        aria-hidden="true"
      ></div>
    </div>
    <div
      v-else
      v-bind="$attrs"
      class="d-flex justify-content-center p-5"
    >
      <div
        class="spinner-grow text-dark"
        role="status"
      >
        <span class="visually-hidden">
          Loading...
        </span>
      </div>
    </div>
  </div>
</template>

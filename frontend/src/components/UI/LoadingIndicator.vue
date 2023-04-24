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
      class="d-flex align-items-center p-5"
      v-bind="$attrs"
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
      class="d-flex justify-content-center p-5"
      v-bind="$attrs"
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

<script>
export default {
  name: 'PageLoadingIndicator'
}
</script>

<template>
  <div class="d-flex justify-content-center p-5">
    <div
      class="spinner-grow text-dark"
      role="status"
    >
      <span class="visually-hidden">
        Loading...
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CheckboxSearchMultipleSelect',
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
  data() {
    return {
      searchQuery: ''
    }
  },
  computed: {
    searchOptions() {
      return this.options.filter((element) => {
        return element.text.toLowerCase().includes(
          this.searchQuery.toLowerCase())
      })
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
  <div class="checkbox-search-multiple-select">
    <label
      v-if="label"
      :for="id"
      class="fw-bold"
    >
      {{ label }}
    </label>
    <div class="d-flex align-items-center border rounded w-100 m-1 px-2">
      <input
        ref="searchInput"
        v-model="searchQuery"
        class="form-control border-0 p-1"
        type="text"
        autocomplete="off"
        :placeholder="$t('search.search2')"
      >
      <span class="text-secondary">
        <i class="fa-solid fa-magnifying-glass"></i>
      </span>
    </div>
    <div
      :id="id"
      v-bind="$attrs"
      class="overflow-auto p-1"
      style="max-height: 135px"
      :aria-invalid="errors.length ? true : null"
      :aria-describedby="errors.length ? `${id}-errors` : null"
    >
      <div
        v-for="option in searchOptions"
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

<style scoped>
.d-flex.align-items-center.border.rounded:hover,
.d-flex.align-items-center.border.rounded:focus-within {
  border-color: #e72a26 !important;
}
</style>

<script>
export default {
  name: 'SearchListInputMultipleSelect',
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
      isActive: false,
      searchQuery: ''
    }
  },
  computed: {
    modelValueDetail() {
      return this.options.filter((element) => {
        return this.modelValue.includes(element.value)
      })
    },
    searchOptions() {
      return this.options.filter((element) => {
        return element.text.toLowerCase().includes(
          this.searchQuery.toLowerCase())
      })
    }
  },
  methods: {
    clickInput() {
      this.$refs.searchInput.focus()
      this.isActive = true
    },
    clickArrow() {
      this.isActive = !this.isActive
      if (this.isActive) {
        this.$refs.searchInput.focus()
      }
    },
    updateModelValue(value) {
      let newModelValue = []
      if (this.modelValue.includes(value)) {
        newModelValue = this.modelValue.filter(element => element !== value)
      } else {
        newModelValue = [...this.modelValue, value]
      }
      this.$emit('update:modelValue', newModelValue)
      this.$refs.searchInput.focus()
    },
    deleteModelValue(value) {
      let newModelValue = []
      newModelValue = this.modelValue.filter(element => element !== value)
      this.$emit('update:modelValue', newModelValue)
    },
    clickOutside(event) {
      if (!event.composedPath().includes(this.$refs.divSelect)) {
        this.isActive = false
        this.searchQuery = ''
      }
    }
  },
  mounted() {
    window.addEventListener('click', this.clickOutside)
  },
  unmounted() {
    window.removeEventListener('click', this.clickOutside)
  }
}
</script>

<template>
  <div class="search-list-input-multiple-select">
    <label
      v-if="label"
      :for="id"
    >
      {{ label }}
    </label>
    <div
      ref="divSelect"
      :id="id"
      v-bind="$attrs"
      class="position-relative"
      :aria-invalid="errors.length ? true : null"
      :aria-describedby="errors.length ? `${id}_errors` : null"
    >
      <div
        :class="[
          'd-flex align-items-stretch border rounded',
          {
            'active': isActive,
            'is-invalid': errors.length
          }
        ]"
      >
        <div
          @click="clickInput()"
          class="flex-grow-1"
        >
          <span
            v-for="modelValueSingle in modelValueDetail"
            :key="modelValueSingle.value"
            class="badge text-bg-light fw-normal m-1"
          >
            <div class="d-flex align-items-center">
              {{ modelValueSingle.text }}
              <button
                @click="deleteModelValue(modelValueSingle.value)"
                type="button"
                class="btn-close ms-1"
                aria-label="Close"
              ></button>
            </div>
          </span>
          <input
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            autocomplete="off"
            class="border-0 m-1"
          >
        </div>
        <div
          @click="clickArrow()"
          class="d-flex align-items-center"
        >
          <i
            v-if="isActive"
            class="fa-solid fa-angle-up me-1"
          ></i>
          <i
            v-else
            class="fa-solid fa-angle-down me-1"
          ></i>
        </div>
      </div>
      <div
        :class="[
          'position-absolute border rounded shadow',
          { 'show': isActive }
        ]"
      >
        <ul class="list-group list-group-flush overflow-auto">
          <li
            v-if="searchOptions.length > 0"
            v-for="option in searchOptions"
            :key="option.value"
            @click="updateModelValue(option.value)"
            :class="[
              'list-group-item py-1',
              { 'list-group-item-primary': modelValue.includes(option.value) }
            ]"
          >
            <div class="d-flex align-items-center justify-content-between">
              {{ option.text }}
              <i
                v-if="modelValue.includes(option.value)"
                class="fa-solid fa-check"
              ></i>
            </div>
          </li>
          <li
            v-else
            class="list-group-item py-3"
          >
            {{ $t('form_help.no_options_available') }}
          </li>
        </ul>
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
.d-flex.align-items-stretch:hover {
  border-color: #e72a26 !important;
  cursor: text;
}
.d-flex.align-items-stretch.active {
  border-color: #e72a26 !important;
}
.badge.text-bg-light:hover {
  cursor: default;
}
.btn-close:focus {
  box-shadow: none;
}
input:focus-visible {
  border: none;
  outline: none;
}

.d-flex.align-items-stretch > .d-flex.align-items-center:hover {
  cursor: pointer;
}

.position-absolute.border.rounded.shadow {
  width: 100%;
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  z-index: 1000;
  transition: all 0.3s;
  -webkit-transition: all 0.3s;
  -moz-transition: all 0.3s;
  -ms-transition: all 0.3s;
  -o-transition: all 0.3s;
}
.position-absolute.border.rounded.shadow.show {
  max-height: 230px;
  opacity: 1;
}

.list-group.list-group-flush.overflow-auto {
  max-height: 230px;
}
.list-group.list-group-flush.overflow-auto::-webkit-scrollbar {
  width: 0.3em;
}
.list-group.list-group-flush.overflow-auto::-webkit-scrollbar-track {
  background-color: #f5f5f5;
}
.list-group.list-group-flush.overflow-auto::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 1em;
}
.list-group.list-group-flush.overflow-auto::-webkit-scrollbar-thumb:hover {
  background-color: #e72a26;
}

.list-group-item.py-1:hover {
  color: #e72a26 !important;
  cursor: pointer;
}

.d-flex.align-items-stretch.is-invalid {
  border-color: #dc3545 !important;
}
.position-relative ~ .invalid-feedback {
  display: block;
  width: 100%;
  margin-top: 0.25rem;
  font-size: 0.875em;
  color: #dc3545;
}
</style>

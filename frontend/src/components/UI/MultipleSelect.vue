<script>
export default {
  name: 'MultipleSelect',
  inheritAttrs: false,
  props: {
    modelValue: {
      type: Array,
      default: []
    },
    id: {
      type: String,
      default: ''
    },
    options: {
      type: Array,
      required: true
    },
    label: {
      type: String,
      default: ''
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
      this.$refs.input.focus()
      this.isActive = true
    },
    clickArrow() {
      this.isActive = !this.isActive
      if (this.isActive) {
        this.$refs.input.focus()
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
      this.$refs.input.focus()
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
  >
    <div
      :class="[
        'd-flex align-items-stretch border rounded',
        { 'active': isActive }
      ]"
    >
      <div
        @click="clickInput"
        class="flex-grow-1"
      >
        <span
          v-for="modelValueSingle in modelValueDetail"
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
          ref="input"
          v-model="searchQuery"
          type="text"
          autocomplete="off"
          class="border-0 m-1"
        >
      </div>
      <div
        @click="clickArrow"
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
        'position-absolute overflow-auto border rounded shadow',
        {'show': isActive}
      ]"
    >
      <ul class="list-group list-group-flush">
        <li
          v-if="searchOptions.length > 0"
          v-for="option in searchOptions"
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
</template>

<style scoped>
* {
  scrollbar-color: #c0c0c0;
  scrollbar-width: thin;
}
::-webkit-scrollbar {
  width: 0.3em;
  height: 0.3em;
  background-color: #f5f5f5;
}
::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 3em;
}
::-webkit-scrollbar-thumb:hover {
  background-color: #808080;
}

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
.position-absolute.overflow-auto {
  display: none;
  margin: 0;
  width: 100%;
  max-height: 230px;
  z-index: 1000;
}
.position-absolute.overflow-auto.show {
  display: block;
}
.list-group-item.py-1:hover {
  color: #e72a26 !important;
  cursor: pointer;
}
</style>

<script>
export default {
  name: 'ListInput',
  inheritAttrs: false,
  props: {
    modelValue: {
      type: Array,
      default: []
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
      valueInput: ''
    }
  },
  methods: {
    clickInput() {
      this.$refs.listInput.focus()
      this.isActive = true
    },
    addValueInput() {
      if (this.valueInput) {
        let newModelValue = [...this.modelValue]
        newModelValue.push(this.valueInput)
        this.$emit('update:modelValue', newModelValue)
        this.valueInput = ''
        this.$refs.listInput.focus()
      }
    },
    deleteModelValue(value) {
      let newModelValue = []
      newModelValue = this.modelValue.filter(element => element !== value)
      this.$emit('update:modelValue', newModelValue)
    },
    clickOutside(event) {
      if (!event.composedPath().includes(this.$refs.divInput)) {
        this.isActive = false
        this.valueInput = ''
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
  <div class="list-input">
    <label
      v-if="label"
      :for="id"
    >
      {{ label }}
    </label>
    <div
      ref="divInput"
      :id="id"
      v-bind="$attrs"
      class="position-relative"
      :aria-invalid="errors.length ? true : null"
      :aria-describedby="errors.length ? `${id}-errors` : null"
    >
      <div
        :class="[
          'd-flex align-items-stretch border rounded',
          { 'active': isActive },
          { 'is-invalid': errors.length }
        ]"
      >
        <div
          @click="clickInput()"
          class="flex-grow-1"
        >
          <span
            v-for="value in modelValue"
            :key="value"
            class="badge text-bg-light fw-normal m-1"
          >
            <div class="d-flex align-items-center">
              {{ value }}
              <button
                @click="deleteModelValue(value)"
                type="button"
                class="btn-close ms-1"
                aria-label="Close"
              ></button>
            </div>
          </span>
          <input
            ref="listInput"
            v-model="valueInput"
            @keyup.ctrl.enter="addValueInput()"
            type="text"
            autocomplete="off"
            class="border-0 m-1"
          >
        </div>
        <div
          v-if="valueInput"
          @click="addValueInput()"
          class="d-flex align-items-center"
        >
        <i class="fa-solid fa-plus me-1"></i>
        </div>
      </div>
    </div>
    <small>{{ $t('form_help.list_input') }}</small>
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

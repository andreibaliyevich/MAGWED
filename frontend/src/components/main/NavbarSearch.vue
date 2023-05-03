<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const searchLoading = ref(false)
const searchQuery = ref('')
const searchedItems = ref([])

const searchModal = ref(null)
const searchInput = ref(null)

const searchItems = async () => {
  searchLoading.value = true
  console.log(searchQuery.value)
  searchLoading.value = false
}

onMounted(() => {
  searchModal.value.addEventListener('shown.bs.modal', () => {
    searchInput.value.focus()
  })
})
</script>

<template>
  <div class="navbar-search">
    <a
      href="#"
      class="text-decoration-none link-secondary"
      data-bs-toggle="modal"
      data-bs-target="#searchModal"
    >
      <i class="fa-solid fa-magnifying-glass"></i>
    </a>

    <Teleport to="body">
      <div
        ref="searchModal"
        id="searchModal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="searchModalLabel"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-scrollable">
          <div class="modal-content">
            <div class="modal-header">
              <form
                @submit.prevent="searchItems()"
                class="d-flex align-items-center border rounded w-100"
              >
                <span class="text-secondary ms-2">
                  <i class="fa-solid fa-magnifying-glass"></i>
                </span>
                <input
                  ref="searchInput"
                  v-model="searchQuery"
                  class="form-control rounded border-0 shadow-none m-1"
                  type="search"
                  :placeholder="$t('search.search2')"
                  aria-label="Search"
                  autocomplete="off"
                  autocorrect="off"
                  autocapitalize="off"
                  enterkeyhint="search"
                  spellcheck="false"
                >
              </form>
            </div>
            <div class="modal-body">
              <LoadingIndicator
                v-if="searchLoading"
                :actionInfo="$t('search.searching')"
              />
              <div v-else-if="searchedItems.length > 0">

              </div>
              <div
                v-else
                class="text-center p-5"
              >
                {{ $t('search.no_results_found') }}
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-light"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.close') }}
              </button>
              <button
                @click="searchItems()"
                type="button"
                class="btn btn-brand"
                :disabled="!searchQuery"
              >
                {{ $t('search.search1') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
form:hover,
form:focus-within {
  border-color: #e72a26 !important;
}
</style>

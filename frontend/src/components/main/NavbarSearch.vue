<script setup>
import axios from 'axios'
import { ref } from 'vue'

const searchQuery = ref('')
const searchedItems = ref([])

const searchInput = ref(null)

const clickSearchLink = () => {
  setTimeout(() => {
    searchInput.value.focus()
  }, 500)
}

const searchItems = async () => {
  console.log(searchQuery.value)
}
</script>

<template>
  <div class="navbar-search">
    <a
      @click="clickSearchLink()"
      href="#"
      class="text-decoration-none link-secondary"
      data-bs-toggle="modal"
      data-bs-target="#searchModal"
    >
      <i class="fa-solid fa-magnifying-glass"></i>
    </a>

    <Teleport to="body">
      <div
        class="modal fade"
        id="searchModal"
        data-bs-keyboard="false"
        tabindex="-1"
        aria-labelledby="searchModalLabel"
        aria-hidden="true"
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
              <div v-if="searchedItems.length > 0">

              </div>
              <div
                v-else
                class="text-center p-3"
              >
                {{ $t('search.no_results_found') }}
              </div>
            </div>
            <div class="modal-footer">
              <button
                ref="btnClose"
                type="button"
                class="btn btn-light"
                data-bs-dismiss="modal"
                aria-label="Close"
              >
                {{ $t('modal.close') }}
              </button>
              <button
                @click="searchItems()"
                class="btn btn-brand"
                type="button"
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
.modal-body {
  scrollbar-color: #c0c0c0;
  scrollbar-width: thin;
}
.modal-body::-webkit-scrollbar {
  width: 0.3em;
  height: 0.3em;
  background-color: #f5f5f5;
}
.modal-body::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 3em;
}
.modal-body::-webkit-scrollbar-thumb:hover {
  background-color: #808080;
}
</style>

<script setup>
import axios from 'axios'
import { ref } from 'vue'

const searchLoading = ref(false)
const searchQuery = ref('')
const searchedItems = ref([])

const searchInput = ref(null)
const btnClose = ref(null)

const clickSearchLink = () => {
  setTimeout(() => {
    searchInput.value.focus()
  }, 500)
}

const searchItems = async () => {
  searchLoading.value = true
  console.log(searchQuery.value)
  searchLoading.value = false
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
        tabindex="-1"
        data-bs-keyboard="false"
        aria-hidden="true"
        aria-labelledby="searchModalLabel"
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
                ref="btnClose"
                class="btn btn-light"
                type="button"
                data-bs-dismiss="modal"
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

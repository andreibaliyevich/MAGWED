<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useCurrencyStore } from '@/stores/currency.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const currencyStore = useCurrencyStore()

const searchLoading = ref(false)
const searchType = ref('organizers')
const searchQuery = ref('')
const searchedItems = ref([])
const moreItemsLoading = ref(false)
const nextURL = ref(null)

const searchModal = ref(null)
const searchModalBootstrap = ref(null)
const searchInput = ref(null)
const searchModalBody = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

const searchItems = async () => {
  searchLoading.value = true

  let requestUrl = ''
  if (searchType.value === 'organizers') {
    requestUrl = '/accounts/organizers/'
  } else if (searchType.value === 'photos') {
    requestUrl = '/portfolio/photo/list/'
  } else if (searchType.value === 'albums') {
    requestUrl = '/portfolio/album/list/'
  } else if (searchType.value === 'articles') {
    requestUrl = '/blog/article/list/'
  }

  try {
    const response = await axios.get(requestUrl, {
      params: {
        search: searchQuery.value
      }
    })
    searchedItems.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    searchLoading.value = false
  }
}

const getMoreItems = async () => {
  moreItemsLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    searchedItems.value = [...searchedItems.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    moreItemsLoading.value = false
  }
}

watch(searchType, () => {
  if (searchQuery.value) {
    nextURL.value = null
    searchItems()
  }
})

watch(searchQuery, (newValue) => {
  nextURL.value = null
  if (newValue) {
    searchItems()
  } else {
    searchedItems.value = []
  }
})

onMounted(() => {
  searchModalBootstrap.value = new bootstrap.Modal(searchModal.value)
  searchModal.value.addEventListener('shown.bs.modal', () => {
    searchInput.value.focus()
  })
  searchModal.value.addEventListener('hidden.bs.modal', () => {
    searchType.value = 'organizers'
    searchQuery.value = ''
    searchedItems.value = []
    nextURL.value = null
  })
})
</script>

<template>
  <div class="navbar-search">
    <button
      type="button"
      class="btn btn-link link-secondary p-0"
      data-bs-toggle="modal"
      data-bs-target="#search_modal"
    >
      <i class="fa-solid fa-magnifying-glass"></i>
    </button>

    <Teleport to="body">
      <div
        ref="searchModal"
        id="search_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="search_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-scrollable modal-fullscreen-sm-down">
          <div class="modal-content">
            <div class="modal-header">
              <form
                @submit.prevent="searchItems()"
                class="w-100"
              >
                <div class="d-flex align-items-center border rounded">
                  <span class="text-secondary ms-2">
                    <i class="fa-solid fa-magnifying-glass"></i>
                  </span>
                  <input
                    ref="searchInput"
                    v-model="searchQuery"
                    class="form-control border-0 m-1"
                    type="search"
                    autocomplete="off"
                    autocorrect="off"
                    autocapitalize="off"
                    enterkeyhint="search"
                    spellcheck="false"
                    :placeholder="$t('search.search2')"
                    aria-label="Search"
                  >
                </div>
                <div class="d-flex justify-content-center mt-1">
                  <div
                    role="group"
                    class="btn-group"
                    aria-label="Search Type"
                  >
                    <input
                      v-model="searchType"
                      value="organizers"
                      id="id_search_type_1"
                      name="search_type"
                      type="radio"
                      class="btn-check"
                    >
                    <label
                      for="id_search_type_1"
                      class="btn btn-outline-dark"
                    >
                      {{ $t('organizers.organizers') }}
                    </label>

                    <input
                      v-model="searchType"
                      value="photos"
                      id="id_search_type_2"
                      name="search_type"
                      type="radio"
                      class="btn-check"
                    >
                    <label
                      for="id_search_type_2"
                      class="btn btn-outline-dark"
                    >
                      {{ $t('portfolio.photos') }}
                    </label>

                    <input
                      v-model="searchType"
                      value="albums"
                      id="id_search_type_3"
                      name="search_type"
                      type="radio"
                      class="btn-check"
                    >
                    <label
                      for="id_search_type_3"
                      class="btn btn-outline-dark"
                    >
                      {{ $t('portfolio.photo_albums') }}
                    </label>

                    <input
                      v-model="searchType"
                      value="articles"
                      id="id_search_type_4"
                      name="search_type"
                      type="radio"
                      class="btn-check"
                    >
                    <label
                      for="id_search_type_4"
                      class="btn btn-outline-dark"
                    >
                      {{ $t('blog.articles') }}
                    </label>
                  </div>
                </div>
              </form>
            </div>
            <div
              ref="searchModalBody"
              class="modal-body"
            >
              <LoadingIndicator
                v-if="searchLoading"
                :actionInfo="$t('search.searching')"
              />
              <div v-else-if="searchedItems.length > 0">
                <div v-if="searchType === 'organizers'">
                  <div
                    v-for="organizer in searchedItems"
                    :key="organizer.user.uuid"
                    class="card border border-light shadow-sm mb-1"
                  >
                    <div class="row g-0">
                      <div class="col-2 d-flex align-items-center">
                        <router-link
                          :to="{
                            name: 'OrganizerDetail',
                            params: {
                              locale: $i18n.locale,
                              profile_url: organizer.user.profile_url
                            }
                          }"
                          @click="searchModalBootstrap.hide()"
                        >
                          <UserAvatarExtended
                            :src="organizer.user.avatar"
                            :width="80"
                            :height="80"
                            :online="organizer.user.status === 'online' ? true : false"
                          />
                        </router-link>
                      </div>
                      <div class="col-10">
                        <div class="card-body">
                          <router-link
                            :to="{
                              name: 'OrganizerDetail',
                              params: {
                                locale: $i18n.locale,
                                profile_url: organizer.user.profile_url
                              }
                            }"
                            @click="searchModalBootstrap.hide()"
                            class="text-decoration-none link-dark"
                          >
                            <h5 class="card-title">{{ organizer.user.name }}</h5>
                          </router-link>
                          <p
                            v-if="organizer.cost_work"
                            class="card-text"
                          >
                            {{ currencyStore.currencyText }}{{ currencyStore.convertCurrency(organizer.cost_work) }}
                            {{ $t('organizers.per_hour') }}
                            <span
                              v-if="organizer.number_hours"
                              class="small text-muted"
                            >
                              {{ $t('organizers.min_number_hours', { n: organizer.number_hours }) }}
                            </span>
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else-if="searchType === 'photos'">
                  <div
                    v-for="photoItem in searchedItems"
                    :key="photoItem.uuid"
                    class="card border border-light shadow-sm mb-1"
                  >
                    <div class="row g-0">
                      <div class="col-4 d-flex align-items-center">
                        <router-link
                          :to="{
                            name: 'PhotoDetail',
                            params: {
                              locale: $i18n.locale,
                              uuid: photoItem.uuid
                            }
                          }"
                          @click="searchModalBootstrap.hide()"
                        >
                          <img
                            :src="photoItem.thumbnail"
                            class="card-img"
                          >
                        </router-link>
                      </div>
                      <div class="col-8">
                        <div class="card-body d-flex flex-column h-100">
                          <router-link
                            v-if="photoItem.title"
                            :to="{
                              name: 'PhotoDetail',
                              params: {
                                locale: $i18n.locale,
                                uuid: photoItem.uuid
                              }
                            }"
                            @click="searchModalBootstrap.hide()"
                            class="text-decoration-none link-dark"
                          >
                            <h5 class="card-title">{{ photoItem.title }}</h5>
                          </router-link>
                          <div class="d-flex align-items-center mt-auto">
                            <router-link
                              :to="{
                                name: 'OrganizerDetail',
                                params: {
                                  locale: $i18n.locale,
                                  profile_url: photoItem.author.profile_url
                                }
                              }"
                              @click="searchModalBootstrap.hide()"
                            >
                              <UserAvatar
                                :src="photoItem.author.avatar"
                                :width="24"
                                :height="24"
                              />
                            </router-link>
                            <router-link
                              :to="{
                                name: 'OrganizerDetail',
                                params: {
                                  locale: $i18n.locale,
                                  profile_url: photoItem.author.profile_url
                                }
                              }"
                              @click="searchModalBootstrap.hide()"
                              class="text-decoration-none link-dark ms-2"
                            >
                              {{ photoItem.author.name }}
                            </router-link>
                          </div>
                          <div class="d-flex justify-content-between mt-auto">
                            <div class="text-muted">
                              <i class="fa-regular fa-eye"></i>
                              {{ photoItem.view_count }}
                            </div>
                            <div class="text-muted">
                              <i class="fa-regular fa-heart"></i>
                              {{ photoItem.like_count }}
                            </div>
                            <div class="text-muted">
                              <i class="fa-regular fa-star"></i>
                              {{ photoItem.rating }}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else-if="searchType === 'albums'">
                  <div
                    v-for="albumItem in searchedItems"
                    :key="albumItem.uuid"
                    class="card border border-light shadow-sm mb-1"
                  >
                    <div class="row g-0">
                      <div class="col-4 d-flex align-items-center">
                        <router-link
                          :to="{
                            name: 'AlbumDetail',
                            params: {
                              locale: $i18n.locale,
                              uuid: albumItem.uuid
                            }
                          }"
                          @click="searchModalBootstrap.hide()"
                        >
                          <img
                            :src="albumItem.thumbnail"
                            class="card-img"
                            :alt="albumItem.title"
                          >
                        </router-link>
                      </div>
                      <div class="col-8">
                        <div class="card-body d-flex flex-column h-100">
                          <router-link
                            :to="{
                              name: 'AlbumDetail',
                              params: {
                                locale: $i18n.locale,
                                uuid: albumItem.uuid
                              }
                            }"
                            @click="searchModalBootstrap.hide()"
                            class="text-decoration-none link-dark"
                          >
                            <h5 class="card-title">{{ albumItem.title }}</h5>
                          </router-link>
                          <div class="d-flex align-items-center mt-auto">
                            <router-link
                              :to="{
                                name: 'OrganizerDetail',
                                params: {
                                  locale: $i18n.locale,
                                  profile_url: albumItem.author.profile_url
                                }
                              }"
                              @click="searchModalBootstrap.hide()"
                            >
                              <UserAvatar
                                :src="albumItem.author.avatar"
                                :width="24"
                                :height="24"
                              />
                            </router-link>
                            <router-link
                              :to="{
                                name: 'OrganizerDetail',
                                params: {
                                  locale: $i18n.locale,
                                  profile_url: albumItem.author.profile_url
                                }
                              }"
                              @click="searchModalBootstrap.hide()"
                              class="text-decoration-none link-dark ms-2"
                            >
                              {{ albumItem.author.name }}
                            </router-link>
                          </div>
                          <div class="d-flex justify-content-between mt-auto">
                            <div class="text-muted">
                              <i class="fa-regular fa-eye"></i>
                              {{ albumItem.view_count }}
                            </div>
                            <div class="text-muted">
                              <i class="fa-regular fa-heart"></i>
                              {{ albumItem.like_count }}
                            </div>
                            <div class="text-muted">
                              <i class="fa-regular fa-star"></i>
                              {{ albumItem.rating }}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else-if="searchType === 'articles'">
                  <div
                    v-for="article in searchedItems"
                    :key="article.slug"
                    class="card border border-light shadow-sm mb-3"
                  >
                    <div class="d-flex align-items-center">
                      <router-link
                        :to="{
                          name: 'ArticleDetail',
                          params: {
                            locale: $i18n.locale,
                            slug: article.slug
                          }
                        }"
                        @click="searchModalBootstrap.hide()"
                      >
                        <img
                          :src="article.thumbnail"
                          class="img-fluid rounded"
                          :alt="article.translated_title"
                        >
                      </router-link>
                    </div>
                    <div class="card-body">
                      <router-link
                        :to="{
                          name: 'ArticleDetail',
                          params: {
                            locale: $i18n.locale,
                            slug: article.slug
                          }
                        }"
                        @click="searchModalBootstrap.hide()"
                        class="text-decoration-none link-dark"
                      >
                        <h5 class="card-title">{{ article.translated_title }}</h5>
                      </router-link>
                      <div class="mb-1">
                        <span
                          v-for="category in article.categories"
                          :key="category"
                          class="badge text-bg-light ms-1"
                        >
                          {{ $t(`category_choices.${category}`) }}
                        </span>
                      </div>
                      <p class="card-text">{{ article.translated_description }}</p>
                      <p class="card-text">
                        <small class="text-body-secondary">
                          <i class="fa-regular fa-calendar-days"></i>
                          {{ getLocaleDateString(article.published_at) }}
                        </small>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div
                v-else-if="searchQuery"
                class="text-center p-5"
              >
                {{ $t('search.no_results_found') }}
              </div>
              <div
                v-else
                class="text-center p-5"
              >
                {{ $t('search.enter_your_request') }}
              </div>
              <div
                v-if="nextURL"
                style="min-height: 1px; margin-bottom: 1px;"
                v-intersection="{
                  'scrollArea': searchModalBody,
                  'callbackFunction': getMoreItems,
                  'functionArguments': []
                }"
              ></div>
              <LoadingIndicator v-if="moreItemsLoading" />
            </div>
            <div class="modal-footer">
              <button
                ref="modalMenuClose"
                type="button"
                class="btn btn-light"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.close') }}
              </button>
              <button
                @click="() => {
                  nextURL = null
                  searchItems()
                }"
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
.d-flex.align-items-center.border.rounded:hover,
.d-flex.align-items-center.border.rounded:focus-within {
  border-color: #e72a26 !important;
}
</style>

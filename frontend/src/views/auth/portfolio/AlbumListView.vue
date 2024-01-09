<script setup>
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const router = useRouter()
const { locale } = useI18n({ useScope: 'global' })

const albumListLoading = ref(true)
const albumList = ref([])
const nextURL = ref(null)

const albumCreating = ref(false)
const albumUuid = ref(null)
const albumImage = ref(null)
const albumTitle = ref('')
const albumDescription = ref('')

const { getLocaleDateTimeString } = useLocaleDateTime()

const errors = ref(null)

const createAlbumModal = ref(null)
const createAlbumModalBootstrap = ref(null)
const albumImg = ref(null)

const getAlbumList = async () => {
  try {
    const response = await axios.get('/portfolio/album/author/list-create/')
    albumList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    albumListLoading.value = false
  }
}

const getMoreAlbumList = async () => {
  albumListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    albumList.value = [...albumList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    albumListLoading.value = false
  }
}

const loadAlbumImage = async (filelist) => {
  albumImage.value = filelist[0]
  const reader = new FileReader()
  reader.readAsDataURL(filelist[0])
  reader.onload = () => {
    albumImg.value.src = reader.result
    albumImg.value.alt = filelist[0].name
  }
}

const createAlbum = async () => {
  albumCreating.value = true
  try {
    let formData = new FormData()
    formData.append('image', albumImage.value, albumImage.value.name)
    formData.append('title', albumTitle.value)
    formData.append('description', albumDescription.value)

    const response = await axios.post(
      '/portfolio/album/author/list-create/',
      formData
    )
    createAlbumModalBootstrap.value.hide()
    router.push({
      name: 'PortfolioAlbumDetail',
      params: {
        locale: locale.value,
        uuid: response.data.uuid
      }
    })
  } catch (error) {
    errors.value = error.response.data
  } finally {
    albumCreating.value = false
  }
}

const removeAlbum = async () => {
  try {
    const response = await axios.delete(
      '/portfolio/album/author/rud/'
        + albumUuid.value
        +'/'
    )
    albumList.value = albumList.value.filter((element) => {
      return element.uuid !== albumUuid.value
    })
  } catch (error) {
    console.error(error)
  } finally {
    albumUuid.value = null
  }
}

onMounted(() => {
  getAlbumList()
  createAlbumModal.value.addEventListener('hidden.bs.modal', () => {
    albumUuid.value = null
    albumImage.value = null
    albumTitle.value = ''
    albumDescription.value = ''
    errors.value = null

    if (albumImg.value) {
      albumImg.value.src = ''
      albumImg.value.alt = ''
    }
  })
  createAlbumModalBootstrap.value = new bootstrap.Modal(createAlbumModal.value)
})
</script>

<template>
  <div class="portfolio-album-list-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <div class="d-flex align-items-center mb-5">
        <router-link
          :to="{ name: 'Portfolio' }"
          class="link-danger text-decoration-none display-6"
        >
          {{ $t('portfolio.portfolio') }}
        </router-link>
        <i class="fa-solid fa-chevron-right mt-2 mx-2"></i>
        <h1 class="display-6 mb-0">
          {{ $t('portfolio.albums') }}
        </h1>
      </div>

      <button
        type="button"
        class="btn btn-soft-brand w-100"
        data-bs-toggle="modal"
        data-bs-target="#create_album_modal"
      >
        {{ $t('portfolio.create_album') }}
        <i class="fa-regular fa-square-plus"></i>
      </button>

      <div
        v-if="albumList.length > 0"
        class="row g-1 mt-1"
      >
        <div
          v-for="albumItem in albumList"
          :key="albumItem.uuid"
          class="col-12 col-md-6 col-xl-4"
        >
          <div class="card border border-0 shadow-sm h-100">
            <img
              :src="albumItem.thumbnail"
              :alt="albumItem.title"
              class="card-img-top"
            >
            <div class="card-body">
              <h5 class="card-title">{{ albumItem.title }}</h5>
              <p class="text-body-secondary">{{ getLocaleDateTimeString(albumItem.created_at) }}</p>
            </div>
            <div class="card-img-overlay text-light">
              <div class="position-absolute top-50 start-50 translate-middle">
                <router-link
                  :to="{
                    name: 'PortfolioAlbumDetail',
                    params: { uuid: albumItem.uuid }
                  }"
                  class="btn btn-outline-light btn-sm"
                >
                  <i class="fa-solid fa-pen fa-sm"></i>
                </router-link>
                <button
                  @click="albumUuid = albumItem.uuid"
                  type="button"
                  class="btn btn-danger btn-sm ms-1"
                  data-bs-toggle="modal"
                  data-bs-target="#remove_album_modal_choice"
                >
                  <i class="fa-solid fa-trash fa-sm"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-else-if="!albumListLoading"
        class="lead d-flex justify-content-center py-3"
      >
        {{ $t('portfolio.no_albums') }}
      </div>
      <div
        v-if="nextURL"
        style="min-height: 1px; margin-bottom: 1px;"
        v-intersection="{
          'scrollArea': null,
          'callbackFunction': getMoreAlbumList,
          'functionArguments': []
        }"
      ></div>
      <LoadingIndicator v-if="albumListLoading" />
    </div>

    <Teleport to="body">
      <div
        ref="createAlbumModal"
        id="create_album_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="create_album_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="create_album_modal_label"
                class="modal-title"
              >
                {{ $t('portfolio.creating_album') }}
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form
                @submit.prevent="createAlbum()"
                id="create_album_form"
              >
                <div class="mb-3">
                  <span v-if="albumImage">
                    {{ $t('portfolio.chosen_image') }}:
                  </span>
                  <div class="d-flex justify-content-center">
                    <img
                      ref="albumImg"
                      src=""
                      alt=""
                      class="mw-100 max-vh-75"
                    >
                  </div>
                  <FileInputButton
                    @selectedFiles="loadAlbumImage"
                    buttonClass="btn btn-soft-brand w-100"
                    accept="image/*"
                  >
                    {{ $t('portfolio.choose_image') }}
                    <i class="fa-regular fa-image"></i>
                  </FileInputButton>
                  <div
                    v-if="errors && errors.image"
                    id="id_image-errors"
                    class="text-danger"
                    aria-live="assertive"
                  >
                    <small v-for="error in errors.image">
                      {{ error }}
                    </small>
                  </div>
                </div>
                <div class="mb-3">
                  <BaseInput
                    v-model="albumTitle"
                    type="text"
                    maxlength="128"
                    id="id_title"
                    name="title"
                    :label="$t('portfolio.title')"
                    :errors="errors?.title ? errors.title : []"
                  />
                </div>
                <div class="mb-3">
                  <BaseTextarea
                    v-model="albumDescription"
                    id="id_description"
                    name="description"
                    :label="$t('portfolio.description')"
                    :errors="errors?.description ? errors.description : []"
                  />
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-light"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.cancel') }}
              </button>
              <SubmitButton
                :loadingStatus="albumCreating"
                buttonClass="btn btn-brand"
                form="create_album_form"
                :disabled="!albumImage || !albumTitle"
              >
                {{ $t('btn.create') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>

      <div
        id="remove_album_modal_choice"
        class="modal fade"
        role="dialog"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div
          class="modal-dialog modal-dialog-centered"
          role="document"
        >
          <div class="modal-content rounded-3 shadow">
            <div class="modal-body p-4 text-center">
              <h5 class="mb-0">{{ $t('portfolio.you_want_remove_album') }}</h5>
              <p class="mb-0">{{ $t('portfolio.album_information_will_lost') }}</p>
            </div>
            <div class="modal-footer flex-nowrap p-0">
              <button
                @click="removeAlbum()"
                type="button"
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0 border-end"
                data-bs-dismiss="modal"
              >
                <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
              </button>
              <button
                type="button"
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.no_cancel') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

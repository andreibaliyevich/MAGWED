<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const router = useRouter()
const { locale } = useI18n({ useScope: 'global' })

const albumListLoading = ref(true)
const albumList = ref([])

const albumCreating = ref(false)
const albumUuid = ref(null)

const albumImage = ref(null)
const albumTitle = ref('')
const albumDescription = ref('')

const { getLocaleDateTimeString } = useLocaleDateTime()

const errors = ref(null)

const createAlbumModal = ref(null)
const createAlbumModalBootstrap = ref(null)

const getAlbumList = async () => {
  try {
    const response = await axios.get('/portfolio/album/crud/list/')
    albumList.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    albumListLoading.value = false
  }
}

const createAlbum = async () => {
  albumCreating.value = true
  try {
    const albumData = new FormData()
    albumData.append('image', albumImage.value, albumImage.value.name)
    albumData.append('title', albumTitle.value)
    albumData.append('description', albumDescription.value)

    const response = await axios.post('/portfolio/album/crud/list/', albumData)
    errors.value = null
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
      '/portfolio/album/crud/detail/'
        + albumUuid.value
        +'/'
    )
    albumList.value = albumList.value.filter((element) => {
      return element.uuid != albumUuid.value
    })
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  getAlbumList()
  createAlbumModal.value.addEventListener('hidden.bs.modal', () => {
    albumImage.value = null
    albumTitle.value = ''
    albumDescription.value = ''
    errors.value = null
  })
  createAlbumModalBootstrap.value = new bootstrap.Modal(createAlbumModal.value)
})
</script>

<template>
  <div class="portfolio-album-list-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">
        {{ $t('portfolio.albums') }}
      </h1>

      <button
        class="btn btn-soft-brand w-100"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#createAlbumModal"
      >
        {{ $t('portfolio.create_album') }}
        <i class="fa-regular fa-square-plus"></i>
      </button>

      <LoadingIndicator v-if="albumListLoading" />
      <div
        v-else-if="albumList.length > 0"
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
                <LocaleRouterLink
                  routeName="PortfolioAlbumDetail"
                  :routeParams="{ uuid: albumItem.uuid }"
                  class="btn btn-outline-light btn-sm"
                >
                  <i class="fa-solid fa-pen fa-sm"></i>
                </LocaleRouterLink>
                <button
                  @click="albumUuid = albumItem.uuid"
                  class="btn btn-danger btn-sm ms-1"
                  type="button"
                  data-bs-toggle="modal"
                  data-bs-target="#removeAlbumModalChoice"
                >
                  <i class="fa-solid fa-trash fa-sm"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-else
        class="lead d-flex justify-content-center py-3"
      >
        {{ $t('portfolio.no_albums') }}
      </div>
    </div>
    <Teleport to="body">
      <div
        ref="createAlbumModal"
        id="createAlbumModal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="createAlbumModalLabel"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="createAlbumModalLabel"
                class="modal-title"
              >
                {{ $t('portfolio.creating_album') }}
              </h5>
              <button
                class="btn-close"
                type="button"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form
                @submit.prevent="createAlbum()"
                id="albumModalForm"
                class="row g-3"
              >
                <div class="col-md-12">
                  <span v-if="albumImage">
                    {{ $t('portfolio.chosen_image') }}:
                    {{ albumImage.name }}
                  </span>
                  <FileInputButton
                    @selectedFiles="(filelist) => albumImage = filelist[0]"
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
                <div class="col-md-12">
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
                <div class="col-md-12">
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
                class="btn btn-light"
                type="button"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.cancel') }}
              </button>
              <SubmitButton
                :loadingStatus="albumCreating"
                buttonClass="btn btn-brand"
                form="albumModalForm"
                :disabled="!albumImage || !albumTitle"
              >
                {{ $t('btn.create') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>

      <div
        id="removeAlbumModalChoice"
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
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0 border-end"
                type="button"
                data-bs-dismiss="modal"
              >
                <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
              </button>
              <button
                class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0"
                type="button"
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

<script setup>
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import PortfolioPhotoList from '@/components/auth/PortfolioPhotoList.vue'

const route = useRoute()
const router = useRouter()
const { locale } = useI18n({ useScope: 'global' })
const { getLocaleDateTimeString } = useLocaleDateTime()

const albumLoading = ref(true)
const albumUpdating = ref(false)
const albumImageUpdating = ref(false)

const albumUuid = ref(null)
const albumImage = ref(null)

const albumTitle = ref('')
const albumDescription = ref('')
const albumTags = ref([])

const albumCreatedAt = ref(null)
const albumNumViews = ref(0)
const albumLikesCount = ref(0)
const albumRating = ref(0)

const albumPhotoList = ref([])

const albumPhotosUploadStatus = ref(0)
const albumPhotosUploading = ref(false)

const uploadAlbumPhotosModal = ref(null)
const uploadAlbumPhotosModalBootstrap = ref(null)

const photosUploadStatusRound = computed(() => {
  return Math.round(albumPhotosUploadStatus.value)
})

const status = ref(null)
const errors = ref(null)

const getAlbumData = async () => {
  try {
    const response = await axios.get(
      '/portfolio/albums/' + route.params.uuid +'/'
    )
    albumUuid.value = response.data.uuid
    albumImage.value = response.data.image

    albumTitle.value = response.data.title
    albumDescription.value = response.data.description
    albumTags.value = response.data.tags

    albumCreatedAt.value = response.data.created_at
    albumNumViews.value = response.data.num_views
    albumLikesCount.value = response.data.likes_count
    albumRating.value = response.data.rating
    
    albumPhotoList.value = response.data.photos
  } catch (error) {
    console.error(error)
  } finally {
    albumLoading.value = false
  }
}

const updateAlbumImage = async (filelist) => {
  albumImageUpdating.value = true

  const albumImageData = new FormData()
  albumImageData.append('image', filelist[0], filelist[0].name)

  try {
    const response = await axios.put(
      '/portfolio/albums/' + albumUuid.value +'/image/',
      albumImageData
    )
    albumImage.value = response.data.image
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    albumImageUpdating.value = false
  }
}

const updateAlbum = async () => {
  albumUpdating.value = true
  try {
    const response = await axios.put(
      '/portfolio/albums/' + albumUuid.value +'/',
      {
        'title': albumTitle.value,
        'description': albumDescription.value,
        'tags': albumTags.value
      }
    )
    router.push({
      name: 'PortfolioAlbums',
      params: { locale: locale.value }
    })
  } catch (error) {
    console.error(error)
  } finally {
    albumUpdating.value = false
  }
}

const removeAlbum = async () => {
  try {
    const response = await axios.delete(
      '/portfolio/albums/' + albumUuid.value +'/'
    )
    router.push({
      name: 'PortfolioAlbums',
      params: { locale: locale.value }
    })
  } catch (error) {
    console.error(error)
  }
}

const uploadAlbumPhotos = async (filelist) => {
  uploadAlbumPhotosModalBootstrap.value.show()
  albumPhotosUploading.value = true
  const uploadStep = 100 / filelist.length

  for (let i = 0; i < filelist.length; i++) {
    if (albumPhotosUploading.value) {
      const photoData = new FormData()
      photoData.append('album', albumUuid.value)
      photoData.append('image', filelist[i], filelist[i].name)

      try {
        const response = await axios.post('/portfolio/photos/', photoData)
        albumPhotoList.value.unshift(response.data)
        albumPhotosUploadStatus.value += uploadStep
      } catch (error) {
        console.error(error)
      }
    } else {
      break
    }
  }

  albumPhotosUploading.value = false
  setTimeout(() => {
    uploadAlbumPhotosModalBootstrap.value.hide()
  }, 500)
}

const updateAlbumPhotoList = (pUuid, pTitle) => {
  const foundIndex = albumPhotoList.value.findIndex((element) => {
    return element.uuid == pUuid
  })
  albumPhotoList.value[foundIndex].title = pTitle
}

const removeAlbumPhotoList = (pUuid) => {
  albumPhotoList.value = albumPhotoList.value.filter((element) => {
    return element.uuid != pUuid
  })
}

onMounted(() => {
  getAlbumData()
  uploadAlbumPhotosModal.value.addEventListener('hidden.bs.modal', () => {
    albumPhotosUploadStatus.value = 0
  })
  uploadAlbumPhotosModalBootstrap.value = new bootstrap.Modal(
    uploadAlbumPhotosModal.value
  )
})
</script>

<template>
  <div class="portfolio-album-view">
    <LoadingIndicator v-if="albumLoading" />
    <div
      v-else
    >
      <div class="card mb-2">
        <LoadingIndicator
          v-if="albumImageUpdating"
          :actionInfo="$t('auth.portfolio.uploading_image')"
        />
        <div v-else>
          <img
            :src="albumImage"
            class="card-img-top"
          >
          <div class="card-body text-center">
            <small
              v-if="status == 200"
              class="text-success"
            >
              {{ $t('auth.portfolio.image_updated_successfully') }}
            </small>
            <small
              v-if="errors && errors.image"
              v-for="error in errors.image"
              class="text-danger"
            >
              {{ error }}
            </small>
            <div class="d-flex justify-content-center">
              <FileInputButton
                @selectedFiles="updateAlbumImage"
                buttonClass="btn btn-light-brand m-1"
                accept="image/*"
              >
                {{ $t('auth.portfolio.update_image') }}
              </FileInputButton>
            </div>
            <small class="text-muted">
              {{ $t('form_help.input_img', { width: '1500', height: '500' }) }}
            </small>
          </div>
        </div>
      </div>

      <form
        @submit.prevent="updateAlbum()"
        id="albumForm"
        class="row g-3"
      >
        <div class="col-md-12">
          <BaseInput
            v-if="errors && errors.title"
            v-model="albumTitle"
            type="text"
            maxlength="128"
            id="id_title"
            name="title"
            :label="$t('auth.portfolio.title')"
            :errors="errors.title"
          />
          <BaseInput
            v-else
            v-model="albumTitle"
            type="text"
            maxlength="128"
            id="id_title"
            name="title"
            :label="$t('auth.portfolio.title')"
          />
        </div>
        <div class="col-md-12">
          <BaseTextarea
            v-if="errors && errors.description"
            v-model="albumDescription"
            id="id_description"
            name="description"
            :label="$t('auth.portfolio.description')"
            :errors="errors.description"
          />
          <BaseTextarea
            v-else
            v-model="albumDescription"
            id="id_description"
            name="description"
            :label="$t('auth.portfolio.description')"
          />
        </div>
        <div class="col-md-12">
          <ListInput
            v-if="errors && errors.tags"
            v-model="albumTags"
            id="id_tags"
            name="tags"
            :label="$t('auth.portfolio.tags')"
            :errors="errors.tags"
          />
          <ListInput
            v-else
            v-model="albumTags"
            id="id_tags"
            name="tags"
            :label="$t('auth.portfolio.tags')"
          />
        </div>
      </form>

      <hr>
      <ul class="list-unstyled my-0 px-xl-10">
        <li>{{ $t('auth.portfolio.created_at') }} {{ getLocaleDateTimeString(albumCreatedAt) }}</li>
        <li>{{ $t('auth.portfolio.num_views') }}: {{ albumNumViews }}</li>
        <li>{{ $t('auth.portfolio.likes') }}: {{ albumLikesCount }}</li>
        <li>{{ $t('auth.portfolio.rating') }}: {{ albumRating }}</li>
      </ul>

      <div class="d-grid d-md-flex justify-content-md-end gap-2 mt-3">
        <button
          class="btn btn-outline-dark"
          type="button"
          data-bs-toggle="modal"
          data-bs-target="#removeAlbumModalChoice"
        >
          {{ $t('btn.delete') }}
        </button>
        <SubmitButton
          :loadingStatus="albumUpdating"
          buttonClass="btn btn-brand"
          form="albumForm"
        >
          {{ $t('btn.update') }}
        </SubmitButton>
      </div>

      <hr>
      <FileInputButton
        @selectedFiles="uploadAlbumPhotos"
        buttonClass="btn btn-light-brand w-100"
        accept="image/*"
        multiple
      >
        {{ $t('auth.portfolio.upload_photos') }}
        <i class="fa-solid fa-upload"></i>
      </FileInputButton>

      <PortfolioPhotoList
        v-if="albumPhotoList.length > 0"
        :photoList="albumPhotoList"
        @updatePhoto="updateAlbumPhotoList"
        @removePhoto="removeAlbumPhotoList"
      />
    </div>
    <Teleport to="body">
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
              <h5 class="mb-0">{{ $t('auth.portfolio.you_want_remove_album') }}</h5>
              <p class="mb-0">{{ $t('auth.portfolio.album_information_will_lost') }}</p>
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

      <div
        ref="uploadAlbumPhotosModal"
        id="uploadAlbumPhotosModal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="uploadAlbumPhotosModalLabel"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="uploadPhotosModalLabel"
                class="modal-title"
              >
                {{ $t('auth.portfolio.uploading_photos') }}
              </h5>
            </div>
            <div class="modal-body">
              <div class="progress">
                <div
                  class="progress-bar progress-bar-striped progress-bar-animated"
                  role="progressbar"
                  aria-label="Upload status of photos"
                  :aria-valuenow="photosUploadStatusRound"
                  aria-valuemin="0"
                  aria-valuemax="100"
                  :style="`width: ${photosUploadStatusRound}%`"
                >{{ photosUploadStatusRound }}%</div>
              </div>
            </div>
            <div class="modal-footer">
              <button
                @click="albumPhotosUploading = false"
                class="btn btn-danger"
                type="button"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.cancel') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

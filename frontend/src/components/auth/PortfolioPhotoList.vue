<script setup>
import axios from 'axios'
import { useRoute } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const route = useRoute()

const photoListLoading = ref(true)
const photoList = ref([])
const nextURL = ref(null)

const photosUploadStatus = ref(0)
const photosUploading = ref(false)

const photoUpdating = ref(false)
const photoUuid = ref(null)
const photoImage = ref(null)
const photoDevice = ref('')
const photoFNumber = ref(null)
const photoExposureTime = ref('')
const photoFocalLength = ref(null)
const photoPhotographicSensitivity = ref(null)
const photoTitle = ref('')
const photoDescription = ref('')
const photoTags = ref([])
const photoUploadedAt = ref(null)
const photoViewCount = ref(0)
const photoLikeCount = ref(0)
const photoRating = ref(0)

const { getLocaleDateTimeString } = useLocaleDateTime()

const errors = ref(null)

const uploadPhotosModal = ref(null)
const uploadPhotosModalBootstrap = ref(null)

const updatePhotoModal = ref(null)
const updatePhotoModalBootstrap = ref(null)

const photosUploadStatusRound = computed(() => {
  return Math.round(photosUploadStatus.value)
})

const getPhotoList = async () => {
  let params = new URLSearchParams()
  if (route.params.uuid) {
    params.append('album', route.params.uuid)
  } else {
    params.append('album_is_null', true)
  }

  try {
    const response = await axios.get('/portfolio/photo/author/list-create/', {
      params: params
    })
    photoList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    photoListLoading.value = false
  }
}

const getMorePhotoList = async () => {
  photoListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    photoList.value = [...photoList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    photoListLoading.value = false
  }
}

const uploadPhotos = async (filelist) => {
  uploadPhotosModalBootstrap.value.show()
  photosUploading.value = true
  const uploadStep = 100 / filelist.length

  for (let i = 0; i < filelist.length; i++) {
    if (photosUploading.value) {
      let formData = new FormData()
      if (route.params.uuid) {
        formData.append('album', route.params.uuid)
      }
      formData.append('image', filelist[i], filelist[i].name)

      try {
        const response = await axios.post(
          '/portfolio/photo/author/list-create/',
          formData
        )
        photoList.value.unshift(response.data)
        photosUploadStatus.value += uploadStep
      } catch (error) {
        console.error(error)
      }
    } else {
      break
    }
  }

  photosUploading.value = false
  setTimeout(() => {
    uploadPhotosModalBootstrap.value.hide()
  }, 500)
}

const getPhotoData = async (pUuid) => {
  try {
    const response = await axios.get(
      '/portfolio/photo/author/rud/'
        + pUuid
        +'/'
    )
    photoUuid.value = pUuid
    photoImage.value = response.data.image

    photoDevice.value = response.data.device
    photoFNumber.value = response.data.f_number
    photoExposureTime.value = response.data.exposure_time
    photoFocalLength.value = response.data.focal_length
    photoPhotographicSensitivity.value = response.data.photographic_sensitivity

    photoTitle.value = response.data.title
    photoDescription.value = response.data.description
    photoTags.value = response.data.tags

    photoUploadedAt.value = response.data.uploaded_at
    photoViewCount.value = response.data.view_count
    photoLikeCount.value = response.data.like_count
    photoRating.value = response.data.rating
  } catch (error) {
    console.error(error)
  }
}

const updatePhoto = async () => {
  photoUpdating.value = true

  if (!photoFNumber.value) {
    photoFNumber.value = null
  }
  if (!photoFocalLength.value) {
    photoFocalLength.value = null
  }
  if (!photoPhotographicSensitivity.value) {
    photoPhotographicSensitivity.value = null
  }

  try {
    const response = await axios.put(
      '/portfolio/photo/author/rud/'
        + photoUuid.value
        +'/',
      {
        device: photoDevice.value,
        f_number: photoFNumber.value,
        exposure_time: photoExposureTime.value,
        focal_length: photoFocalLength.value,
        photographic_sensitivity: photoPhotographicSensitivity.value,
        title: photoTitle.value,
        description: photoDescription.value,
        tags: photoTags.value
      }
    )

    const foundIndex = photoList.value.findIndex((element) => {
      return element.uuid == photoUuid.value
    })
    photoList.value[foundIndex].title = photoTitle.value

    updatePhotoModalBootstrap.value.hide()
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  } finally {
    photoUpdating.value = false
  }
}

const removePhoto = async () => {
  try {
    const response = await axios.delete(
      '/portfolio/photo/author/rud/'
        + photoUuid.value
        +'/'
    )
    photoList.value = photoList.value.filter((element) => {
      return element.uuid !== photoUuid.value
    })
  } catch (error) {
    console.error(error)
  } finally {
    photoUuid.value = null
  }
}

onMounted(() => {
  getPhotoList()
  uploadPhotosModal.value.addEventListener('hidden.bs.modal', () => {
    photosUploadStatus.value = 0
  })
  uploadPhotosModalBootstrap.value = new bootstrap.Modal(
    uploadPhotosModal.value
  )
  updatePhotoModal.value.addEventListener('hidden.bs.modal', () => {
    photoUuid.value = null
    photoImage.value = null

    photoDevice.value = ''
    photoFNumber.value = null
    photoExposureTime.value = ''
    photoFocalLength.value = null
    photoPhotographicSensitivity.value = null

    photoTitle.value = ''
    photoDescription.value = ''
    photoTags.value = []

    photoUploadedAt.value = null
    photoViewCount.value = 0
    photoLikeCount.value = 0
    photoRating.value = 0

    errors.value = null
  })
  updatePhotoModalBootstrap.value = new bootstrap.Modal(updatePhotoModal.value)
})
</script>

<template>
  <div class="portfolio-photo-list">
    <FileDragAndDropInputButton
      @selectedFiles="uploadPhotos"
      buttonClass="btn btn-soft-brand"
      accept="image/*"
      multiple
    >
      <div class="px-2 my-2">{{ $t('portfolio.drag_and_drop_image') }}</div>
      <template #button>
        {{ $t('portfolio.upload_photos') }}
        <i class="fa-solid fa-upload"></i>
      </template>
    </FileDragAndDropInputButton>

    <div
      v-if="photoList.length > 0"
      class="row g-1 mt-1"
    >
      <div
        v-for="photoItem in photoList"
        :key="photoItem.uuid"
        class="col-12 col-md-6 col-xl-4"
      >
        <div class="card h-100">
          <img
            :src="photoItem.thumbnail"
            :alt="photoItem.title"
            class="card-img"
          >
          <div class="card-img-overlay text-light">
            <div class="position-absolute top-0 start-50 translate-middle-x mt-2">
              <h5 class="card-title h6 text-center">{{ photoItem.title }}</h5>
            </div>
            <div class="position-absolute top-50 start-50 translate-middle">
              <button
                @click="getPhotoData(photoItem.uuid)"
                type="button"
                class="btn btn-outline-light btn-sm"
                data-bs-toggle="modal"
                data-bs-target="#update_photo_modal"
              >
                <i class="fa-solid fa-pen fa-sm"></i>
              </button>
              <button
                @click="photoUuid = photoItem.uuid"
                class="btn btn-danger btn-sm ms-1"
                type="button"
                data-bs-toggle="modal"
                data-bs-target="#remove_photo_modal_choice"
              >
                <i class="fa-solid fa-trash fa-sm"></i>
              </button>
            </div>
            <div class="position-absolute bottom-0 start-50 translate-middle-x mb-2">
              <p class="card-text text-center">
                <small>{{ getLocaleDateTimeString(photoItem.uploaded_at) }}</small>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      v-else-if="!photoListLoading"
      class="lead d-flex justify-content-center py-3"
    >
      {{ $t('portfolio.no_photos') }}
    </div>
    <div
      v-if="nextURL"
      style="min-height: 1px; margin-bottom: 1px;"
      v-intersection="{
        'scrollArea': null,
        'callbackFunction': getMorePhotoList,
        'functionArguments': []
      }"
    ></div>
    <LoadingIndicator v-if="photoListLoading" />

    <Teleport to="body">
      <div
        ref="uploadPhotosModal"
        id="upload_photos_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="upload_photos_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="upload_photos_modal_label"
                class="modal-title"
              >
                {{ $t('portfolio.uploading_photos') }}
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
                @click="photosUploading = false"
                type="button"
                class="btn btn-danger"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.cancel') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        ref="updatePhotoModal"
        id="update_photo_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="update_photo_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                id="update_photo_modal_label"
                class="modal-title"
              >
                {{ $t('portfolio.updating_photo') }}
              </h5>
              <button
                class="btn-close"
                type="button"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <div class="d-flex justify-content-center">
                <img
                  :src="photoImage"
                  :alt="photoTitle"
                  class="mw-100 max-vh-75"
                >
              </div>
              <form
                @submit.prevent="updatePhoto()"
                id="photo_modal_form"
                class="row g-3 mt-1 px-xl-10"
              >
                <div class="col-md-12">
                  <BaseInput
                    v-model="photoTitle"
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
                    v-model="photoDescription"
                    id="id_description"
                    name="description"
                    :label="$t('portfolio.description')"
                    :errors="errors?.description ? errors.description : []"
                  />
                </div>
                <div class="col-md-12">
                  <BaseInput
                    v-model="photoDevice"
                    type="text"
                    maxlength="128"
                    id="id_device"
                    name="device"
                    :label="$t('portfolio.device')"
                    :errors="errors?.device ? errors.device : []"
                  />
                </div>
                <div class="col-md-6">
                  <BaseInput
                    v-model="photoFNumber"
                    type="number"
                    step="0.01"
                    id="id_f_number"
                    name="f_number"
                    :label="$t('portfolio.f_number')"
                    :errors="errors?.f_number ? errors.f_number : []"
                  />
                </div>
                <div class="col-md-6">
                  <BaseInput
                    v-model="photoExposureTime"
                    type="text"
                    maxlength="32"
                    id="id_exposure_time"
                    name="exposure_time"
                    :label="$t('portfolio.exposure_time')"
                    :errors="errors?.exposure_time ? errors.exposure_time : []"
                  />
                </div>
                <div class="col-md-6">
                  <BaseInput
                    v-model="photoFocalLength"
                    type="number"
                    step="0.01"
                    id="id_focal_length"
                    name="focal_length"
                    :label="$t('portfolio.focal_length')"
                    :errors="errors?.focal_length ? errors.focal_length : []"
                  />
                </div>
                <div class="col-md-6">
                  <BaseInput
                    v-model="photoPhotographicSensitivity"
                    type="number"
                    min="0"
                    id="id_photographic_sensitivity"
                    name="photographic_sensitivity"
                    :label="$t('portfolio.photographic_sensitivity')"
                    :errors="
                      errors?.photographic_sensitivity
                      ? errors.photographic_sensitivity
                      : []
                    "
                  />
                </div>
                <div class="col-md-12">
                  <ListInput
                    v-model="photoTags"
                    id="id_tags"
                    name="tags"
                    :label="$t('portfolio.tags')"
                    :errors="errors?.tags ? errors.tags : []"
                  />
                </div>
              </form>
              <hr>
              <ul class="list-unstyled my-0 px-xl-10">
                <li>
                  {{ $t('portfolio.uploaded_at') }}
                  {{ getLocaleDateTimeString(photoUploadedAt) }}
                </li>
                <li>
                  {{ $t('portfolio.view_count') }}:
                  {{ photoViewCount }}
                </li>
                <li>
                  {{ $t('portfolio.likes') }}:
                  {{ photoLikeCount }}
                </li>
                <li>
                  {{ $t('portfolio.rating') }}:
                  {{ photoRating }}
                </li>
              </ul>
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
                :loadingStatus="photoUpdating"
                buttonClass="btn btn-brand"
                form="photo_modal_form"
              >
                {{ $t('btn.update') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>

      <div
        id="remove_photo_modal_choice"
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
              <h5 class="mb-0">{{ $t('portfolio.you_want_remove_photo') }}</h5>
              <p class="mb-0">{{ $t('portfolio.photo_information_will_lost') }}</p>
            </div>
            <div class="modal-footer flex-nowrap p-0">
              <button
                @click="removePhoto()"
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

<style scoped>
.modal-dialog-scrollable .modal-body::-webkit-scrollbar {
  width: 0.3em;
}
.modal-dialog-scrollable .modal-body::-webkit-scrollbar-track {
  background-color: #f5f5f5;
}
.modal-dialog-scrollable .modal-body::-webkit-scrollbar-thumb {
  background-color: #c0c0c0;
  border-radius: 1em;
}
.modal-dialog-scrollable .modal-body::-webkit-scrollbar-thumb:hover {
  background-color: #e72a26;
}

@media (min-width: 1200px) {
  .px-xl-10 {
    padding-right: 10rem !important;
    padding-left: 10rem !important;
  }
}
</style>

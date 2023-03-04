<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const { getLocaleDateTimeString } = useLocaleDateTime()

const emit = defineEmits(['updatePhoto', 'removePhoto'])

defineProps({
  photoList: {
    type: Array,
    required: true
  }
})

const photoUpdating = ref(false)

const photoUuid = ref(null)
const photoImage = ref(null)

const photoDevice = ref('')
const photoFNumber = ref(0.00)
const photoExposureTime = ref('')
const photoFocalLength = ref(0.00)
const photoPhotographicSensitivity = ref(0)

const photoTitle = ref('')
const photoDescription = ref('')
const photoTags = ref([])

const photoUploadedAt = ref(null)
const photoNumViews = ref(0)
const photoLikesCount = ref(0)
const photoRating = ref(0)

const errors = ref(null)

const updatePhotoModal = ref(null)
const updatePhotoModalBootstrap = ref(null)

const getPhotoData = async (pUuid) => {
  try {
    const response = await axios.get('/portfolio/photos/' + pUuid +'/')
    photoUuid.value = response.data.uuid
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
    photoNumViews.value = response.data.num_views
    photoLikesCount.value = response.data.likes_count
    photoRating.value = response.data.rating
  } catch (error) {
    console.error(error)
  }
}

const updatePhoto = async () => {
  photoUpdating.value = true
  try {
    const response = await axios.put(
      '/portfolio/photos/' + photoUuid.value +'/',
      {
        'device': photoDevice.value,
        'f_number': photoFNumber.value,
        'exposure_time': photoExposureTime.value,
        'focal_length': photoFocalLength.value,
        'photographic_sensitivity': photoPhotographicSensitivity.value,

        'title': photoTitle.value,
        'description': photoDescription.value,
        'tags': photoTags.value
      }
    )
    emit('updatePhoto', photoUuid.value, photoTitle.value)
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
      '/portfolio/photos/' + photoUuid.value +'/'
    )
    emit('removePhoto', photoUuid.value)
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  updatePhotoModal.value.addEventListener('hidden.bs.modal', () => {
    photoImage.value = null

    photoDevice.value = ''
    photoFNumber.value = 0.00
    photoExposureTime.value = ''
    photoFocalLength.value = 0.00
    photoPhotographicSensitivity.value = 0

    photoTitle.value = ''
    photoDescription.value = ''
    photoTags.value = []

    photoUploadedAt.value = null
    photoNumViews.value = 0
    photoLikesCount.value = 0
    photoRating.value = 0

    errors.value = null
  })
  updatePhotoModalBootstrap.value = new bootstrap.Modal(updatePhotoModal.value)
})
</script>

<template>
  <div class="portfolio-photo-list">
    <div class="row row-cols-1 row-cols-lg-2 row-cols-xl-3 g-1 mt-1">
      <div
        v-for="photoItem in photoList"
        :key="photoItem.uuid"
        class="col"
      >
        <div class="card h-100">
          <img
            :src="photoItem.thumbnail"
            :alt="photoItem.title"
            class="card-img-top"
          >
          <div class="card-body">
            <h5 class="card-title">
              {{ photoItem.title }}
            </h5>
            <p class="card-text">
              <small>
                {{ getLocaleDateTimeString(photoItem.uploaded_at) }}
              </small>
            </p>
          </div>
          <div class="card-footer">
            <div class="d-flex justify-content-center">
              <button
                @click="getPhotoData(photoItem.uuid)"
                type="button"
                class="btn btn-outline-secondary btn-sm"
                data-bs-toggle="modal"
                data-bs-target="#updatePhotoModal"
              >
                <i class="fa-solid fa-pen fa-sm"></i>
              </button>
              <button
                @click="photoUuid = photoItem.uuid"
                class="btn btn-danger btn-sm ms-1"
                type="button"
                data-bs-toggle="modal"
                data-bs-target="#removePhotoModalChoice"
              >
                <i class="fa-solid fa-trash fa-sm"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Teleport to="body">
      <div
        ref="updatePhotoModal"
        id="updatePhotoModal"
        class="modal fade"
        tabindex="-1"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        aria-hidden="true"
        aria-labelledby="updatePhotoModalLabel"
      >
        <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                class="modal-title"
                id="updatePhotoModalLabel"
              >
                {{ $t('auth.portfolio.updating_photo') }}
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
                id="photoModalForm"
                class="row g-3 mt-1 px-xl-10"
              >
                <div class="col-md-12">
                  <BaseInput
                    v-if="errors && errors.title"
                    v-model="photoTitle"
                    :label="$t('auth.portfolio.title')"
                    :errors="errors.title"
                    id="id_title"
                    name="title"
                    type="text"
                    maxlength="128"
                  />
                  <BaseInput
                    v-else
                    v-model="photoTitle"
                    :label="$t('auth.portfolio.title')"
                    id="id_title"
                    name="title"
                    type="text"
                    maxlength="128"
                  />
                </div>
                <div class="col-md-12">
                  <BaseTextarea
                    v-if="errors && errors.description"
                    v-model="photoDescription"
                    :label="$t('auth.portfolio.description')"
                    :errors="errors.description"
                    id="id_description"
                    name="description"
                  />
                  <BaseTextarea
                    v-else
                    v-model="photoDescription"
                    :label="$t('auth.portfolio.description')"
                    id="id_description"
                    name="description"
                  />
                </div>
                <div class="col-md-12">
                  <ListInput
                    v-if="errors && errors.tags"
                    v-model="photoTags"
                    :label="$t('auth.portfolio.tags')"
                    :errors="errors.tags"
                    id="id_tags"
                    name="tags"
                  />
                  <ListInput
                    v-else
                    v-model="photoTags"
                    :label="$t('auth.portfolio.tags')"
                    id="id_tags"
                    name="tags"
                  />
                </div>
                <div class="col-md-12">
                  <BaseInput
                    v-if="errors && errors.device"
                    v-model="photoDevice"
                    :label="$t('auth.portfolio.device')"
                    :errors="errors.device"
                    id="id_device"
                    name="device"
                    type="text"
                    maxlength="128"
                  />
                  <BaseInput
                    v-else
                    v-model="photoDevice"
                    :label="$t('auth.portfolio.device')"
                    id="id_device"
                    name="device"
                    type="text"
                    maxlength="128"
                  />
                </div>
                <div class="col-md-6">
                  <BaseInput
                    v-if="errors && errors.f_number"
                    v-model="photoFNumber"
                    :label="$t('auth.portfolio.f_number')"
                    :errors="errors.f_number"
                    id="id_f_number"
                    name="f_number"
                    type="number"
                    step="0.01"
                  />
                  <BaseInput
                    v-else
                    v-model="photoFNumber"
                    :label="$t('auth.portfolio.f_number')"
                    id="id_f_number"
                    name="f_number"
                    type="number"
                    step="0.01"
                  />
                </div>
                <div class="col-md-6">
                  <BaseInput
                    v-if="errors && errors.exposure_time"
                    v-model="photoExposureTime"
                    :label="$t('auth.portfolio.exposure_time')"
                    :errors="errors.exposure_time"
                    id="id_exposure_time"
                    name="exposure_time"
                    type="text"
                    maxlength="32"
                  />
                  <BaseInput
                    v-else
                    v-model="photoExposureTime"
                    :label="$t('auth.portfolio.exposure_time')"
                    id="id_exposure_time"
                    name="exposure_time"
                    type="text"
                    maxlength="32"
                  />
                </div>
                <div class="col-md-6">
                  <BaseInput
                    v-if="errors && errors.focal_length"
                    v-model="photoFocalLength"
                    :label="$t('auth.portfolio.focal_length')"
                    :errors="errors.focal_length"
                    id="id_focal_length"
                    name="focal_length"
                    type="number"
                    step="0.01"
                  />
                  <BaseInput
                    v-else
                    v-model="photoFocalLength"
                    :label="$t('auth.portfolio.focal_length')"
                    id="id_focal_length"
                    name="focal_length"
                    type="number"
                    step="0.01"
                  />
                </div>
                <div class="col-md-6">
                  <BaseInput
                    v-if="errors && errors.photographic_sensitivity"
                    v-model="photoPhotographicSensitivity"
                    :label="$t('auth.portfolio.photographic_sensitivity')"
                    :errors="errors.photographic_sensitivity"
                    id="id_photographic_sensitivity"
                    name="photographic_sensitivity"
                    type="number"
                    min="0"
                  />
                  <BaseInput
                    v-else
                    v-model="photoPhotographicSensitivity"
                    :label="$t('auth.portfolio.photographic_sensitivity')"
                    id="id_photographic_sensitivity"
                    name="photographic_sensitivity"
                    type="number"
                    min="0"
                  />
                </div>
              </form>
              <hr>
              <ul class="list-unstyled my-0 px-xl-10">
                <li>{{ $t('auth.portfolio.uploaded_at') }} {{ getLocaleDateTimeString(photoUploadedAt) }}</li>
                <li>{{ $t('auth.portfolio.num_views') }}: {{ photoNumViews }}</li>
                <li>{{ $t('auth.portfolio.likes') }}: {{ photoLikesCount }}</li>
                <li>{{ $t('auth.portfolio.rating') }}: {{ photoRating }}</li>
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
                form="photoModalForm"
              >
                {{ $t('btn.update') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>

      <div
        id="removePhotoModalChoice"
        class="modal fade"
        role="dialog"
        tabindex="-1"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        aria-hidden="true"
      >
        <div
          class="modal-dialog modal-dialog-centered"
          role="document"
        >
          <div class="modal-content rounded-3 shadow">
            <div class="modal-body p-4 text-center">
              <h5 class="mb-0">{{ $t('auth.portfolio.you_want_remove_photo') }}</h5>
              <p class="mb-0">{{ $t('auth.portfolio.photo_information_will_lost') }}</p>
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
.max-vh-75 {
  max-height: 75vh !important;
}
@media (min-width: 1200px) {
  .px-xl-10 {
    padding-right: 10rem !important;
    padding-left: 10rem !important;
  }
}
</style>
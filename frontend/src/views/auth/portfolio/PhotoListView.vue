<script setup>
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'
import PortfolioPhotoList from '@/components/auth/PortfolioPhotoList.vue'

const photoListLoading = ref(true)
const photoList = ref([])

const photosUploadStatus = ref(0)
const photosUploading = ref(false)

const uploadPhotosModal = ref(null)
const uploadPhotosModalBootstrap = ref(null)

const photosUploadStatusRound = computed(() => {
  return Math.round(photosUploadStatus.value)
})

const getPhotoList = async () => {
  try {
    const response = await axios.get('/portfolio/photo/author/list-create/')
    photoList.value = response.data
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

const updatePhotoList = (pUuid, pTitle) => {
  const foundIndex = photoList.value.findIndex((element) => {
    return element.uuid == pUuid
  })
  photoList.value[foundIndex].title = pTitle
}

const removePhotoList = (pUuid) => {
  photoList.value = photoList.value.filter((element) => {
    return element.uuid !== pUuid
  })
}

onMounted(() => {
  getPhotoList()
  uploadPhotosModal.value.addEventListener('hidden.bs.modal', () => {
    photosUploadStatus.value = 0
  })
  uploadPhotosModalBootstrap.value = new bootstrap.Modal(
    uploadPhotosModal.value
  )
})
</script>

<template>
  <div class="portfolio-photo-list-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <div class="d-flex align-items-center mb-5">
        <LocaleRouterLink
          routeName="Portfolio"
          class="link-danger text-decoration-none display-6"
        >
          {{ $t('portfolio.portfolio') }}
        </LocaleRouterLink>
        <i class="fa-solid fa-chevron-right mt-2 mx-2"></i>
        <h1 class="display-6 mb-0">
          {{ $t('portfolio.photos') }}
        </h1>
      </div>

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

      <LoadingIndicator v-if="photoListLoading" />
      <PortfolioPhotoList
        v-else
        :photoList="photoList"
        @updatePhoto="updatePhotoList"
        @removePhoto="removePhotoList"
      />
    </div>
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
    </Teleport>
  </div>
</template>

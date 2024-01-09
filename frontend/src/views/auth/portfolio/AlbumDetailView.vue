<script setup>
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import PortfolioPhotoList from '@/components/auth/PortfolioPhotoList.vue'

const route = useRoute()
const router = useRouter()

const albumDataLoading = ref(true)
const albumDataUpdating = ref(false)
const albumImageUpdating = ref(false)

const albumImage = ref(null)
const albumTitle = ref('')
const albumDescription = ref('')
const albumTags = ref([])
const albumCreatedAt = ref(null)
const albumViewCount = ref(0)
const albumLikeCount = ref(0)
const albumRating = ref(0)

const { getLocaleDateTimeString } = useLocaleDateTime()

const status = ref(null)
const errors = ref(null)

const getAlbumData = async () => {
  try {
    const response = await axios.get(
      '/portfolio/album/author/rud/'
        + route.params.uuid
        +'/'
    )
    albumImage.value = response.data.image
    albumTitle.value = response.data.title
    albumDescription.value = response.data.description
    albumTags.value = response.data.tags
    albumCreatedAt.value = response.data.created_at
    albumViewCount.value = response.data.view_count
    albumLikeCount.value = response.data.like_count
    albumRating.value = response.data.rating
  } catch (error) {
    console.error(error)
  } finally {
    albumDataLoading.value = false
  }
}

const updateAlbumImage = async (filelist) => {
  albumImageUpdating.value = true

  let formData = new FormData()
  formData.append('image', filelist[0], filelist[0].name)

  try {
    const response = await axios.put(
      '/portfolio/album/author/image-update/'
        + route.params.uuid
        +'/',
      formData
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
  albumDataUpdating.value = true
  try {
    const response = await axios.put(
      '/portfolio/album/author/rud/'
        + route.params.uuid
        +'/',
      {
        title: albumTitle.value,
        description: albumDescription.value,
        tags: albumTags.value
      }
    )
    router.push({ name: 'PortfolioAlbumList' })
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    albumDataUpdating.value = false
  }
}

const removeAlbum = async () => {
  try {
    const response = await axios.delete(
      '/portfolio/album/author/rud/'
        + route.params.uuid
        +'/'
    )
    router.push({ name: 'PortfolioAlbumList' })
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  getAlbumData()
})
</script>

<template>
  <div class="portfolio-album-detail-view">
    <LoadingIndicator v-if="albumDataLoading" />
    <div
      v-else
      class="px-1 px-lg-3 px-xl-5"
    >
      <div class="d-flex align-items-center mb-3">
        <router-link
          :to="{ name: 'Portfolio' }"
          class="link-danger text-decoration-none display-6"
        >
          {{ $t('portfolio.portfolio') }}
        </router-link>
        <i class="fa-solid fa-chevron-right mt-2 mx-2"></i>
        <router-link
          :to="{ name: 'PortfolioAlbumList' }"
          class="link-danger text-decoration-none display-6"
        >
          {{ $t('portfolio.albums') }}
        </router-link>
        <i class="fa-solid fa-chevron-right mt-2 mx-2"></i>
        <h1 class="display-6 mb-0">
          {{ albumTitle }}
        </h1>
      </div>
      <div class="card mb-2">
        <LoadingIndicator
          v-if="albumImageUpdating"
          :actionInfo="$t('portfolio.uploading_image')"
        />
        <div v-else>
          <img
            :src="albumImage"
            class="card-img-top"
          >
          <div class="card-body text-center">
            <small
              v-if="status === 200"
              class="text-success"
            >
              {{ $t('portfolio.image_updated_successfully') }}
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
                buttonClass="btn btn-soft-brand m-1"
                accept="image/*"
              >
                {{ $t('portfolio.update_image') }}
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
        id="album_form"
        class="row g-3"
      >
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
        <div class="col-md-12">
          <ListInput
            v-model="albumTags"
            id="id_tags"
            name="tags"
            :label="$t('portfolio.tags')"
            :errors="errors?.tags ? errors.tags : []"
          />
        </div>
      </form>

      <hr>
      <ul class="list-unstyled my-0 px-xl-10">
        <li>{{ $t('portfolio.created_at') }} {{ getLocaleDateTimeString(albumCreatedAt) }}</li>
        <li>{{ $t('portfolio.view_count') }}: {{ albumViewCount }}</li>
        <li>{{ $t('portfolio.likes') }}: {{ albumLikeCount }}</li>
        <li>{{ $t('portfolio.rating') }}: {{ albumRating }}</li>
      </ul>

      <div class="d-grid d-md-flex justify-content-md-end gap-2 mt-3">
        <button
          type="button"
          class="btn btn-outline-dark"
          data-bs-toggle="modal"
          data-bs-target="#remove_album_modal_choice"
        >
          {{ $t('btn.delete') }}
        </button>
        <SubmitButton
          :loadingStatus="albumDataUpdating"
          buttonClass="btn btn-brand w-100"
          form="album_form"
        >
          {{ $t('btn.update') }}
        </SubmitButton>
      </div>
      <hr>
      <PortfolioPhotoList />
    </div>

    <Teleport to="body">
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
